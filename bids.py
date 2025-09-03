from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass
class Bid:
    id: int
    price: float  # in euros

# CONCORRENTES, PREÇO
# bids: List[Bid] = []


bids: List[Bid] = [
    Bid(1, 1_053_496.00),
    Bid(2, 1_200_000.00),
    Bid(3, 1_000_000.00),
    Bid(4,   800_000.00),
    Bid(5, 1_100_000.00),
    Bid(6,   700_000.00),
    Bid(7, 1_300_000.00),
    Bid(8, 1_259_000.00),
    Bid(9,   900_000.00),
    Bid(10, 600_000.00)
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