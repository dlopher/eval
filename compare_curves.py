import matplotlib.pyplot as plt
import numpy as np

from config import REF_PRICE, LOWER_THRESHOLD, UPPER_THRESHOLD
from bids import bids
from curves import linear, inverse_proportional, exponential, sigmoid

def compare_all():
    xs = np.linspace(LOWER_THRESHOLD * REF_PRICE * 0.95,
                     UPPER_THRESHOLD * REF_PRICE * 1.05, 400)

    plt.figure()
    plt.plot(xs, [linear(x) for x in xs], label="Linear")
    plt.plot(xs, [inverse_proportional(x) for x in xs], label="Inversa")
    plt.plot(xs, [exponential(x) for x in xs], label="Exponencial")
    plt.plot(xs, [sigmoid(x) for x in xs], label="Sigmoid")

    # Mark bids on each curve
    for curve_fn, name in [(linear, "Linear"),
                           (inverse_proportional, "Inversa"),
                           (exponential, "Exponencial"),
                           (sigmoid, "Sigmoid")]:
        for b in bids:
            plt.scatter(b.price, curve_fn(b.price), s=30)

    plt.xlabel("Preço (€)")
    plt.ylabel("Puntuação (0–100)")
    plt.title("Comparativa de Curvas de Puntuación")
    plt.legend()
    plt.grid(True)

    # Save to PNG instead of plt.show()
    plt.tight_layout()
    plt.savefig("compare_curves.png")
    plt.close()
    print("Plot saved as: compare_curves.png\n")

    # Also print the numeric table
    print("ID  Preço (€)  Linear   Inversa   Exponencial   Sigmoid")
    print("-------------------------------------------------------------")
    for b in bids:
        print(f"{b.id:<6} {b.price:>10,.2f}   "
              f"{linear(b.price):>6.1f}   "
              f"{inverse_proportional(b.price):>7.1f}   "
              f"{exponential(b.price):>11.1f}   "
              f"{sigmoid(b.price):>7.1f}")

if __name__ == "__main__":
    compare_all()