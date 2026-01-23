import os
import pandas as pd
from typing import List, Dict
from src.models.bids_linear import Projeto, Disciplina, Factor, Concorrente, Formação
from src.models.bids_price import Bid
from src.config.factor_structure import FACTOR_STRUCTURE
from src.config.config_linear import MAX_PROJECTS_PER_DISCIPLINA
from src.utils.date_validation import parse_date, validate_date


def validate_required_fields(row, factor_id: str) -> tuple:
    """
    Check if required fields are present based on factor_type.
    Returns: (is_valid, missing_fields_note)
    """
    factor_config = FACTOR_STRUCTURE[factor_id]

    required_always = ["Projeto", "Valor de obra"]

    required_conditional = []
    if factor_config.get("require_owner", False):
        required_conditional.append("Dono de obra")
    if factor_config.get("require_date", False):
        required_conditional.append("Data")
    
    required_fields = required_always + required_conditional
    missing = []

    for field in required_fields:
        value = row.get(field, None)
        if pd.isna(value) or str(value).strip() == "":
            missing.append(field)
    
    if missing:
        note = f"Faltam campos obrigatórios: {', '.join(missing)}"
        return False, note
    
    return True, ""

def read_excel_folder(input_dir: str = "data/input") -> List[Concorrente]:
    """Reads Excel files and creates Concorrente objects with factor-aware validation"""
    
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

        # Track project names across all factors to detect duplicates
        projeto_registry: Dict[str, tuple] = {} # {nome: (valor, factor-disciplina)} 

        factors = []
        # Read each factor sheet
        xl = pd.ExcelFile(competitor_file)

        for factor_id in FACTOR_STRUCTURE.keys():
            sheet_name = f"Factor_{factor_id}"
            if sheet_name not in xl.sheet_names:
                print(f"Warning: Sheet {sheet_name} not found for competitor {competitor_id}")
                continue
        
            df = pd.read_excel(competitor_file, sheet_name=sheet_name)
            factor_config = FACTOR_STRUCTURE[factor_id]
            require_date = factor_config.get("require_date", False)

            # Group by disciplina
            disciplinas = []
            for disciplina_name, group in df.groupby("Disciplina"):
                # Filter out empty projects
                valid_rows = group[group["Projeto"].notna()]

                if factor_id == "A5":
                    # For A5: parse hours instead of cost, re-use structure and no-limit on number of formações
                    formacoes = []
                    for _, row in valid_rows.iterrows():
                        # Check required fields
                        fields_valid, fields_note = validate_required_fields(row, factor_id)
                        if not fields_valid:
                            formacao = Formação(
                                name=row.get("Projeto", ""),
                                hours=0.0,
                                date=None,
                                observations=fields_note,
                                status="DESCL"
                            )
                            formacoes.append(formacao)
                            continue

                        # Parse date if provided
                        date_obj = None
                        date_obs = ""

                        has_date = pd.notna(row.get("Data", None))

                        if require_date and not has_date:
                            # Date is required but missing:
                            formacao = Formação(
                                name=row["Projeto"],
                                hours=float(row["Valor de obra"]),
                                date=None,
                                observations="sem data",
                                status="DESCL"
                            )
                            formacoes.append(formacao)
                            continue
                        
                        elif has_date:
                            # Date provided, try to parse it
                            date_obj, date_parse_valid, date_parse_note = parse_date(row.get("Data", None))
                            if not date_parse_valid:
                                # Date was provided but invalid format
                                formacao = Formação(
                                    name=row["Projeto"],
                                    hours=float(row["Valor de obra"]),
                                    date=None,
                                    observations=date_parse_note,
                                    status="DESCL"
                                )
                                formacoes.append(formacao)
                                continue
                            # Date is valid, validate age
                            is_valid, status, obs = validate_date(date_obj, item_type="formacao")
                            date_obs = obs
                        
                        # If we get here, all validations passed
                        formacao = Formação(
                            name=row["Projeto"],
                            hours=float(row["Valor de obra"]),
                            date=date_obj,
                            observations=date_obs,
                            status=""
                        )
                        formacoes.append(formacao)
                    
                    disciplinas.append(Disciplina(name=disciplina_name, formacoes=formacoes))
                
                else:
                    # A1-A4: Projetos with strict validation
                    projetos = []
                    for _, row in valid_rows.iterrows():
                        projeto_name = row.get("Projeto", "").strip()
                        
                        # 1. Check required fields (stricter for A1-A4)
                        fields_valid, fields_note = validate_required_fields(row, factor_id)
                        if not fields_valid:
                            projeto = Projeto(
                                name=projeto_name,
                                cost=0.0,
                                date=None,
                                observations=fields_note,
                                status="DESCL"
                            )
                            projetos.append(projeto)
                            continue
                        
                        # Parse and validate date
                        date_obj, date_parse_valid, date_parse_note = parse_date(row.get("Data", None))
                        
                        if not date_parse_valid:
                            projeto = Projeto(
                                name=projeto_name,
                                cost=float(row["Valor de obra"]) if pd.notna(row["Valor de obra"]) else 0.0,
                                date=None,
                                observations=date_parse_note,
                                status="DESCL"
                            )
                            projetos.append(projeto)
                            continue
                        
                        # Validate age
                        is_valid, age_status, age_obs = validate_date(date_obj, item_type="projeto")
                        
                        projeto_cost = float(row["Valor de obra"])
                        current_obs = age_obs
                        current_status = age_status
                        
                        # Check for duplicate names and value consistency
                        if projeto_name in projeto_registry:
                            registered_cost, registered_location = projeto_registry[projeto_name]
                            if registered_cost != projeto_cost:
                                current_obs = f"Mesmo projeto, valores diferentes: aplica-se valor de '{registered_location}' (€{registered_cost:,.2f})"
                                projeto_cost = registered_cost
                        else:
                            # Register this project's first occurrence
                            projeto_registry[projeto_name] = (projeto_cost, f"{factor_id}-{disciplina_name}")
                        
                        projeto = Projeto(
                            name=projeto_name,
                            cost=projeto_cost,
                            date=date_obj,
                            observations=current_obs,
                            status=current_status
                        )
                        projetos.append(projeto)
                    
                    # Enforce MAX_PROJECTS_PER_DISCIPLINA limit (only on non-disqualified)
                    non_descl = [p for p in projetos if p.status != "DESCL"]
                    descl = [p for p in projetos if p.status == "DESCL"]
                    
                    if len(non_descl) > MAX_PROJECTS_PER_DISCIPLINA:
                        print(f"Warning: Disciplina '{disciplina_name}' in factor {factor_id} has {len(non_descl)} valid projects. "
                              f"Keeping only first {MAX_PROJECTS_PER_DISCIPLINA}.")
                        projetos = non_descl[:MAX_PROJECTS_PER_DISCIPLINA] + descl
                    
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