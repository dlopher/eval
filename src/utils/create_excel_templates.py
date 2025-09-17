import os
import pandas as pd
from src.config.factor_structure import FACTOR_STRUCTURE
from src.config.config_linear import MAX_PROJECTS_PER_DISCIPLINA


def create_competitor_template(competitor_id: int, output_dir: str):
    """Creates Excel template file for a single competitor with all factors as sheets"""
    filename = os.path.join(output_dir, f"{competitor_id}.xlsx")

    # Create empty DataFrame with required columns
    base_columns = ["Disciplina", "Projeto", "Dono de obra", "Data", "Valor da obra", "Status", "Observações"]

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Create a sheet for each factor
        for factor_id, factor_info in FACTOR_STRUCTURE.items():
            # Create rows for each disciplina, repeated MAX_PROJECTS_PER_DISCIPLINA times
            rows = []
            for disciplina in factor_info["disciplinas"]:
                for _ in range(MAX_PROJECTS_PER_DISCIPLINA):
                    rows.append([disciplina, "", "", "", "", "", ""])
            
            df = pd.DataFrame(rows, columns=base_columns)
            df.to_excel(writer, sheet_name=f"Factor_{factor_id}", index=False)
    
    return filename


def create_excel_templates(output_dir: str = "data/input"):
    """Creates Excel template files for each competitor."""

    # Create output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Check for existing competitors registry
    competitors_file = os.path.join(output_dir, "competitors.xlsx")

    if os.path.exists(competitors_file):
        # Read existing competitors and create template for each
        competitors_df = pd.read_excel(competitors_file)
        for _, row in competitors_df.iterrows():
            competitor_id = row["ID"]
            template_file = create_competitor_template(competitor_id, output_dir)
            print(f"Created template for competitor {competitor_id}: {template_file}")
    else:
        # Create empty competitors registry and single-base-template
        competitors_df = pd.DataFrame(columns=["ID", "Nome"])
        competitors_df.to_excel(competitors_file, index=False)
        print(f"Created competitors registry: {competitors_file}")

        template_file = create_competitor_template(1, output_dir)
        print(f"Created template: {template_file}")


if __name__ == "__main__":
    create_excel_templates()