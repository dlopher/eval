from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

from config_fct import FACTOR_THRESHOLDS, FACTOR_WEIGHTS, MAX_PROJECTS_PER_DISCIPLINA, MIN_SCORE_PER_PROJECT, MAX_SCORE_PER_PROJECT
from bids_fct import competitors
from curves import linear_abs

def evaluate_linear_abs():
    # Marca temporal y carpeta de salida
    timestamp = datetime.now().strftime("%y%m%d-%H%M")
    out_dir = "output"
    os.makedirs(out_dir, exist_ok=True)
    
    # Calcular puntos de los trabajos
    results = []
    
    factor_ids = [factor.id for factor in competitors[0].factors]
    factor_disciplinas = {factor.id: len(factor.disciplinas) for factor in competitors[0].factors}
    factor_max_score = {
        fid: factor_disciplinas[fid] * MAX_PROJECTS_PER_DISCIPLINA * MAX_SCORE_PER_PROJECT
        for fid in factor_disciplinas
        }
    concorrente_factor_scores = {}  # {cid: {fid: sum}}

    for comp in competitors:
        concorrente_factor_scores[comp.id] = {fid: 0.0 for fid in factor_ids}
        for factor in comp.factors:
            abs_min = FACTOR_THRESHOLDS[factor.id]["ABS_MIN"]
            abs_max = FACTOR_THRESHOLDS[factor.id]["ABS_MAX"]
            for disciplina in factor.disciplinas:
                for projeto in disciplina.projetos:
                    cost = projeto.cost
                    score = linear_abs(cost, abs_min, abs_max)
                    if cost < abs_min:
                        status = "ABAIXO"
                    elif cost > abs_max:
                        status = "ACIMA"
                    else:
                        status = "-"
                    results.append((
                        comp.id,
                        factor.id,
                        factor.name,
                        disciplina.name,
                        projeto.name,
                        cost,
                        score,
                        status
                    ))
                    concorrente_factor_scores[comp.id][factor.id] += score
                    # (old--just concorrente) total_points[comp.id] = total_points.get(comp.id, 0) + score
    
    concorrente_final_scores = {}
    for cid, factor_scores in concorrente_factor_scores.items():
        total=0.0
        for fid in factor_ids:
            w = FACTOR_WEIGHTS[fid]
            Pk = factor_scores[fid]
            Pk_max = factor_max_score[fid]
            norm = Pk / Pk_max if Pk_max else 0
            total += w * norm
        concorrente_final_scores[cid] = round(10 * total / 100, 4)


    # Build static header
    titulo_factor = "FACTOR A. QUALIDADE DA EQUIPA TÉCNICA"
    header = (
        f"{'Concorrente':<15}"
        f"{'f.ID':<9}"
        f"{'Factor':<60}"
        f"{'Disciplina':<18}"
        f"{'Projeto':<36}"
        f"{'Custo (€)':<21}"
        f"{'Pontuação':<12}"
        f"{'Status':<9}"
    )
    sep = "-" * len(header)
    
    # Print to console. REDUX. 
    print("\n" + titulo_factor)
    print("\n" + header)
    print(sep)
    for cid, fid, factor, disciplina, projeto, cost, score, st in results:
        print(f"{cid:<15}"
              f"{fid:<9}"
              f"{factor:<60}"
              f"{disciplina:<18}"
              f"{projeto:<36}"
              f"{cost:<21,.2f}"
              f"{score:<12.4f}"
              f"{st:<9}")
      
    # Write to .txt
    txt_file = os.path.join(out_dir, f"{timestamp}_linearFCT.txt")
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(f"{titulo_factor}\n")
        f.write("EvaluaçãoLinearProjeto: P = MIN_SCORE_PER_PROJECT + (ValorOBRA - ABS_MIN)*(MAX_SCORE_PER_PROJECT - MIN_SCORE_PER_PROJECT / (ABS_MAX - ABS_MIN))\n\n")
        # f.write(f"EvaluaçãoLinearProjeto: P = {MIN_SCORE_PER_PROJECT} + (ValorOBRA - {ABS_MIN}) * (({MAX_SCORE_PER_PROJECT} - {MIN_SCORE_PER_PROJECT}) / ({ABS_MAX} - {ABS_MIN}))\n\n")
        f.write(header + "\n" + sep + "\n")
        last_cid = None
        for row in results:
            cid,fid, factor, disciplina, projeto, cost, score, st = row
            if last_cid is not None and cid != last_cid:
                # Write per-factor sub-totals
                f.write(sep + "\n")
                for sub_fid in factor_disciplinas:
                    f.write(f"{last_cid:<15}{sub_fid:<9}{'':<60}{'':<18}{'':<36}{'':<21}{concorrente_factor_scores[last_cid][sub_fid]:<12.4f}{'':<9}\n")
                # Write total
                f.write(sep + "\n")
                f.write(f"{last_cid:<15}{'':<9}{'Pontuação Final':<60}{'':<18}{'':<36}{'':<21}{concorrente_final_scores[last_cid]:<12.4f}{'':<9}\n")
                f.write(sep + "\n")
            f.write(f"{cid:<15}"
                    f"{fid:<9}"
                    f"{factor:<60}"
                    f"{disciplina:<18}"
                    f"{projeto:<36}"
                    f"{cost:<21,.2f}"
                    f"{score:<12.4f}"
                    f"{st:<9}\n")
            last_cid = cid
        # Write last total
        if last_cid is not None:
            f.write(sep + "\n")
            for sub_fid in factor_disciplinas:
                f.write(f"{last_cid:<15}{sub_fid:<9}{'':<60}{'':<18}{'':<36}{'':<21}{concorrente_factor_scores[last_cid][sub_fid]:<12.4f}{'':<9}\n")
            f.write(sep + "\n")
            f.write(f"{last_cid:<15}{'':<9}{'':<60}{'':<18}{'':<36}{'':<21}{concorrente_final_scores[last_cid]:<12.4f}{'':<9}\n")
            f.write(sep + "\n")
    
    print(f"\nTable saved to: {txt_file}")

    # Construir curva (un color pro subfactor) & plot
    unique_thresholds = {}
    for fid in factor_ids:
        pair = (FACTOR_THRESHOLDS[fid]["ABS_MIN"], FACTOR_THRESHOLDS[fid]["ABS_MAX"])
        unique_thresholds[pair] = unique_thresholds.get(pair, []) + [fid]
    
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'cyan', 'magenta', 'brown']
    subfactor_names = []
    plt.figure(figsize=(16, 7))
    
    for i, ((abs_min, abs_max), fids) in enumerate(unique_thresholds.items()):
        xs = np.linspace(abs_min, abs_max, 400)
        ys = [linear_abs(x, abs_min, abs_max) for x in xs]
        label = " / ".join(fids) + f" (MIN={abs_min/1e6:.1f}M, MAX={abs_max/1e6:.1f}M)"
        subfactor_names.extend(fids)
        plt.plot(xs, ys, label=label, color=colors[i % len(colors)], linewidth=1.5)

    # Color map por concorrente
    cmap = plt.get_cmap('tab10')  # or 'tab20', etc.
    comp_ids = [comp.id for comp in competitors] 
    color_map = {cid: cmap(i % cmap.N) for i, cid in enumerate(comp_ids)}
    
    # Marcar cada obra
    for cid, fid, factor, disciplina, projeto, cost, score, st in results:
        color = color_map[cid]
        cost_l = f"{cost:,.2f}€".replace(",", "X").replace(".", ",").replace("X", ".")  # Format cost
        legend_label = f"{cid}-{fid}-{disciplina}{projeto}-({cost_l})"
        if st == "-":
            plt.scatter(cost, score, s=25, marker="o", color=color,
                    label=f"{legend_label} ({score:.2f})")
        elif st == "ABAIXO":
            plt.scatter(cost, score, s=30, marker="x", color=color,
                    label=f"{legend_label} ({st})")
        elif st == "ACIMA":
            plt.scatter(cost, score, s=25, marker="o", color=color,
                    label=f"{legend_label} ({st})")
    
    plt.xlabel("CUSTO OBRA (€)")
    plt.ylabel("PONTUAÇÃO (0–100)")
    subfactor_str = ", ".join(subfactor_names)
    plt.title(f"CURVA LINEAR PARA AVALIAÇÃO DE CONDIÇÕES TÉCNICAS — Subfactores: {subfactor_str}", pad=20)
    # plt.xlim(ABS_MIN, ABS_MAX)  # X axis from 0 to max --- old version
    
    # WORK ON X-AXIS DYNAMICALLY
    costs = [cost for _, _, _, _, _, cost, _, _ in results]

    # include both the absolute thresholds for all factors and any actual bid extremes
    all_abs_mins = {FACTOR_THRESHOLDS[fid]["ABS_MIN"] for fid in factor_ids}
    all_abs_maxs = {FACTOR_THRESHOLDS[fid]["ABS_MAX"] for fid in factor_ids}
    all_thresholds = sorted(all_abs_mins | all_abs_maxs)

    raw_min = min(costs + list(all_abs_mins))
    raw_max = max(costs + list(all_abs_maxs))

    # add a 5% margin on each side
    x_min = raw_min - 0.05 * (raw_max - raw_min)
    x_max = raw_max + 0.05 * (raw_max - raw_min)

    plt.xlim(x_min, x_max)

    # --- Mark thresholds explicitly on the x‑axis ---
    ticks = list(plt.xticks()[0])  # existing ticks
    # add ABS_MIN & ABS_MAX if they're not already in the list
    for t in all_thresholds:
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
        if t in all_thresholds:
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
        bbox_to_anchor=(0, -1, 1, 1),
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