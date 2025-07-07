import numpy as np
import matplotlib.pyplot as plt

# Reference price and boundaries
ref = 1053496.00
lower_bound = ref * 0.8    # -20% (€842,796.80)
upper_bound = ref * 1.2    # +20% (€1,264,195.20)
reward_threshold = ref * 0.9  # -10% (€948,146.40)

# Sigmoid-based scoring function
def sigmoid_based_score(price):
    # Sigmoid parameters
    k_lower = 0.000015  # Steepness for lower region
    k_upper = 0.00001   # Steepness for upper region
    
    # Prices below -20% (asymptotic to 100)
    if price <= lower_bound:
        return 100.0
    # Prices above +20% (asymptotic to 0)
    elif price >= upper_bound:
        return 0.0
    # Prices between -20% and -10%
    elif price <= reward_threshold:
        # Calculate center point between boundaries
        center = (lower_bound + reward_threshold) / 2
        # Sigmoid transition: 100 at -20%, 95 at -10%
        return 100 - 5 / (1 + np.exp(-k_lower * (price - center)))
    # Prices between -10% and reference
    elif price <= ref:
        # Linear reward: 95 at -10%, 80 at reference
        return 80 + 15 * (ref - price) / (ref - reward_threshold)
    # Prices above reference
    else:
        # Calculate center point between reference and upper bound
        center = (ref + upper_bound) / 2
        # Sigmoid penalty: 80 at reference, asymptotic to 0 at +20%
        return 80 / (1 + np.exp(k_upper * (price - center)))

# Test bids
bids = np.array([
    1053496.00,   # Reference
    1264000.00,   # +20% (upper bound)
    1000000.00,   # -5.08%
    800000.00,    # -24.05%
    1100000.00    # +4.41%
])

# Calculate scores
scores = [sigmoid_based_score(b) for b in bids]

# Generate curve
prices = np.linspace(700000, 1400000, 500)
curve_scores = [sigmoid_based_score(p) for p in prices]

# Create plot
plt.figure(figsize=(14, 8))
plt.plot(prices, curve_scores, 'b-', linewidth=2.5, label='Scoring Curve')
plt.scatter(bids, scores, c='red', s=100, zorder=5, label='Submitted Bids')

# Add critical boundaries
plt.axvline(ref, color='purple', ls='--', alpha=0.7, label=f'Reference (€{ref/1000:.0f}K)')
plt.axvline(reward_threshold, color='green', ls='--', alpha=0.7, label=f'-10% Threshold (€{reward_threshold/1000:.0f}K)')
plt.axvline(lower_bound, color='orange', ls='--', alpha=0.7, label=f'-20% Floor (€{lower_bound/1000:.0f}K)')
plt.axvline(upper_bound, color='red', ls='--', alpha=0.7, label=f'+20% Ceiling (€{upper_bound/1000:.0f}K)')

# Annotate bids
bid_labels = [
    f"1. Reference: €{bids[0]/1000:.0f}K → {scores[0]:.1f}",
    f"2. +20%: €{bids[1]/1000:.0f}K → {scores[1]:.1f}",
    f"3. -5.1%: €{bids[2]/1000:.0f}K → {scores[2]:.1f}",
    f"4. -24.1%: €{bids[3]/1000:.0f}K → {scores[3]:.1f}",
    f"5. +4.4%: €{bids[4]/1000:.0f}K → {scores[4]:.1f}"
]

for i, (bid, score, txt) in enumerate(zip(bids, scores, bid_labels)):
    plt.annotate(txt, (bid, score), 
                 (bid, score + 5 - 15*(i==3)),  # Adjust for Bid 4
                 ha='center',
                 fontsize=9,
                 arrowprops=dict(arrowstyle="->", color='gray'))

# Formatting
plt.title('Sigmoid-Based Asymmetric Scoring Curve', fontsize=16)
plt.xlabel('Price (€)', fontsize=12)
plt.ylabel('Score', fontsize=12)
plt.ylim(0, 110)
plt.xlim(700000, 1400000)
plt.grid(alpha=0.2)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('sigmoid_asymmetric_curve.png', dpi=300)
plt.show()

# Print scores
print("Bid Scores:")
for i, (bid, score) in enumerate(zip(bids, scores)):
    print(f"Bid {i+1}: €{bid:,.2f} → {score:.1f} points")