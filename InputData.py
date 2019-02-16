from enum import Enum


# simulation settings
POP_SIZE = 2000         # cohort population size
SIMULATION_LENGTH = 50    # length of simulation (years)

ANNUAL_PROB_BACKGROUND_MORT = 18 / 1000


class HealthState(Enum):
    """ health states of patients """
    WELL = 0
    POST_STROKE = 1
    DEAD = 2
    STROKE = 3
    NATURAL_DEATH = 4


# transition probability matrix without anticoagulation
TRANS_RATE_MATRIX_1 = [
    [0, 0.136, 0, 0.00151, 0.0178],       # WELL
    [0, 0, 52, 0, 0],                     # STROKE
    [0, 0.03, 0, 0.0075, 0.0178],         # POST-STROKE
    [0, 0, 0, 0, 0],                      # STROKE-DEATH
    [0, 0, 0, 0, 0]                       # NATURAL-DEATH
]


# transition probability matrix with anticoagulation
TRANS_RATE_MATRIX_2 = [
    [0, 0.136, 0, 0.00151, 0.0187],       # WELL
    [0, 0, 52, 0, 0],                     # STROKE
    [0, 0.023, 0, 0.0056, 0.0187],         # POST-STROKE
    [0, 0, 0, 0, 0],                      # STROKE-DEATH
    [0, 0, 0, 0, 0]                       # NATURAL-DEATH
]



