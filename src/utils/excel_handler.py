import os
import pandas as pd
from typing import List
from src.models.bids_linear import Projeto, Disciplina, Factor, Concorrente
from src.config.factor_structure import FACTOR_STRUCTURE

def read_excel_folder(input_dir: str = "data/input") -> List[Concorrente]:
    """Reads Excel files and creates Concorrente objects"""
    
    # First read competitors entry
    competitors_file = os.path.join(input_dir, "competitors.xlsx")
    competitors_df = pd.read_excel(competitors_file)
    
    competitors = []
    for _, row in competitors_df.iterrows():
        competitor_id = row["ID"]
        competitor_name = row["Nome"]

        factors = []
        # Read each factor file
        for factor_id in FACTOR_STRUCTURE.keys():
            factor_file = os.path.join(input_dir, f"factor_{factor_id.lower()}.xlsx")
            factor_data = pd.read_excel(factor_file, sheet_name=None)
        
            disciplinas = []
            for disciplina_name, disciplina_df in factor_data.items():
                # Filter projects for this competitor
                competitors_projects = disciplina_df[disciplina_df["ID_Concorrente"] == competitor_id]

                projetos = [
                    Projeto(
                        name=row["Projeto"],
                        cost=row["Valor da obra"],
                        observations=row["Observações"] if pd.notna(row["Observações"]) else "",
                        status=row["Status"] if pd.notna(row["Status"]) else ""
                    )
                    for _, row in competitors_projects.iterrows()
                ]

                disciplinas.append(Disciplina(name=disciplina_name, projetos=projetos))

            factors.append(Factor(
                id=factor_id,
                name=FACTOR_STRUCTURE[factor_id]["name"],
                disciplinas=disciplinas
            ))

        competitors.append(Concorrente(id=competitor_id, factors=factors))

    return competitors