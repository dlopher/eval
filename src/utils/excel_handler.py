import os
import pandas as pd
from typing import List
from src.models.bids_linear import Projeto, Disciplina, Factor, Concorrente
from src.models.bids_price import Bid
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

        # Read competitors file
        competitor_file = os.path.join(input_dir, f"{competitor_id}.xlsx")
        if not os.path.exists(competitor_file):
            print(f"Warning: No data file found for competitor {competitor_id}")
            continue

        factors = []
        # Read each factor sheet
        xl = pd.ExcelFile(competitor_file)

        for factor_id in FACTOR_STRUCTURE.keys():
            sheet_name = f"Factor_{factor_id}"
            if sheet_name not in xl.sheet_names:
                print(f"Warning: Sheet {sheet_name} not found for competitor {competitor_id}")
                continue
        
            df = pd.read_excel(competitor_file, sheet_name=sheet_name)

            # Group by disciplina
            disciplinas = []
            for disciplina_name, group in df.groupby("Disciplina"):
                # Filter out empty projects
                valid_projects = group[group["Projeto"].notna()]

                if factor_id == "A5":
                    # For A5: parse hours instead of cost, but re-use structure
                    formacoes = [
                        Formação(
                            name=row["Projeto"], #re-use column name using same logic
                            hours=float(row["Valor de obra"]) if pd.notna(row["Valor de obra"]) else 0.0,
                            observations=row["Observações"] if pd.notna(row["Observações"]) else "",
                            status=row["Status"] if pd.notna(row["Status"]) else ""
                        )
                        for _, row in valid_projects.iterrows()
                    ]
                    disciplinas.append(Disciplina(name=disciplina_name, formacoes=formacoes))
                else:
                    projetos = [
                        Projeto(
                            name=row["Projeto"],
                            cost=row["Valor de obra"],
                            observations=row["Observações"] if pd.notna(row["Observações"]) else "",
                            status=row["Status"] if pd.notna(row["Status"]) else ""
                        )
                        for _, row in valid_projects.iterrows()
                    ]

                    disciplinas.append(Disciplina(name=disciplina_name, projetos=projetos))

            factors.append(Factor(
                id=factor_id,
                name=FACTOR_STRUCTURE[factor_id]["name"],
                disciplinas=disciplinas
            ))

        competitors.append(Concorrente(id=competitor_id, factors=factors))
    
    return sorted(competitors, key=lambda x: x.id)

def read_bids_from_registry(input_dir: str = "data/input") -> List[Bid]:
    """
    Read bids from the competitors.xlsx registry file.
    Expects columns: ID, Nome, Preço
    Returns a list of src.models.bids_price.Bid
    """
    competitors_file = os.path.join(input_dir, "competitors.xlsx")
    if not os.path.exists(competitors_file):
        return []

    df = pd.read_excel(competitors_file)
    bids_list: List[Bid] = []
    
    for _, row in df.iterrows():
        # Skip rows without price
        price = row.get("Preço", None)
        if pd.isna(price) or price is None:
            continue
        try:
            bid_id = int(row["ID"])
            name = row.get("Nome", f"bid{bid_id}")
            bids_list.append(Bid(id=bid_id, name=str(name), price=float(price)))
        except Exception:
            # ignore malformed rows
            continue
    
    return bids_list