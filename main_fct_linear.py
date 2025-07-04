from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

from config_fct import ABS_MIN, ABS_MAX, SIGMOID_K_FCT, SIGMOID_X0_FCT
from bids_fct import competitors
from curves import linear_abs

def evaluate_linear_abs():
    # Marca temporal y carpeta de salida
    timestamp = datetime.now().strftime("%y%m%d-%H%M")
    out_dir = "output"
    os.makedirs(out_dir, exist_ok=True)
    
    # Calcular puntos de los trabajos y el totoal por concorrente
    results = []
    total_points = {}
    
    for comp in competitors:
        for work in comp.works:
            cost = work.cost
            score = linear_abs(cost)
            if cost < ABS_MIN:
                status = "ABAIXO"
            elif cost > ABS_MAX:
                status = "ACIMA"
            else:
                status = "-"
            results.append((comp.id, work.label, cost, score, status))
            total_points[comp.id] = total_points.get(comp.id, 0) + score
    
    # Build static header
    titulo_factor = "FACTOR 1. EDIFÍCIOS ESCOLARES"
    header = (
        f"{'Concorrente':<16}"
        f"{'Obra':<24}"
        f"{'Custo (€)':<18}"
        f"{'Pontuação':<14}"
        f"{'Status':<12}"
    )
    sep = "-" * len(header)
    
    # Print to console. REDUX. 
    print("\n" + titulo_factor)
    print("\n" + header)
    print(sep)
    for cid, label, cost, score, st in results:
        print(f"{cid:<16}"
              f"{label:<24}"
              f"{cost:<18,.2f}"
              f"{score:<14.4f}"
              f"{st:<12}")
      
    # Write to .txt
    txt_file = os.path.join(out_dir, f"{timestamp}_linearFCT.txt")
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(f"{titulo_factor}\n")
        f.write("EvaluaçãoLinear: P = 1 + (x - ABS_MIN)*(99/(ABS_MAX-ABS_MIN))\n")
        f.write(f"EvaluaçãoLinear: P = 1 + (CUSTO OBRA - {ABS_MIN})*(99/({ABS_MAX}-{ABS_MIN}))\n\n")
        f.write(header + "\n" + sep + "\n")
        last_cid = None
        for i, (cid, label, cost, score, st) in enumerate(results):
            if last_cid is not None and cid != last_cid:
                # Write total
                f.write(sep + "\n")
                f.write(f"{last_cid:<16}{'':<24}{'':<18}{total_points[last_cid]:<14.4f}{'':<12}\n")
                f.write(sep + "\n")
            f.write(f"{cid:<16}"
                    f"{label:<24}"
                    f"{cost:<18,.2f}"
                    f"{score:<14.4f}"
                    f"{st:<12}\n")
            last_cid = cid
        # Write last total
        if last_cid is not None:
            f.write(sep + "\n")
            f.write(f"{last_cid:<16}{'':<24}{'':<18}{total_points[last_cid]:<14.4f}{'':<12}\n")
            f.write(sep + "\n")
    
    print(f"\nTable saved to: {txt_file}")

    # Construir curva sigmoide & plot
    xs = np.linspace(ABS_MIN, ABS_MAX, 400)
    ys = [linear_abs(x) for x in xs]

    plt.figure(figsize=(16, 7))
    plt.plot(xs, ys, label="EvalLinear", color='blue', linewidth=1.5)
    
    # Create a color map (one color per competitor)
    cmap = plt.get_cmap('tab10')  # or 'tab20', etc.
    comp_ids = [comp.id for comp in competitors]
    color_map = {cid: cmap(i % cmap.N) for i, cid in enumerate(comp_ids)}
    
    # Marcar cada obra
    for cid, label, cost, score, st in results:
        color = color_map[cid]
        cost_l = f"{cost:,.2f}€".replace(",", "X").replace(".", ",").replace("X", ".")  # Format cost
        legend_label = f"{cid}-{label}-({cost_l})"
        if st == "-":   
            plt.scatter(cost, score, s=25, marker="o", color = color,
                    label=f"{legend_label} ({score:.2f})")
        elif st == "ABAIXO":
            plt.scatter(cost, score, s=30, marker="x", color=color,
                    label=f"{legend_label} ({st})")
        elif st == "ACIMA":
            plt.scatter(cost, score, s=25, marker="o", color=color,
                    label=f"{legend_label} ({st})")
    
    plt.xlabel("CUSTO OBRA (€)")
    plt.ylabel("PONTUAÇÃO (0–100)")
    plt.title("CURVA LINEAR PARA AVALIAÇÃO DE CONDIÇÕES TÉCNICAS", pad=20)
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
        return f"{x/1e6:.0f}M€"

    # Format tick labels in millions
    plt.xticks(ticks, [format_millions(t) for t in ticks], fontsize=9)

    # Set color for threshold labels
    ax = plt.gca()
    labels = ax.get_xticklabels()
    for i, t in enumerate(ticks):
        if t in (ABS_MIN, ABS_MAX):
            labels[i].set_color('red')
    ax.set_xticklabels(labels)
    
    plt.ylim(-5, 105) # Y axis with some "extra-room"
    plt.yticks(np.arange(0, 101, 10))  # Tick every 10 points
    plt.grid(True)

    """
    # Visulaización de ejes
    for spine in plt.gca().spines.values():
        spine.set_color('#cccccc')
        spine.set_linewidth(0.5)
    """
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
    png_file = os.path.join(out_dir, f"{timestamp}_linearFCT.png")
    plt.savefig(png_file, bbox_inches="tight")
    plt.close()
    print(f"Plot saved to: {png_file}\n")
    print("\n")

if __name__ == "__main__":
    evaluate_linear_abs()