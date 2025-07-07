import numpy as np
import matplotlib.pyplot as plt

# Reference price and boundaries
ref = 1053496.00
lower_bound = ref * 0.8    # -20%
upper_bound = ref * 1.2    # +20%
reward_threshold = ref * 0.9  # -10%

# Custom scoring function
def calculate_score(price):
    # Prices above upper bound
    if price >= upper_bound:
        return 0.0
        
    # Prices between reference and upper bound
    elif price >= ref:
        return 100 * np.exp(-3.0 * (price - ref) / (upper_bound - ref))
        
    # Prices between reward threshold and reference
    elif price >= reward_threshold:
        return 80 + 20 * (ref - price) / (ref - reward_threshold)
        
    # Prices between lower bound and reward threshold
    elif price >= lower_bound:
        return 95 + 5 * (1 - np.exp(-10 * (price - lower_bound) / (reward_threshold - lower_bound)))
        
    # Prices below lower bound (flat)
    else:
        return 100.0

# Test bids
bids = [
    1053496.00,   # Reference
    1264000.00,   # +20% (upper bound)
    1000000.00,   # -5.08%
    800000.00,    # -24.05%
    1100000.00    # +4.41%
]

# Calculate scores
scores = [calculate_score(bid) for bid in bids]

# Generate curve
prices = np.linspace(700000, 1400000, 500)
curve_scores = [calculate_score(p) for p in prices]

# Plot
plt.figure(figsize=(14, 8))
plt.plot(prices, curve_scores, 'b-', linewidth=2.5, label='Scoring Curve')
plt.scatter(bids, scores, c='red', s=100, zorder=5, label='Submitted Bids')

# Add reference lines
plt.axvline(ref, color='purple', linestyle='--', alpha=0.7, label=f'Reference (€{ref/1000:.0f}K)')
plt.axvline(reward_threshold, color='green', linestyle='--', alpha=0.7, label=f'-10% Threshold (€{reward_threshold/1000:.0f}K)')
plt.axvline(lower_bound, color='orange', linestyle='--', alpha=0.7, label=f'-20% Boundary (€{lower_bound/1000:.0f}K)')
plt.axvline(upper_bound, color='red', linestyle='--', alpha=0.7, label=f'+20% Boundary (€{upper_bound/1000:.0f}K)')

# Annotate bids
bid_labels = [
    f"1. Reference: €{bids[0]/1000:.0f}K → {scores[0]:.1f} pts",
    f"2. +20%: €{bids[1]/1000:.0f}K → {scores[1]:.1f} pts",
    f"3. -5.1%: €{bids[2]/1000:.0f}K → {scores[2]:.1f} pts",
    f"4. -24.1%: €{bids[3]/1000:.0f}K → {scores[3]:.1f} pts",
    f"5. +4.4%: €{bids[4]/1000:.0f}K → {scores[4]:.1f} pts"
]
for i, (bid, score) in enumerate(zip(bids, scores)):
    plt.annotate(bid_labels[i], (bid, score), 
                 (bid, score + 5), 
                 ha='center', 
                 fontsize=9,
                 arrowprops=dict(arrowstyle="->", color='gray'))

# Formatting
plt.title('Asymmetric Price Scoring Curve', fontsize=16)
plt.xlabel('Price (€)', fontsize=12)
plt.ylabel('Score', fontsize=12)
plt.ylim(-5, 110)
plt.xlim(700000, 1400000)
plt.grid(alpha=0.2)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('asymmetric_scoring_curve.png', dpi=300)
print("Scores for test bids:")
for i, (bid, score) in enumerate(zip(bids, scores)):
    print(f"Bid {i+1}: €{bid:,.2f} → {score:.1f} points")