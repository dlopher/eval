import pdfplumber
import os
import re
from typing import Dict, List


def debug_pdf_tables(pdf_path: str):
    """Debug: print all tables and headers found in a PDF"""
    print(f"\n=== Debugging: {pdf_path} ===")
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if tables:
                print(f"Page {page_num + 1}: Found {len(tables)} table(s)")
                for t_idx, table in enumerate(tables):
                    if table:
                        header = table[0]
                        print(f"  Table {t_idx + 1} header: {header}")
            else:
                print(f"Page {page_num + 1}: No tables found")


def normalize_text(text: str) -> str:
    """
    Normalize teor comparison: remove newlines, extra spaces, special chars.
    Keeps only letters and digits.
    """
    if not text:
        return ""
    # Remove newlines and tabs
    text = text.replace('\n', ' ').replace('\t', ' ')
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters like ª, º, etc.
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip().lower()


def normalize_professional_number(number_str: str) -> str:
    """
    Extract only digits from professional number.
    Handles: "OA n. 1234", "OA 1234", "OA nº 1234", "1234"
    """
    if not number_str:
        return ""
    # Keep only digits
    digits = re.sub(r'\D', '', str(number_str))
    return digits.strip()


def find_table_by_columns(pdf_path: str, column_names: List[str]) -> Dict:
    """
    Extract table from PDF by matching column headers.

    Args:
        pdf_path: Path to PDF file.
        column_names: List of expected column names

    Returns:
        Dict with matched table data, or empty dict if not found.
    """

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if not tables:
                continue

            for table in tables:
                # Get header row (first row)
                if not table or len(table) < 2:
                    continue

                # Normalize header for comparison
                header = [normalize_text(str(cell)) for cell in table[0]]
                expected = [normalize_text(col) for col in column_names]

                # Debug: print what we are comparing
                print(f"  Page {page_num + 1} - Header: {header}")
                print(f"  Expected: {expected}")

                # Check if all expected columns are present
                if all(col in header for col in expected):
                    print(f"Matched table on page {page_num + 1}")
                    return {
                        "page": page_num + 1,
                        "header": table[0], # Keep original header
                        "rows": table[1:]
                    }
                
    return {}


def read_pdf_folder(folder_path: str, column_names: List[str],
                    key_mapping: Dict[str, str]) -> Dict:
    """
    Read multiple PDFs from folder, extract table data, and organize by file key.
    
    Args:
        folder_path: Directory containing PDF files
        column_names: Expected table column headers
        key_mapping: {filename: identifier_key} e.g., {"report1.pdf": "R001"} (from config_team.py)
    
    Returns:
        Dict organized by key with extracted data
    """
    results = {}

    for filename, identifier_key in key_mapping.items():
        pdf_path = os.path.join(folder_path, filename)

        if not os.path.exists(pdf_path):
            print(f"File not found: {pdf_path}")
            continue

        print(f"Processing file: {filename}")
        table_data = find_table_by_columns(pdf_path, column_names)

        if table_data:
            results[identifier_key] = table_data
        else:
            print(f"No matching table found in {filename}")

    return results


def parse_cell_entries(cell_value: str) -> List[str]:
    """
    Parse cell that might contain multiple entries separated by newlines.
    """
    if not cell_value:
        return []
    entries = str(cell_value).split('\n')
    return [e.strip() for e in entries if e.strip()]


def transform_pdf_data(pdf_data: Dict) -> Dict:
    """
    Transform raw PDF table data into structured format.
    {
        identifier_key: {
            especialidade: {
                "nome": [list of names],
                "numero_ordem_profissional": [list of numbers]

            }
        }
    }
    """
    structured = {}

    for identifier_key, table_info in pdf_data.items():
        structured[identifier_key] = {}
        rows = table_info.get("rows", [])

        for row in rows:
            if len(row) < 3:
                continue

            especialidade = str(row[0]).strip()
            nomes = parse_cell_entries(row[1])
            numero_raw = parse_cell_entries(row[2])
            numero_ordem_profissional = [normalize_professional_number(n) for n in numero_raw]

            # Store as lists to handle multiple entries per row
            if especialidade:
                structured[identifier_key][especialidade] = {
                    "nome": nomes,
                    "numero_ordem_profissional": numero_ordem_profissional
                }

    return structured