from dataclasses import dataclass
from typing import List
import numpy as np
from src.config.config_price import REF_PRICE, MAX_PRICE

# --- DATA STRUCTURE ---
@dataclass
class Bid:
    id: int
    name: str
    price: float  # in euros

def generate_test_bids() -> List[Bid]:
    """
    Generates test bids based on REF_PRICE and MAX_PRICE with predefined reductions
    """
    reductions = [2, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 75]
    test_bids = []
    
    # Add reference price bid
    test_bids.append(Bid(11000, "ref", REF_PRICE))
    
    # Add max price bid
    test_bids.append(Bid(11001, "testMax", MAX_PRICE))
    
    # Add reduction bids
    for i, reduction in enumerate(reductions):
        price = MAX_PRICE * (1 - reduction/100)
        test_bids.append(
            Bid(11000 + i + 2, f"test{reduction:02d}", price)
        )
    
    return test_bids


# --- COMPETITION DATA ---
# bids: List[Bid] = []

bids: List[Bid] = [
    Bid(11003, "ref", 1_050_000.00),
    Bid(11115, "testMax", 1_260_000.00),
    Bid(11151, "test05", 1_197_000.00),
    Bid(11161, "test10", 928_000.00),
    Bid(11163, "test15", 1_053_700.00),
    Bid(11178, "test20", 919_000.00),
    Bid(11192, "test25", 459_094.60),
    Bid(11196, "test30", 890_700.00),
    Bid(11250, "test35", 630_000.00),
    Bid(11245, "test40", 567_000.00),
    Bid(11235, "test50", 420_000.00),
    Bid(11240, "test60", 504_000.00),
    Bid(11230, "test70", 378_000.00),
    Bid(11220, "test80", 252_000.00),
    Bid(11210, "test90", 126_000.00),
    Bid(11200, "test95", 63_000.00)
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