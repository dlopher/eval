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
    "A3": {"ABS_MIN": 6_000_000.0, "ABS_MAX": 20_000_000.0},
    "A4": {"ABS_MIN": 6_000_000.0, "ABS_MAX": 20_000_000.0},
}

MIN_SCORE_PER_PROJECT = 1
MAX_SCORE_PER_PROJECT = 100
