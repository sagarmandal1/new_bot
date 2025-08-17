import re
from datetime import datetime

def validate_time_format(time_str: str) -> bool:
    """Validate time format (HH:MM)"""
    pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
    return bool(re.match(pattern, time_str))

def validate_name(name: str) -> bool:
    """Validate name (non-empty, reasonable length)"""
    return bool(name and len(name.strip()) >= 2 and len(name.strip()) <= 50)

def validate_age(age_str: str) -> bool:
    """Validate age (must be a number between 5 and 120)"""
    try:
        age = int(age_str)
        return 5 <= age <= 120
    except ValueError:
        return False

def validate_routine_name(name: str) -> bool:
    """Validate routine name"""
    return bool(name and len(name.strip()) >= 2 and len(name.strip()) <= 100)

def validate_routine_description(description: str) -> bool:
    """Validate routine description"""
    return bool(description and len(description.strip()) >= 5 and len(description.strip()) <= 500)

def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    return text.strip()[:500]  # Limit length and remove whitespace

def validate_frequency(frequency: str) -> bool:
    """Validate routine frequency"""
    valid_frequencies = ["daily", "weekly", "monthly", "প্রতিদিন", "সাপ্তাহিক", "মাসিক"]
    return frequency.lower() in [f.lower() for f in valid_frequencies]