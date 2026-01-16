# ---------LINEAR: FACTOR A --------------

MAX_PROJECTS_PER_DISCIPLINA = 5

FACTOR_WEIGHTS = {
    "A1": 20,
    "A2": 30,
    "A3": 30,
    "A4": 17,
    "A5": 3,
}

# Absolute thresholds (euros)
    # anything below → 0 points
    # anything above → 100 points

FACTOR_THRESHOLDS = {
     "A1": {
        "default": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
        "BIM": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
    },
    "A2": {
        "default": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
        "BIM": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
    },
    "A3": {
        "default": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
        "BIM": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
    },
    "A4": {
        "default": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
        "BIM": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
    },
    "A5": {
        "default": {"ABS_MIN": 100.0, "ABS_MAX": 1_000.0},
        "formação BIM": {"ABS_MIN": 80.0, "ABS_MAX": 800.0},
    }
}

MIN_SCORE_PER_PROJECT = 1
MAX_SCORE_PER_PROJECT = 100
