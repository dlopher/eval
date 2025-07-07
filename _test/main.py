import numpy as np
import matplotlib
# Use non-interactive backend
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Parameters
x = np.linspace(80, 220, 500)
x_min, x_max = 100, 200
y_max = 100
x_best = x_min  # Lowest bid for inverse
k_exp = 2       # Exponent for exponential
k_sig = 0.06    # Steepness for sigmoid
x_target = 150  # For sigmoid

# 1. Linear
y_linear = y_max * (x_max - x) / (x_max - x_min)

# 2. Inverse Proportional
y_inverse = y_max * (x_best / x)

# 3. Exponential
base = np.clip((x_max - x) / (x_max - x_min), 0, 1)
y_exp = y_max * base**k_exp

# 4. Sigmoid (decreasing function)
y_sig = y_max * (1 - 1/(1 + np.exp(-k_sig * (x - x_target))))

# Create plot
plt.figure(figsize=(12, 7))
plt.plot(x, y_linear, label='Linear', lw=2)
plt.plot(x, y_inverse, label='Inverse Proportional', lw=2)
plt.plot(x, y_exp, label=f'Exponential (k={k_exp})', lw=2)
plt.plot(x, y_sig, label=f'Sigmoid (k={k_sig}, target=${x_target})', lw=2)

# Add reference lines
plt.axvline(x_min, color='gray', ls='--', alpha=0.7, label=f'Min price (${x_min})')
plt.axvline(x_max, color='black', ls='--', alpha=0.7, label=f'Max price (${x_max})')
plt.axhline(y_max, color='red', ls=':', alpha=0.5, label=f'Max score ({y_max})')

# Formatting
plt.ylim(-10, 130)
plt.xlabel("Price Offered ($x$)")
plt.ylabel("Score ($y$)")
plt.title("Price Scoring Curves Comparison")
plt.legend(loc='upper right')
plt.grid(alpha=0.2)

# Save to file
plt.savefig('price_scoring_curves.png', bbox_inches='tight')
print("Plot saved as 'price_scoring_curves.png'")