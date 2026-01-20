from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

from src.config.config_linear import FACTOR_THRESHOLDS, FACTOR_WEIGHTS, MAX_PROJECTS_PER_DISCIPLINA, MIN_SCORE_PER_PROJECT, MAX_SCORE_PER_PROJECT
from src.utils.curves import linear_abs
from src.utils.excel_handler import read_excel_folder

def evaluate_linear_abs(use_excel: bool = False, excel_dir: str = "data/input"):
    """
    Evaluate competitors using linear absolute scoring
    
    Args:
        use_excel: If True, read data from Excel files
        excel_dir: Directory containing Excel input files
    """
    if use_excel:
        competitors = read_excel_folder(excel_dir)
    else:
        from src.models.bids_linear_restelo import competitors
    
    # Marca temporal y carpeta de salida
    timestamp = datetime.now().strftime("%y%m%d-%H%M")
    out_dir = "data/output"
    os.makedirs(out_dir, exist_ok=True)
    
    # Calcular puntos de los trabajos
    results = []
    
    factor_ids = [factor.id for factor in competitors[0].factors]
    factor_disciplinas = {factor.id: len(factor.disciplinas) for factor in competitors[0].factors}
    factor_max_score = {}
    for fid in factor_disciplinas:
        if fid == "A5":
            # A5: only 1 disciplina ("formação BIM")
            factor_max_score[fid] = 1 * MAX_SCORE_PER_PROJECT
        else:
            # A1 to A4: limit by MAX_PROJECTS_PER_DISCIPLINA per disciplina
            factor_max_score[fid] = factor_disciplinas[fid] * MAX_PROJECTS_PER_DISCIPLINA * MAX_SCORE_PER_PROJECT
         
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
            for disciplina in factor.disciplinas:

                if factor.id == "A5":
                    # A5: Sum hours instead of evaluating projects individually
                    abs_min_max = FACTOR_THRESHOLDS[factor.id]["formação BIM"]
                    abs_min = abs_min_max["ABS_MIN"]
                    abs_max = abs_min_max["ABS_MAX"]
                    
                    # Filter out disqualified formações and sum valid hours
                    valid_formacoes = [f for f in disciplina.formacoes if not f.status]
                    total_hours = sum(f.hours for f in valid_formacoes)
                    num_valid = len(valid_formacoes)

                    if total_hours < abs_min:
                        score = 0
                        status = "ABAIXO"
                    elif total_hours > abs_max:
                        score = MAX_SCORE_PER_PROJECT
                        status = "ACIMA"
                    else:
                        score = linear_abs(total_hours, abs_min, abs_max)
                        status = "-"
                    
                    results.append((
                        comp.id,
                        factor.id,
                        factor.name,
                        disciplina.name,
                        f"{num_valid} formações válidas",  # show count of valid ones
                        total_hours,
                        score,
                        status,
                        ""
                    ))
                    concorrente_disciplina_scores[comp.id][factor.id][disciplina.name] += score
                    concorrente_factor_scores[comp.id][factor.id] += score

                else:
                    abs_min_max = FACTOR_THRESHOLDS[factor.id].get(
                    disciplina.name,
                    FACTOR_THRESHOLDS[factor.id]["default"]
                    )
                    abs_min = abs_min_max["ABS_MIN"]
                    abs_max = abs_min_max["ABS_MAX"]

                    disciplina_score = 0.0
                    for projeto in disciplina.projetos:
                        cost = projeto.cost
                        
                        # Check if project is disqualified
                        if projeto.status:
                            score = 0
                            status = "DESCL"
                        else:
                            # Evaluate price if project is not disqualified
                            cost = projeto.cost
                            if cost < abs_min:
                                score = 0
                                status = "ABAIXO"
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

if __name__ == "__main__":
    evaluate_linear_abs()