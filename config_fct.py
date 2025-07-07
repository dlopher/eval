# ---------LINEAR: FACTOR A --------------

MAX_PROJECTS_PER_DISCIPLINA = 5

FACTOR_WEIGHTS = {
    "A1": 35,
    "A2": 40,
    "A3": 15,
    "A4": 10,
}

# Absolute thresholds (euros)
    # anything below → 0 points
    # anything above → 100 points

FACTOR_THRESHOLDS = {
    "A1": {"ABS_MIN": 6_000_000.0, "ABS_MAX": 20_000_000.0},
    "A2": {"ABS_MIN": 6_000_000.0, "ABS_MAX": 20_000_000.0},
    "A3": {"ABS_MIN": 4_000_000.0, "ABS_MAX": 20_000_000.0},
    "A4": {"ABS_MIN": 6_000_000.0, "ABS_MAX": 20_000_000.0},
}

MIN_SCORE_PER_PROJECT = 1
MAX_SCORE_PER_PROJECT = 100

"""
# ---------SIGMOID--------------
# Pontuación para los extremos
SCORE_AT_MIN = 1.0000      # on a 0–100 scale, at ABS_MIN
SCORE_AT_MAX = 99.9999     # on a 0–100 scale, at ABS_MAX

# Convert to fractions (0–1):
s_min = SCORE_AT_MIN / 100.0
s_max = SCORE_AT_MAX / 100.0

# Anchor positions:
L = ABS_MIN
U = ABS_MAX

# Solve for a logistic of form 
#   f(x) = 1 / (1 + exp( k*(x - x0) ))
# with f(L)=s_min and f(U)=s_max
alpha_low  = (1.0 / s_min) - 1.0
alpha_high = (1.0 / s_max) - 1.0

# k = ln(alpha_low / alpha_high) / (L - U)
SIGMOID_K_FCT = math.log(alpha_low/alpha_high) / (L - U)

# x0 = L - ln(alpha_low)/k
SIGMOID_X0_FCT = L - (math.log(alpha_low) / SIGMOID_K_FCT)

"""