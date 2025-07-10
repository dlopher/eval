from dataclasses import dataclass
from typing import List

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
    Bid(10, 600_000.00),
]
