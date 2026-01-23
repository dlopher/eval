from datetime import datetime


# --- date validation ---
CURRENT_DATE = datetime.now()

DATE_LIMITS = {
    "projeto": 15,
    "formação": 999,
}

# Accepted date formats for parsing
ACCEPTED_DATE_FORMATS = [
    '%d/%m/%Y',   # dd/mm/yyyy
    '%d/%m/%y',   # dd/mm/yy
    '%d-%m-%Y',   # dd-mm-yyyy
    '%d-%m-%y',   # dd-mm-yy
]


# --- factor configuration ---
FACTOR_WEIGHTS = {
    "A1": 17,
    "A2": 30,
    "A3": 30,
    "A4": 20,
    "A5": 3,
}

FACTOR_THRESHOLDS = {
     "A1": {
        "default": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
        # "BIM": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
    },
    "A2": {
        "default": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
        # "BIM": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
    },
    "A3": {
        "default": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
        "BIM": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
    },
    "A4": {
        "default": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
        # "BIM": {"ABS_MIN": 5_000_000.0, "ABS_MAX": 25_000_000.0},
    },
    "A5": {
        "default": {"ABS_MIN": 100.0, "ABS_MAX": 1_000.0},
        "formação BIM": {"ABS_MIN": 80.0, "ABS_MAX": 800.0},
    }
}

MAX_PROJECTS_PER_DISCIPLINA = 5

MIN_SCORE_PER_PROJECT = 1
MAX_SCORE_PER_PROJECT = 100
