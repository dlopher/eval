import math
from config import REF_PRICE, SIGMOID_K, SIGMOID_X0, LOWER_THRESHOLD, UPPER_THRESHOLD
from config_fct import MIN_SCORE_PER_PROJECT, MAX_SCORE_PER_PROJECT

def linear_abs(cost: float, abs_min: float, abs_max: float) -> float:
    """
    Linear mapping from ABS_MIN→1 point up to ABS_MAX→100 points.
    Below ABS_MIN → 0; above ABS_MAX → 100.
    """
    if cost < abs_min:
        return 0.0
    if cost > abs_max:
        return float(MAX_SCORE_PER_PROJECT)
    # interpolate so ABS_MIN => 1, ABS_MAX => 100
    return MIN_SCORE_PER_PROJECT + (cost - abs_min) * ((MAX_SCORE_PER_PROJECT - MIN_SCORE_PER_PROJECT) / (abs_max - abs_min))

def _clamp(x, lo=0.0, hi=100.0):
    return max(lo, min(hi, x))

def linear(price: float) -> float:
    """
    Linear map: at LOWER_THRESHOLD*REF → 100, at UPPER_THRESHOLD*REF → 0
    """
    x = price / REF_PRICE
    # normalize to [0,1]
    norm = (UPPER_THRESHOLD - x) / (UPPER_THRESHOLD - LOWER_THRESHOLD)
    return _clamp(norm * 100)

def inverse_proportional(price: float) -> float:
    """
    Inverse‐proportional map: higher price → lower score,
    normalized so that at LOWER_THRESHOLD*REF → 100, at UPPER_THRESHOLD*REF → 0
    """
    inv_val = (REF_PRICE / price)
    inv_lo = 1 / LOWER_THRESHOLD
    inv_hi = 1 / UPPER_THRESHOLD
    norm = (inv_val - inv_hi) / (inv_lo - inv_hi)
    return _clamp(norm * 100)

def exponential(price: float, alpha: float = 5.0) -> float:
    """
    Exponential decay: at LOWER_THRESHOLD*REF → ~100,
    at UPPER_THRESHOLD*REF → ~0. Uses parameter alpha to control sharpness.
    """
    # normalized [0,1] between safe thresholds
    x = price / REF_PRICE
    t = (x - LOWER_THRESHOLD) / (UPPER_THRESHOLD - LOWER_THRESHOLD)
    t = max(0.0, min(1.0, t))
    # map t∈[0,1] to score∈[100→0] via (exp(-α t) − exp(-α))/(1 − exp(-α))
    num = math.exp(-alpha * t) - math.exp(-alpha)
    den = 1 - math.exp(-alpha)
    return _clamp((num / den) * 100)

def sigmoid(price: float) -> float:
    """
    Calculates a score from 0 to 100 using a sigmoid function:
        P = 100 / (1 + exp(k * ((price / REF_PRICE) - 1 - x0)))
    where:
        - price: the bid/proposal value
        - REF_PRICE: reference price
        - k, x0: sigmoid parameters
    Returns:
        Score in the range [0, 100].
    """
    # compute relative delta
    x_rel = (price / REF_PRICE) - 1.0
    # logistic with steepness K and center X0
    frac = 1.0 / (1.0 + math.exp(SIGMOID_K * (x_rel - SIGMOID_X0)))
    return max(0.0, min(100.0, frac * 100.0))

"""
def sigmoid_abs(price: float) -> float:
    
    # - price < ABS_MIN → 0
    # - price >= ABS_MAX → 100
    # - otherwise → logistic between 1 and 100 points.
    
    # outside clamps
    if price < ABS_MIN:
        return 0.0
    if price > ABS_MAX:
        return 100.0

    # logistic in between
    exponent = SIGMOID_K_FCT * (price - SIGMOID_X0_FCT)
    frac     = 1.0 / (1.0 + math.exp(exponent))
    return max(0.0, min(100.0, frac * 100.0))

"""