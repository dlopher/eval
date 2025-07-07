from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

from config_fct import ABS_MIN, ABS_MAX, SIGMOID_K_FCT, SIGMOID_X0_FCT
from bids_fct import competitors
from curves import sigmoid_abs

def evaluate_sigmoid_fct():
    # Marca temporal y carpeta de salida
    timestamp = datetime.now().strftime("%y%m%d-%H%M")
    out_dir = "output"
    os.makedirs(out_dir, exist_ok=True)
    
    # Calcular puntos de los trabajos
    results = []
    for comp in competitors:
        for work in comp.works:
            cost = work.cost
            score = sigmoid_abs(cost)
            if cost < ABS_MIN:
                status = "ABAIXO"
            elif cost > ABS_MAX:
                status = "ACIMA"
            else:
                status = "-"
            results.append((comp.id, work.label, cost, score, status))
    
    # Build static header
    header = (
        f"{'CompID':<6} "
        f"{'Work':<12} "
        f"{'Custo (€)':>12}   "
        f"{'Pontos Sigmoid':>14}   "
        f"{'Status':>12}"
    )
    sep = "-" * len(header)
    
    # Print to console
    print("\n" + header)
    print(sep)
    for cid, label, cost, score, st in results:
        print(f"{cid:<6} "
              f"{label:<12} "
              f"{cost:>12,.2f}   "
              f"{score:>14.4f}   "
              f"{st:>12}")
      
    # Write to .txt
    txt_file = os.path.join(out_dir, f"{timestamp}_sigmoidFCT.txt")
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(f"CurvaSigmoideAbs: Pont = 1 / (1 + e^(k * (x - x0)))\n")
        #   Pont = 1 / (1 + exp(k*(x - x0)))
        f.write(f"k = {SIGMOID_K_FCT:.4f}, x0 = {SIGMOID_X0_FCT:.4f}\n\n")
        f.write(header + "\n" + sep + "\n")
        for cid, label, cost, score, st in results:
            f.write(f"{cid:<6} "
                    f"{label:<12} "
                    f"{cost:>12,.2f}   "
                    f"{score:>14.4f}   "
                    f"{st:>12}\n")
    print(f"\nTable saved to: {txt_file}")

    # Construir curva sigmoide & plot
    xs = np.linspace(ABS_MIN, ABS_MAX, 400)
    ys = [sigmoid_abs(x) for x in xs]

    plt.figure(figsize=(16, 7))
    plt.plot(xs, ys, label="CurvaEvalSigmoideFCT", color='blue', linewidth=1.5)
    
    # marcar cada obra
    for cid, label, cost, score, st in results:
        if st == "-":   
            plt.scatter(cost, score, s=25, marker="o",
                        label=f"{cid}-{label} ({score:.1f})")
        else:
            plt.scatter(cost, score, s=30, marker="x", color="red",
                        label=f"{cid}-{label} ({st})")
    
    plt.xlabel("CUSTO (€)")
    plt.ylabel("PONTUAÇÃO (0–100)")
    plt.title("CURVA SIGMOIDE DE AVAILAÇÃO DE CONDIÇÕES TÉCNICAS", pad=40)
    # plt.xlim(ABS_MIN, ABS_MAX)  # X axis from 0 to max --- old version
    
    # WORK ON X-AXIS DYNAMICALLY
    costs = [cost for _, _, cost, _, _ in results]

    # include both the absolute thresholds and any actual bid extremes
    raw_min = min(costs + [ABS_MIN])
    raw_max = max(costs + [ABS_MAX])

    # add a 5% margin on each side
    x_min = raw_min - 0.05 * (raw_max - raw_min)
    x_max = raw_max + 0.05 * (raw_max - raw_min)

    plt.xlim(x_min, x_max)

    # --- Mark thresholds explicitly on the x‑axis ---
    ticks = list(plt.xticks()[0])  # existing ticks
    # add ABS_MIN & ABS_MAX if they're not already in the list
    for t in (ABS_MIN, ABS_MAX):
        if t < x_min or t > x_max:
            continue
        if not any(abs(t - existing) < 1e-8 for existing in ticks):
            ticks.append(t)
    ticks = sorted(ticks)
    
    def format_millions(x):
        return f"{x/1e6:.2f}e6"

    # Format tick labels in millions
    plt.xticks(ticks, [format_millions(t) for t in ticks], fontsize=9)

    # Set color for threshold labels
    ax = plt.gca()
    labels = ax.get_xticklabels()
    for i, t in enumerate(ticks):
        if t in (ABS_MIN, ABS_MAX):
            labels[i].set_color('red')
    ax.set_xticklabels(labels)
    
    plt.ylim(0, 100) # Y axis from 0 to 100
    plt.yticks(np.arange(0, 101, 10))  # Tick every 10 points
    plt.grid(True)

    """
    # Visulaización de ejes
    for spine in plt.gca().spines.values():
        spine.set_color('#cccccc')
        spine.set_linewidth(0.5)
    """
    # Formula + constants
    plt.figtext(
        0.53, 0.92,
        "CurvaSigmoideAbs: Pont = 1 / (1 + e^(k * (x - x0)))\n"
        f"k = {SIGMOID_K_FCT:.4f}, x0 = {SIGMOID_X0_FCT:.4f}",
        ha="center", fontsize=9
    )

    # Leyenda
    plt.tight_layout()
    plt.legend(
        loc='lower left',
        bbox_to_anchor=(0, -0.40, 1, 1),
        # mode="expand",
        ncol=1,
        borderaxespad=0,
        frameon=False,
    )

    # Save to PNG
    png_file = os.path.join(out_dir, f"{timestamp}_sigmoidFCT.png")
    plt.savefig(png_file, bbox_inches="tight")
    plt.close()
    print(f"Plot saved to: {png_file}\n")
    print("\n")

if __name__ == "__main__":
    evaluate_sigmoid_fct()