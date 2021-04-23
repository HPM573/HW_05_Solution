import numpy as np

import SimPy.Markov as Markov
import SimPy.SamplePath as Path
from InputData import HealthStates


class Patient:
    def __init__(self, id, trans_rate_matrix):
        """ initiates a patient
        :param id: ID of the patient
        :param trans_rate_matrix: transition rate matrix
        """

        self.id = id
        self.transRateMatrix = trans_rate_matrix
        self.stateMonitor = PatientStateMonitor()

    def simulate(self, sim_length):
        """ simulate the patient over the specified simulation length """

        # random number generator for this patient
        rng = np.random.RandomState(seed=self.id)
        # gillespie algorithm
        gillespie = Markov.Gillespie(transition_rate_matrix=self.transRateMatrix)

        t = 0  # simulation time
        if_stop = False

        # while the patient is alive and simulation length is not yet reached
        while not if_stop:
            # find time until next event (dt), and next state
            # (note that the gillespie algorithm returns None for dt if the process
            # is in an absorbing state)
            dt, new_state_index = gillespie.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=rng)

            # stop if time to next event (dt) is None (i.e. we have reached an absorbing state)
            if dt is None:
                if_stop = True

            else:
                # else if next event occurs beyond simulation length
                if dt + t > sim_length:
                    # advance time to the end of the simulation and stop
                    t = sim_length
                    # the individual stays in the current state until the end of the simulation
                    new_state_index = self.stateMonitor.currentState.value
                    if_stop = True
                else:
                    # advance time to the time of next event
                    t += dt
                # update health state
                self.stateMonitor.update(time=t, new_state=HealthStates(new_state_index))


class PatientStateMonitor:

    def __init__(self):

        self.currentState = HealthStates.WELL    # assuming everyone starts in "Well"
        self.survivalTime = None
        self.nStrokes = 0

    def update(self, time, new_state):
        """
        update the current health state to the new health state
        :param time: current time
        :param new_state: new state
        """

        # update survival time
        if new_state in (HealthStates.STROKE_DEAD, HealthStates.NATURAL_DEATH):
            self.survivalTime = time

        # update number of strokes
        if new_state in (HealthStates.STROKE, HealthStates.STROKE_DEAD) :
            self.nStrokes += 1

        # update current health state
        self.currentState = new_state


class Cohort:

    def __init__(self, id, pop_size, trans_rate_matrix):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param trans_rate_matrix: transition rate matrix
        """
        self.id = id
        self.popSize = pop_size
        self.transRateMatrix = trans_rate_matrix
        self.cohortOutcomes = CohortOutcomes()

    def simulate(self, sim_length):
        """ simulate the cohort of patients over the specified number of time-steps
        :param sim_length: simulation length
        """

        # populate the cohort
        patients = []
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id*self.popSize + i,
                              trans_rate_matrix=self.transRateMatrix)
            # add the patient to the cohort
            patients.append(patient)

        # simulate all patients
        for patient in patients:
            patient.simulate(sim_length=sim_length)

        # store outputs of this simulation
        self.cohortOutcomes.extract_outcomes(patients)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []
        self.nTotalStrokes = []
        self.nLivingPatients = None
        self.meanSurvivalTime = None
        self.meanNumOfStrokes = None

    def extract_outcomes(self, simulated_patients):
        """ extracts outcomes of a simulated cohort
        :param simulated_patients: a list of simulated patients"""

        for patient in simulated_patients:
            # survival time
            if not (patient.stateMonitor.survivalTime is None):
                self.survivalTimes.append(patient.stateMonitor.survivalTime)
            # number of strokes
            self.nTotalStrokes.append(patient.stateMonitor.nStrokes)

        self.meanSurvivalTime = sum(self.survivalTimes) / len(self.survivalTimes)
        self.meanNumOfStrokes = sum(self.nTotalStrokes) / len(self.nTotalStrokes)

        self.nLivingPatients = Path.PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=len(simulated_patients),
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )
