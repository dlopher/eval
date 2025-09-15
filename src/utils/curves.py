import math
from src.config.config_price import MAX_SCORE, MIN_SCORE, MAX_PRICE, REF_PRICE, SIGMOID_K, SIGMOID_X0, LOWER_THRESHOLD, UPPER_THRESHOLD
from src.config.config_linear import MIN_SCORE_PER_PROJECT, MAX_SCORE_PER_PROJECT


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


def linear(price: float, min_score: float = MIN_SCORE, max_score: float = MAX_SCORE) -> float:
    """
    Linear mapping from 0 to MAX_PRICE.
    Higher price → lower score.
    """
    # Normalize price to [0,1] range, inverted
    norm = 1.0 - min(1.0, price / MAX_PRICE)
    # Map to score range
    return min_score + norm * (max_score - min_score)


def inverse_proportional(price: float, min_score: float = MIN_SCORE, max_score: float = MAX_SCORE, power: float = 1.0) -> float:
    """
    Inverse‐proportional map: higher price → lower score.

    Uses the mathematical function: score ∝ (MAX_PRICE/price)^power
    
    Parameters:
        power: Higher values create a more aggressive curve that favors lower prices
               - power=1: Standard hyperbola (1/x shape)
               - power=2: Quadratic fall-off
               - power=0.5: Square root fall-off (more gradual)
    """
    if price <= 0:
        return max_score
        
    # Calculate inverse value with optional power for steepness control
    inv_val = (MAX_PRICE / price) ** power
    
    # Normalize between 1 and MAX_PRICE/epsilon
    norm = (inv_val - 1) / ((MAX_PRICE / 0.001) - 1)
    norm = max(0.0, min(1.0, norm))
    
    # Map to score range
    return min_score + norm * (max_score - min_score)


def exponential(price: float, min_score: float = MIN_SCORE, max_score: float = MAX_SCORE, alpha: float = 4.0) -> float:
    """
    Exponential decay: score decays exponentially as price increases.
    Higher alpha = steeper curve.
    """
    # Normalize price to [0,1] range
    t = min(1.0, price / MAX_PRICE)
    
    # Exponential decay function
    decay = math.exp(-alpha * t)
    
    # Map to score range
    return min_score + decay * (max_score - min_score)


def sigmoid(price: float, min_score: float = MIN_SCORE, max_score: float = MAX_SCORE) -> float:
    """
    Calculates a score from 0 to 100 using a sigmoid function:
        P = 100 / (1 + exp(k * ((price / REF_PRICE) - 1 - x0)))
    where:
        - price: the bid/proposal value
        - REF_PRICE: reference price
        - k, x0: sigmoid parameters
    Returns:
        Score in the range [min_score, max_score].
    """
    # compute relative delta
    x_rel = (price / REF_PRICE) - 1.0
    
    # logistic with steepness K and center X0
    frac = 1.0 / (1.0 + math.exp(SIGMOID_K * (x_rel - SIGMOID_X0)))
    
    # Map to the specified score range
    score = min_score + frac * (max_score - min_score)
    
    return max(min_score, min(max_score, score))


def semicircle(price: float, min_score: float = MIN_SCORE, max_score: float = MAX_SCORE) -> float:
    """
    Calculates a score from 0 to 100 using a semicircle function:
        C = 100 * sqrt(1 - x²)
    where:
        - x = price / max_price
        - max_price = REF_PRICE * UPPER_THRESHOLD
    
    Returns:
        Score in the range [min_score, max_score, 100].
    """
    x = price / MAX_PRICE
    
    # Ensure x is in valid range for sqrt(1-x²)
    x = max(0.0, min(1.0, x))
    
    # Semicircle equation: normalized to [0, 1]
    frac = math.sqrt(1 - x * x)

    # Map to the specified score range
    score = min_score + frac * (max_score - min_score)
    
    return max(min_score, min(max_score, score))
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