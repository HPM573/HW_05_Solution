import MarkovClasses as Cls
import SimPy.Plots.SamplePaths as Path
import SimPy.Plots.Histogram as Hist
import InputData as D

# -----------------------------
# Model with no anticoagulation
# -----------------------------
myCohortNoAntiCoag = Cls.Cohort(id=1,
                                pop_size=D.POP_SIZE,
                                trans_rate_matrix=D.get_trans_rate_matrix(with_treatment=False))

# simulate
myCohortNoAntiCoag.simulate(sim_length=D.SIMULATION_LENGTH)

# survival curve
Path.plot_sample_path(
    sample_path=myCohortNoAntiCoag.cohortOutcomes.nLivingPatients,
    title='Survival Curve (Model without anticoagulation)',
    x_label='Time Step (Year)',
    y_label='Number of Surviving Patients'
)

# histograms of survival times
Hist.plot_histogram(
    data=myCohortNoAntiCoag.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time\n(Model without anticoagulation)',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=5
)

# histogram of number of strokes
Hist.plot_histogram(
    data=myCohortNoAntiCoag.cohortOutcomes.nTotalStrokes,
    title='Number of Strokes (Without anticoagulation)',
    x_label='Number of Strokes',
    y_label='Count',
    bin_width=1,
    x_range=[0, 7]
)

# print the patient survival time and average number of strokes
print('Without anticoagulation:')
print('     Mean survival time for the model (years):',
      myCohortNoAntiCoag.cohortOutcomes.meanSurvivalTime)
print('     Mean number of strokes:',
      myCohortNoAntiCoag.cohortOutcomes.meanNumOfStrokes)


# -----------------------------
# Markov model with anticoagulation
# -----------------------------
myCohortWithAntiCoag = Cls.Cohort(id=1,
                                  pop_size=D.POP_SIZE,
                                  trans_rate_matrix=D.get_trans_rate_matrix(with_treatment=True))

# simulate
myCohortWithAntiCoag.simulate(sim_length=D.SIMULATION_LENGTH)

# survival curve
Path.plot_sample_path(
    sample_path=myCohortWithAntiCoag.cohortOutcomes.nLivingPatients,
    title='Survival Curve (Model with anticoagulation)',
    x_label='Time Step (Year)',
    y_label='Number of Surviving Patients'
)

# histograms of survival times
Hist.plot_histogram(
    data=myCohortWithAntiCoag.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time\n(Model with anticoagulation)',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=5
)

# histogram of number of strokes
Hist.plot_histogram(
    data=myCohortWithAntiCoag.cohortOutcomes.nTotalStrokes,
    title='Number of Strokes (With anticoagulation)',
    x_label='Number of Strokes',
    y_label='Count',
    bin_width=1,
    x_range=[0, 7]
)

print('With anticoagulation:')
print('     Mean survival time for the model (years):',
      myCohortWithAntiCoag.cohortOutcomes.meanSurvivalTime)
print('     Mean number of strokes:',
      myCohortWithAntiCoag.cohortOutcomes.meanNumOfStrokes)

