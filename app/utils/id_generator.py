"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

import random
import string

def generate_unique_code(country_code, city_code, gender):
    """
    Generate unique alphanumeric code: PPVVVNNNNG
    PP: 2 letters from country
    VVV: 3 letters from city
    NNNN: 4 random digits
    G: Gender (M/F/N)
    """
    country_part = country_code[:2].upper()
    city_part = city_code[:3].upper()
    numbers = ''.join(random.choices(string.digits, k=4))
    gender_part = gender.upper() if gender in ['M', 'F', 'N'] else 'N'
    
    code = f"{country_part}{city_part}{numbers}{gender_part}"
    return code

def is_code_unique(code):
    """Check if code is unique in database"""
    from app.models.user import User
    return User.query.filter_by(unique_code=code).first() is None

def generate_unique_user_code(country_code, city_code, gender):
    """Generate unique code and ensure it's not already in database"""
    max_attempts = 100
    for _ in range(max_attempts):
        code = generate_unique_code(country_code, city_code, gender)
        if is_code_unique(code):
            return code
    
    raise ValueError("Unable to generate unique code after maximum attempts")
