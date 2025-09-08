from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

from config_fct import FACTOR_THRESHOLDS, FACTOR_WEIGHTS, MAX_PROJECTS_PER_DISCIPLINA, MIN_SCORE_PER_PROJECT, MAX_SCORE_PER_PROJECT
from bids_fct_restelo import competitors
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
    
    concorrente_disciplina_scores = {}  # {cid: {fid: {did: sum}}}
    for comp in competitors:
        concorrente_disciplina_scores[comp.id] = {}
        for factor in comp.factors:
            concorrente_disciplina_scores[comp.id][factor.id] = {}
            for disciplina in factor.disciplinas:
                concorrente_disciplina_scores[comp.id][factor.id][disciplina.name] = 0.0

    for comp in competitors: 
        for factor in comp.factors:
            abs_min = FACTOR_THRESHOLDS[factor.id]["ABS_MIN"]
            abs_max = FACTOR_THRESHOLDS[factor.id]["ABS_MAX"]
            for disciplina in factor.disciplinas:
                disciplina_score = 0.0
                for projeto in disciplina.projetos:
                    cost = projeto.cost
                    # Check price threshold and status
                    if cost < abs_min or projeto.status:
                        score = 0
                        status = "DESCL" if projeto.status else "ABAIXO"
                    
                    elif cost > abs_max:
                        score = MAX_SCORE_PER_PROJECT
                        status = "ACIMA"
                    
                    else:
                        score = linear_abs(cost, abs_min, abs_max)
                        status = "-"
                    
                    results.append((
                        comp.id,
                        factor.id,
                        factor.name,
                        disciplina.name,
                        projeto.name,
                        cost,
                        score,
                        status,
                        projeto.observations
                    ))
                    concorrente_disciplina_scores[comp.id][factor.id][disciplina.name] += score
                    concorrente_factor_scores[comp.id][factor.id] += score
    
    concorrente_final_scores = {}
    for cid, factor_scores in concorrente_factor_scores.items():
        total = 0.0
        for fid in factor_ids:
            w = FACTOR_WEIGHTS[fid]
            Pk = factor_scores[fid]
            Pk_max = factor_max_score[fid]
            norm = Pk / Pk_max if Pk_max else 0
            total += w * norm
        concorrente_final_scores[cid] = round(total, 4)


    # Print to console. REDUX.
    titulo_factor = "FACTOR A. QUALIDADE DA EQUIPA TÉCNICA"
    print("\n" + titulo_factor + "\n")
    for cid, fid, factor, disciplina, projeto, cost, score, st, _ in results:
        print(f"{cid:<15}"
              f"{fid:<9}"
              f"{factor:<54}"
              f"{disciplina:<18}"
              f"{projeto:<76}"
              f"{cost:<21,.2f}"
              f"{score:<12.4f}"
              f"{st:<9}"
            )
      
    # Write to .txt
    txt_file = os.path.join(out_dir, f"{timestamp}_linearFCT.txt")
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(f"{titulo_factor}\n")
        f.write("EvaluaçãoLinearProjeto: P = MIN_SCORE_PER_PROJECT + ((ValorOBRA - ABS_MIN)*(MAX_SCORE_PER_PROJECT - MIN_SCORE_PER_PROJECT) / (ABS_MAX - ABS_MIN))\n\n")
        # f.write(f"EvaluaçãoLinearProjeto: P = {MIN_SCORE_PER_PROJECT} + (ValorOBRA - {ABS_MIN}) * (({MAX_SCORE_PER_PROJECT} - {MIN_SCORE_PER_PROJECT}) / ({ABS_MAX} - {ABS_MIN}))\n\n")
        header = (
            f"{'Concorrente':<15}"
            f"{'f.ID':<9}"
            f"{'Factor':<54}"
            f"{'Disciplina':<18}"
            f"{'Projeto':<76}"
            f"{'Custo (€)':<21}"
            f"{'Pontuação':<12}"
            f"{'Status':<9}"
            f"{'Observações':<36}"
        )
        sep = "-" * len(header)
        f.write(header + "\n" + sep + "\n")
        
        last_cid = None
        last_fid = None
        last_disciplina = None

        for row in results:
            cid,fid, factor, disciplina, projeto, cost, score, st, obs = row

            # When concorrente changes, print all previous totals
            if last_cid is not None and cid != last_cid:
                # Print last discipline subtotal
                f.write(f"{last_cid:<15}{last_fid:<9}{'':<54}{last_disciplina:<18}{'':<76}{'':<21}{concorrente_disciplina_scores[last_cid][last_fid][last_disciplina]:<12.4f}{'':<9}{'':<36}\n")
                f.write("\n")

                # Print last factor subtotal
                f.write(sep + "\n")
                f.write(f"{last_cid:<15}{last_fid:<9}{'SUBTOTAL':<54}{'':<18}{'':<76}{'':<21}{concorrente_factor_scores[last_cid][last_fid]:<12.4f}{'':<9}{'':<36}\n")
                
                # Print final total for this concorrente
                f.write(sep + "\n")
                f.write(f"{last_cid:<15}{'TOTAL':<9}{'*Pontuação do Factor A com ponderação por subfator':<54}{'':<18}{'':<76}{'':<21}{concorrente_final_scores[last_cid]:<12.4f}{'':<9}{'':<36}\n")
                f.write(sep + "\n")
                f.write("\n")
                f.write(sep + "\n")

            # When factor changes within same concorrente
            elif last_cid is not None and fid != last_fid:
                # Print last disciplina sub-total
                f.write(f"{last_cid:<15}{last_fid:<9}{'':<54}{last_disciplina:<18}{'':<76}{'':<21}{concorrente_disciplina_scores[last_cid][last_fid][last_disciplina]:<12.4f}{'':<9}{'':<36}\n")
                f.write("\n")

                # Print factor sub-total
                f.write(sep + "\n")
                f.write(f"{last_cid:<15}{last_fid:<9}{'SUBTOTAL':<54}{'':<18}{'':<76}{'':<21}{concorrente_factor_scores[last_cid][last_fid]:<12.4f}{'':<9}{'':<36}\n")
                f.write(sep + "\n")
            
            # When only disciplina changes
            elif last_disciplina is not None and disciplina != last_disciplina:
                f.write(f"{cid:<15}{fid:<9}{'':<54}{last_disciplina:<18}{'':<76}{'':<21}{concorrente_disciplina_scores[cid][fid][last_disciplina]:<12.4f}{'':<9}{'':<36}\n")
                f.write("\n")

            # Write current row
            f.write(f"{cid:<15}{fid:<9}{factor:<54}{disciplina:<18}{projeto:<76}{cost:<21,.2f}{score:<12.4f}{st:<9}{obs:<36}\n")
                
            last_cid = cid
            last_fid = fid
            last_disciplina = disciplina

        # Print final subtotals for last concorrente
        if last_cid is not None:
            # Print last discipline subtotal
            f.write(f"{last_cid:<15}{last_fid:<9}{'':<54}{last_disciplina:<18}{'':<76}{'':<21}{concorrente_disciplina_scores[last_cid][last_fid][last_disciplina]:<12.4f}{'':<9}{'':<36}\n")
            f.write("\n")

            # Print last factor subtotal
            f.write(sep + "\n")
            f.write(f"{last_cid:<15}{last_fid:<9}{'SUBTOTAL':<54}{'':<18}{'':<76}{'':<21}{concorrente_factor_scores[last_cid][last_fid]:<12.4f}{'':<9}{'':<36}\n")

            # Print final total for last concorrente
            f.write(sep + "\n")
            f.write(f"{last_cid:<15}{'TOTAL':<9}{'*Pontuação do Factor A com ponderação por subfator':<54}{'':<18}{'':<76}{'':<21}{concorrente_final_scores[last_cid]:<12.4f}{'':<9}{'':<36}\n")
            f.write(sep + "\n")
            f.write("\n")
            f.write(sep + "\n")

    print(f"\nTable saved to: {txt_file}")

"""
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
    
    # Visulaización de ejes
    # for spine in plt.gca().spines.values():
        # spine.set_color('#cccccc')
        # spine.set_linewidth(0.5)
    
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
"""

if __name__ == "__main__":
    evaluate_linear_abs()