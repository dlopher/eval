import os
import pandas as pd
from src.config.factor_structure import FACTOR_STRUCTURE

def create_excel_templates(output_dir: str = "data/input"):
    """Creates Excel template files for each factor with their respective disciplines."""

    # Create output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Creates competitors registrty
    competitors_df = pd.DataFrame(columns=["ID", "Nome"])
    competitors_file = os.path.join(output_dir, "competitors.xlsx")
    competitors_df.to_excel(competitors_file, index=False)
    print(f"Created competitors registry: {competitors_file}")


    # Create empty DataFrame with required columns
    columns = ["ID_Concorrente", "Projeto", "Dono de obra", "Data", "Valor da obra", "Status", "Observações"]
    df = pd.DataFrame(columns=columns)

    # Create an Excel file for each factor
    for factor_id, factor_info in FACTOR_STRUCTURE.items():
        filename = os.path.join(output_dir, f"factor_{factor_id.lower()}.xlsx")

        # Create multiples sheets in each factor file, one per disciplina.
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for disciplina in factor_info["disciplinas"]:
                df.to_excel(writer, sheet_name=disciplina, index=False)
        
        print(f"Created template: {filename}")

if __name__ == "__main__":
    create_excel_templates()