"""
Core utilities and helper functions.
"""
import random
import string
from datetime import date


def generate_unique_id(prefix='', length=6):
    """
    Generate a unique ID with given prefix.
    Example: generate_unique_id('STU', 6) -> 'STU123456'
    """
    chars = string.digits
    random_part = ''.join(random.choice(chars) for _ in range(length))
    return f"{prefix}{random_part}"


def calculate_age(birth_date):
    """Calculate age from birth date."""
    if not birth_date:
        return None
    today = date.today()
    age = today.year - birth_date.year
    # Adjust if birthday hasn't occurred this year
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    return age


def get_current_academic_year():
    """
    Get current academic year.
    Academic year typically runs from June to May in India.
    """
    today = date.today()
    if today.month >= 6:  # June onwards
        return f"{today.year}-{today.year + 1}"
    else:  # January to May
        return f"{today.year - 1}-{today.year}"