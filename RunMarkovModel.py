import MarkovClasses as Cls
import SimPy.SamplePathClasses as PathCls
import SimPy.FigureSupport as Fig
import InputData as D

# Markov model without temp state
myCohortNoAntiCoag = Cls.Cohort(id=1,
                                pop_size=D.POP_SIZE,
                                trans_matrix=D.get_trans_rate_matrix(with_treatment=False))
# Markov model with temp state
myCohortWithAntiCoag = Cls.Cohort(id=1,
                                  pop_size=D.POP_SIZE,
                                  trans_matrix=D.get_trans_rate_matrix(with_treatment=True))

# simulate all models
myCohortNoAntiCoag.simulate(sim_length=D.SIMULATION_LENGTH)
myCohortWithAntiCoag.simulate(sim_length=D.SIMULATION_LENGTH)


# sample paths
PathCls.graph_sample_path(
    sample_path=myCohortNoAntiCoag.cohortOutcomes.nLivingPatients,
    title='Survival Curve (Model without anticoagulation)',
    x_label='Time Step (Year)',
    y_label='Number of Surviving Patients'
)
PathCls.graph_sample_path(
    sample_path=myCohortWithAntiCoag.cohortOutcomes.nLivingPatients,
    title='Survival Curve (Model with anticoagulation)',
    x_label='Time Step (Year)',
    y_label='Number of Surviving Patients'
)


# histograms of survival times
Fig.graph_histogram(
    data=myCohortNoAntiCoag.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time\n(Model without anticoagulation)',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1
)
Fig.graph_histogram(
    data=myCohortWithAntiCoag.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time\n(Model with anticoagulation)',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1
)
# histogram of number of strokes
Fig.graph_histogram(
    data=myCohortNoAntiCoag.cohortOutcomes.nTotalStrokes,
    title='Number of Strokes (Without anticoagulation)',
    x_label='Number of Strokes',
    y_label='Count',
    bin_width=1
)

Fig.graph_histogram(
    data=myCohortWithAntiCoag.cohortOutcomes.nTotalStrokes,
    title='Number of Strokes (With anticoagulation)',
    x_label='Number of Strokes',
    y_label='Count',
    bin_width=1
)

# print the patient survival time
print('Mean survival time for the model without anticoagulation (years):',
      myCohortNoAntiCoag.cohortOutcomes.meanSurvivalTime)
print('Mean survival time for the model with anticoagulation (years):',
      myCohortWithAntiCoag.cohortOutcomes.meanSurvivalTime)


