import SimPy.RandomVariantGenerators as RVGs
import SimPy.SamplePathClasses as PathCls
from InputData import HealthState
import SimPy.MarkovClasses as Markov


class Patient:
    def __init__(self, id, trans_rate_matrix):

        self.id = id
        self.transRateMatrix = trans_rate_matrix
        self.stateMonitor = PatientStateMonitor()

    def simulate(self, sim_length):

        rng = RVGs.RNG(seed=self.id)
        gillespie = Markov.Gillespie(transition_rate_matrix=self.transRateMatrix)

        t = 0
        if_stop = False
        # while the patient is alive and simulation length is not yet reached
        while not if_stop:
            dt, new_state_index = gillespie.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=rng)

            if dt is None or dt + t > sim_length:
                if_stop = True
            else:
                # increment time
                t += dt
                # update health state
                self.stateMonitor.update(time=t, new_state=HealthState(new_state_index))


class PatientStateMonitor:
    def __init__(self):

        self.currentState = HealthState.WELL    # assuming everyone starts in "Well"
        self.survivalTime = None
        self.nStrokes = 0

    def update(self, time, new_state):

        if new_state == HealthState.STROKE_DEAD or HealthState.NATURAL_DEATH:
            self.survivalTime = time

        if self.currentState == HealthState.STROKE or self.currentState == HealthState.STROKE_DEAD:
            self.nStrokes += 1

        self.currentState = new_state

    def get_if_alive(self):
        if self.currentState != HealthState.STROKE_DEAD or self.currentState != HealthState.NATURAL_DEATH:
            return True
        else:
            return False


class Cohort:
    def __init__(self, id, pop_size, trans_rate_matrix):

        self.id = id
        self.popSize = pop_size
        self.transRateMatrix = trans_rate_matrix
        self.cohortOutcomes = CohortOutcomes()

    def simulate(self, sim_length):

        patients = []
        for i in range(self.popSize):
            patient = Patient(id=self.id*self.popSize + i,
                              trans_rate_matrix=self.transRateMatrix)
            patients.append(patient)

        for patient in patients:
            patient.simulate(sim_length=sim_length)

        self.cohortOutcomes.extract_outcomes(patients)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []
        self.nTotalStrokes = []
        self.nLivingPatients = None
        self.meanSurvivalTime = None
        self.meanNumOfStrokes = None

    def extract_outcomes(self, simulated_patients):
        for patient in simulated_patients:
            if not (patient.stateMonitor.survivalTime is None):
                self.survivalTimes.append(patient.stateMonitor.survivalTime)
                self.nTotalStrokes.append(patient.stateMonitor.nStrokes)

        self.meanSurvivalTime = sum(self.survivalTimes) / len(self.survivalTimes)
        self.meanNumOfStrokes = sum(self.nTotalStrokes) / len(self.nTotalStrokes)

        self.nLivingPatients = PathCls.PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size= len(simulated_patients),
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )
