from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass
class Bid:
    id: int
    name: str
    price: float  # in euros

# CONCORRENTES, PREÇO
# bids: List[Bid] = []

bids: List[Bid] = [
    Bid(11003, "a", 739_606.16),
    Bid(11115, "b", 1_143_200.00),
    Bid(11151, "c", 805_988.80),
    Bid(11161, "d", 928_000.00),
    Bid(11163, "e", 1_053_700.00),
    Bid(11178, "f", 919_000.00),
    Bid(11180, "g", 1_260_000.00),
    Bid(11192, "h", 459_094.60),
    Bid(11196, "i", 890_700.00)
]


def calc_abnormally_low_bid(bid_prices=None, factor=0.8):
    """
    Calculate the abnormally low price threshold.
    
    Args:
        bid_prices: Optional list of prices. If None, uses all bids in the module.
        factor: Factor to multiply the average by (default: 0.8 - 20% below average)
    
    Returns:
        The abnormally low price threshold, or 0 if no prices provided
    """
    if bid_prices is None:
        bid_prices = [bid.price for bid in bids]
    
    if not bid_prices: # Empty list
        return 0
    
    avg = np.mean(bid_prices)
    return avg * factor