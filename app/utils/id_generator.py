"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

def generate_unique_code(country_code, city_code, gender):
    """
    Generate unique alphanumeric code: PPGNNNNVVV
    PP: 2 letters from country (ISO-2 code)
    G: Gender (M/F/N)
    NNNN: 4 sequential digits (incremented per country)
    VVV: 3 letters from city
    
    Example: MAM0001RAB (Morocco, Male, 1st person in Morocco, Rabat)
    
    Note: The sequential number is incremented per COUNTRY, not per city.
    This ensures unique identification while maintaining country-level tracking.
    """
    from app.models.user import User
    
    country_part = country_code[:2].upper()
    city_part = city_code[:3].upper()
    gender_part = gender.upper() if gender in ['M', 'F', 'N'] else 'N'
    
    # Find the next sequential number for this COUNTRY
    # Search for all codes starting with the country code
    all_users = User.query.filter(
        User.unique_code.like(f"{country_part}%")
    ).all()
    
    max_sequence = 0
    if all_users:
        for user in all_users:
            if user.unique_code and len(user.unique_code) >= 10:
                try:
                    # Extract the numeric part from PPGNNNNVVV format
                    # Position 3-7 contains NNNN (4 digits)
                    numeric_part = user.unique_code[3:7]
                    if numeric_part.isdigit():
                        sequence_num = int(numeric_part)
                        max_sequence = max(max_sequence, sequence_num)
                except (ValueError, IndexError):
                    continue
    
    next_number = max_sequence + 1
    
    # Format the number with 4 digits (zero-padded)
    sequence = str(next_number).zfill(4)
    
    # Build the final code: PPGNNNNVVV
    code = f"{country_part}{gender_part}{sequence}{city_part}"
    
    return code

def is_code_unique(code):
    """Check if code is unique in database"""
    from app.models.user import User
    return User.query.filter_by(unique_code=code).first() is None

def generate_unique_user_code(country_code, city_code, gender):
    """
    Generate unique code with sequential numbering per country.
    
    Format: PPGNNNNVVV
    - PP: Country code (2 letters)
    - G: Gender (M/F/N)
    - NNNN: Sequential number per country (4 digits)
    - VVV: City code (3 letters)
    
    The function ensures the code is unique by checking the database.
    Sequential numbering is incremented per country, not per city.
    """
    # Generate the code
    code = generate_unique_code(country_code, city_code, gender)
    
    # Double-check uniqueness (should always be unique with sequential numbering)
    if not is_code_unique(code):
        # This should rarely happen, but handle it just in case
        # Try up to 10 times with incremented numbers
        from app.models.user import User
        for i in range(1, 11):
            country_part = country_code[:2].upper()
            city_part = city_code[:3].upper()
            gender_part = gender.upper() if gender in ['M', 'F', 'N'] else 'N'
            
            # Find max again and add offset
            all_users = User.query.filter(
                User.unique_code.like(f"{country_part}%")
            ).all()
            
            max_sequence = 0
            if all_users:
                for user in all_users:
                    if user.unique_code and len(user.unique_code) >= 10:
                        try:
                            numeric_part = user.unique_code[3:7]
                            if numeric_part.isdigit():
                                sequence_num = int(numeric_part)
                                max_sequence = max(max_sequence, sequence_num)
                        except (ValueError, IndexError):
                            continue
            
            next_number = max_sequence + i
            sequence = str(next_number).zfill(4)
            code = f"{country_part}{gender_part}{sequence}{city_part}"
            
            if is_code_unique(code):
                return code
        
        raise ValueError("Unable to generate unique code after maximum attempts")
    
    return code
