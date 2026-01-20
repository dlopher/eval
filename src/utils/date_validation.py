from datetime import datetime
import re
from src.config.config_linear import CURRENT_DATE, DATE_LIMITS


def parse_date(date_input) -> datetime:
    """
    Parse date from multiple formats: dd/mm/yyyy, dd/mm/yy, yyyy, or datetime object
    Returns None if unparseable
    """
    if isinstance(date_input, datetime):
        return date_input
    
    if pd.isna(date_input):
        return None
    
    date_str = str(date_input).strip()
    
    # Try yyyy format
    if re.match(r'^\d{4}$', date_str):
        try:
            return datetime(int(date_str), 12, 31)  # end of year
        except:
            return None
    
    # Try dd/mm/yyyy or dd/mm/yy
    for fmt in ['%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y']:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    
    return None


def validate_date(date_obj: datetime, item_type: str = "projeto") -> tuple:
    """
    Validate date against age limit.
    Returns: (is_valid, status, observation)
    
    - is_valid: True if passes validation
    - status: "" (empty/valid), "DESCL" (disqualified), or "AVISO" (warning)
    - observation: reason/note
    """
    if date_obj is None:
        return False, "DESCL", "Data ausente"
    
    limit_years = DATE_LIMITS.get(item_type, 10)
    year_diff = CURRENT_DATE.year - date_obj.year
    
    # Account for months (if project is in same year but after current date, it's -1)
    if date_obj.month > CURRENT_DATE.month:
        year_diff -= 1
    elif date_obj.month == CURRENT_DATE.month and date_obj.day > CURRENT_DATE.day:
        year_diff -= 1
    
    if year_diff > limit_years:
        return False, "DESCL", f"Excede limite de {limit_years} anos (antiguedade: {year_diff} anos)"
    elif year_diff == limit_years:
        return True, "AVISO", f"No limite de {limit_years} anos (antiguedade: {year_diff} anos. Verificar data)"
    else:
        return True, "", ""