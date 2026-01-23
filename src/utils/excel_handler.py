import os
import pandas as pd
from typing import List
from src.models.bids_linear import Projeto, Disciplina, Factor, Concorrente, Formação
from src.models.bids_price import Bid
from src.config.factor_structure import FACTOR_STRUCTURE
from src.config.config_linear import MAX_PROJECTS_PER_DISCIPLINA
from src.utils.date_validation import parse_date, validate_date


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
                valid_rows = group[group["Projeto"].notna()]

                if factor_id == "A5":
                    # For A5: parse hours instead of cost, re-use structure and no-limit on number of formações
                    formacoes = []
                    for _, row in valid_rows.iterrows():
                        date_obj = parse_date(row.get("Data", None))
                        is_valid, status, obs = validate_date(date_obj, item_type="formacao")
                        
                        formacao = Formação(
                            name=row["Projeto"],
                            hours=float(row["Valor de obra"]) if pd.notna(row["Valor de obra"]) else 0.0,
                            date=date_obj,
                            observations=obs if obs else (row.get("Observações", "") or ""),
                            status=status
                        )
                        formacoes.append(formacao)
                    
                    disciplinas.append(Disciplina(name=disciplina_name, formacoes=formacoes))
                
                else:
                    projetos = []
                    for _, row in valid_rows.iterrows():
                        date_obj = parse_date(row.get("Data", None))
                        is_valid, status, obs = validate_date(date_obj, item_type="projeto")

                        if not is_valid:
                            status = "DESCL"
                        
                        projeto = Projeto(
                            name=row["Projeto"],
                            cost=row["Valor de obra"],
                            date=date_obj,
                            observations=obs if obs else (row.get("Observações", "") or ""),
                            status=status
                        )
                        projetos.append(projeto)
                    
                    # Keep only first MAX_PROJECTS_PER_DISCIPLINA projects
                    if len(projetos) > MAX_PROJECTS_PER_DISCIPLINA:
                        print(f"Warning: Disciplina '{disciplina_name}' in factor {factor_id} has {len(projetos)} projects. "
                              f"Keeping only first {MAX_PROJECTS_PER_DISCIPLINA}.")
                        projetos = projetos[:MAX_PROJECTS_PER_DISCIPLINA]
                    
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