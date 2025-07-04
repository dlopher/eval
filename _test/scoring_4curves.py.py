import numpy as np
import matplotlib.pyplot as plt

# Reference price and bids
ref = 1053496.00
bids = np.array([
    1053496.00,   # Reference
    1264000.00,   # +20%
    1000000.00,   # -5.08%
    800000.00,    # -24.05%
    1100000.00    # +4.41%
])

# Define curve parameters (using ±20% boundaries)
x_min = ref * 0.8   # 842,796.80
x_max = ref * 1.2   # 1,264,195.20
x_best = x_min      # Best possible price
k_exp = 2           # Exponential factor
k_sig = 0.0000015   # Sigmoid steepness
x_target = ref      # Sigmoid target

# 1. Linear Curve
def linear_score(x):
    return 100 * (x_max - x) / (x_max - x_min)

# 2. Inverse Proportional
def inverse_score(x):
    return 100 * (x_best / np.where(x < x_best, x_best, x))

# 3. Exponential
def exp_score(x):
    base = np.clip((x_max - x) / (x_max - x_min), 0, 1)
    return 100 * (base ** k_exp)

# 4. Sigmoid
def sigmoid_score(x):
    return 100 / (1 + np.exp(-k_sig * (x - x_target)))

# Calculate all scores
results = {
    "Bid 1 (Reference)": bids[0],
    "Bid 2 (+20%)": bids[1],
    "Bid 3 (-5.08%)": bids[2],
    "Bid 4 (-24.05%)": bids[3],
    "Bid 5 (+4.41%)": bids[4]
}

for name, bid in results.items():
    print(f"\n{name}: €{bid:,.2f}")
    print(f"  Linear: {linear_score(bid):.1f}")
    print(f"  Inverse: {inverse_score(bid):.1f}")
    print(f"  Exponential: {exp_score(bid):.1f}")
    print(f"  Sigmoid: {sigmoid_score(bid):.1f}")

# Generate comparison table
data = [
    ["Curve Type", "Bid 1", "Bid 2", "Bid 3", "Bid 4", "Bid 5"],
    ["Linear", *[f"{linear_score(b):.1f}" for b in bids]],
    ["Inverse", *[f"{inverse_score(b):.1f}" for b in bids]],
    ["Exponential", *[f"{exp_score(b):.1f}" for b in bids]],
    ["Sigmoid", *[f"{sigmoid_score(b):.1f}" for b in bids]]
]

print("\nComparison Table:")
for row in data:
    print(f"{row[0]:<12} | {row[1]:>8} | {row[2]:>8} | {row[3]:>8} | {row[4]:>8} | {row[5]:>8}")