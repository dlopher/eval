import os
from typing import Dict, List
from src.utils.pdf_handler import read_pdf_folder, transform_pdf_data, normalize_text
# from src.utils.pdf_handler import debug_pdf_tables
from src.config.config_team import COLUMNS, FILE_MAPPING, PDF_FOLDER, ESPECIALIDADES


def validate_estrutura(structured_data: Dict) -> Dict:
    """
    Validate that all identifiers have expected especialidades.
    Normalizes text to avoid punctuation/accent mismatches.
    Uses same matching logic as check_light_repetitions.
    Returns {identifier: status, missing, extra}.
    """
    validation = {}
    expected_normalized = {normalize_text(esp): esp for esp in ESPECIALIDADES}  # Map normalized → original
    
    for identifier_key, especialidades in structured_data.items():
        missing = set()
        extra = set()
        matched_keys = set()
        
        # Check each actual especialidade against expected ones
        for esp_actual in especialidades.keys():
            esp_normalized = normalize_text(esp_actual)
            
            if esp_normalized in expected_normalized:
                # Found a match - mark as matched
                matched_keys.add(esp_normalized)
            else:
                # No normalized match found - this is truly EXTRA
                extra.add(esp_actual)
        
        # Find missing especialidades (expected but not found)
        missing = set(expected_normalized.keys()) - matched_keys
        
        status = "OK" if missing == set() and extra == set() else "MISMATCH"
        
        validation[identifier_key] = {
            "status": status,
            "missing": list(missing),  # Normalized
            "extra": list(extra),  # Original text (true extras only)
            "actual_keys": list(especialidades.keys())  # Keep original for debugging
        }
    
    return validation


def check_light_repetitions(structured_data: Dict) -> Dict:
    """
    Light comparison: check repeated professional numbers in same especialidade
    across different identifiers. Uses normalized especialidade names.
    """
    repetitions = {}
    expected_normalized = set(normalize_text(esp) for esp in ESPECIALIDADES)
    
    for esp_expected in ESPECIALIDADES:
        esp_normalized = normalize_text(esp_expected)
        numeros_by_id = {}
        
        for identifier_key, especialidades in structured_data.items():
            # Find matching especialidade (accounting for typos/normalization)
            matching_esp = None
            for esp_actual in especialidades.keys():
                if normalize_text(esp_actual) == esp_normalized:
                    matching_esp = esp_actual
                    break
            
            if matching_esp:
                # Filter out empty numbers
                numeros = [n for n in especialidades[matching_esp]["numero_ordem_profissional"] if n.strip()]
                if numeros:  # Only store if there are non-empty numbers
                    numeros_by_id[identifier_key] = numeros
        
        # Find duplicates across identifiers for this especialidade
        all_numeros = {}
        for identifier_key, numeros in numeros_by_id.items():
            for numero in numeros:
                if numero not in all_numeros:
                    all_numeros[numero] = []
                all_numeros[numero].append(identifier_key)
        
        # Find numbers appearing in multiple identifiers
        duplicates = {num: ids for num, ids in all_numeros.items() if len(ids) > 1}
        if duplicates:
            repetitions[esp_expected] = duplicates  # Use original name for display
    
    return repetitions


def check_hard_repetitions(structured_data: Dict) -> Dict:
    """
    Hard comparison: check if any professional number appears in multiple IDENTIFIERS,
    regardless of especialidade. Ignores empty/invalid numbers and same number in same identifier.
    Uses ALL especialidades (including "EXTRA" ones)
    No filtering by validation status
    """
    all_numeros = {}
    total_numeros_collected = 0
    
    for identifier_key, especialidades in structured_data.items():
        for esp_actual, data in especialidades.items():
            # Filter out empty numbers
            numeros = [n for n in data["numero_ordem_profissional"] if n.strip()]
            total_numeros_collected += len(numeros)

            for numero in numeros:
                if numero not in all_numeros:
                    all_numeros[numero] = []
                all_numeros[numero].append({
                    "identifier": identifier_key,
                    "especialidade": esp_actual
                })
    
    # Find numbers appearing in MULTIPLE IDENTIFIERS
    repetitions = {}
    for num, occurrences in all_numeros.items():
        unique_identifiers = set(occ["identifier"] for occ in occurrences)
        if len(unique_identifiers) > 1:
            repetitions[num] = occurrences
    
    print(f"\n[DEBUG] COMPARATIVA DURA: Collected {total_numeros_collected} total numbers")  # DEBUG
    print(f"[DEBUG] COMPARATIVA DURA: Found {len(repetitions)} duplicates across identifiers\n")  # DEBUG
    return repetitions


def print_structured_data_table(structured_data: Dict, validation: Dict):
    """
    Print detailed table showing what data will be used in repetition checks.
    Marks especialidades that don't match predefined list.
    """
    print("\n" + "="*100)
    print("DATA EXTRACTION SUMMARY - What will be compared for repetitions")
    print("="*100)
    
    for identifier_key in sorted(structured_data.keys()):
        especialidades = structured_data[identifier_key]
        val_info = validation[identifier_key]
        
        print(f"\n{identifier_key}:")
        print(f"  {'ESPECIALIDADE (PDF)':<60} | {'NOME':<20} | {'ORDEM Nº':<12} | Status")
        print(f"  {'-'*60}-+-{'-'*20}-+-{'-'*12}-+--------")
        
        for esp_actual, data in especialidades.items():
            nomes = data.get("nome", [])
            numeros = data.get("numero_ordem_profissional", [])
            
            # Check if this especialidade is in predefined list
            esp_normalized = normalize_text(esp_actual)
            is_predefined = any(normalize_text(e) == esp_normalized for e in ESPECIALIDADES)
            status_mark = "✓" if is_predefined else "⚠ EXTRA"
            
            # Handle multiple names/numbers per row
            for i, (nome, numero) in enumerate(zip(nomes, numeros)):
                nome_short = nome[:20] if nome else ""
                numero_clean = numero.strip() if numero else ""
                
                if i == 0:
                    print(f"  {esp_actual:<60} | {nome_short:<20} | {numero_clean:<12} | {status_mark}")
                else:
                    print(f"  {'(cont.)':<60} | {nome_short:<20} | {numero_clean:<12} |")
    
    print("\n" + "="*100 + "\n")


def print_validation_report(light_reps: Dict, hard_reps: Dict):
    """Print repetition report (validation now shown in data table)"""
    
    print("\n" + "="*60)
    print("REPETITION CHECKS")
    print("="*60)
    
    # 1. Light repetitions
    print("\n1. COMPARATIVA BRANDA (o número de ordem aparece na MESMA especialidade em varios concorrentes):")
    if light_reps:
        for especialidade, duplicates in light_reps.items():
            print(f"\n  {especialidade}:")
            for numero, identifiers in duplicates.items():
                print(f"    Nº {numero}: {', '.join(identifiers)}")
    else:
        print("  ✓ Sem duplicados")
    
    # 2. Hard repetitions
    print("\n" + "-"*60)
    print("2. COMPARATIVA DURA (o número de ordem aparece em dois concorrentes diferentes, sem considerar especialidade):")
    if hard_reps:
        for numero, occurrences in hard_reps.items():
            print(f"\n  Nº {numero}:")
            for occ in occurrences:
                print(f"    - {occ['identifier']} ({occ['especialidade']})")
    else:
        print("  ✓ Sem duplicados")
    
    print("\n" + "="*60 + "\n")


def process_team_data(pdf_folder: str = None):
    """
    Read PDFs, extract table data, validate and check for repetitions.
    
    Args:
        pdf_folder: Directory containing PDF files (uses config default if None)
    
    Returns:
        Dict organized by identifier_key with structured data
    """
    if pdf_folder is None:
        pdf_folder = PDF_FOLDER
    
    print(f"Reading PDFs from: {pdf_folder}\n")
    
    raw_pdf_data = read_pdf_folder(
        folder_path=pdf_folder,
        column_names=COLUMNS,
        key_mapping=FILE_MAPPING
    )
    
    if not raw_pdf_data:
        print("No PDF data extracted.")
        return {}
    
    # Transformar em formato estruturado
    structured_data = transform_pdf_data(raw_pdf_data)
    print(f"\nSuccessfully extracted {len(structured_data)} PDF files\n")

    # Validar la estructura vertical de especialidades
    validation = validate_estrutura(structured_data)

    # Verificar repeticiones
    light_reps = check_light_repetitions(structured_data)
    hard_reps = check_hard_repetitions(structured_data)

    # Imprimir tabla detallada de datos extraídos
    print_structured_data_table(structured_data, validation)
    
    # Imprimir conflictos
    print_validation_report(light_reps, hard_reps)

    return structured_data


if __name__ == "__main__":
    extracted_data = process_team_data()
    # Debug: coordinate with import at the top of the file
    # debug_pdf_tables(os.path.join(PDF_FOLDER, "11178.pdf"))