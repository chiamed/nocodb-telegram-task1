import re
from datetime import datetime

def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def is_valid_phone(phone: str) -> bool:
    return re.match(r"^\+?\d[\d\s]{6,20}$", phone) is not None

def is_valid_username(username: str) -> bool:
    return re.match(r"^@[\w\d_]{3,32}$", username) is not None

def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False

def normalize_sex(value: str) -> str | None:
    value = value.lower()

    if value in ["male", "m", "man", "uomo"]:
        return "Male"
    if value in ["female", "f", "woman", "donna"]:
        return "Female"

    return None
