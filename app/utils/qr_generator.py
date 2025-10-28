"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

import qrcode
import os
from flask import url_for

def generate_qr_code(unique_code, save_path, profile_type='user'):
    """
    Generate QR code for user or cinema profile
    
    Args:
        unique_code (str): Unique code of the profile
        save_path (str): Path to save the QR code image
        profile_type (str): 'user' for regular profiles, 'cinema' for cinema talents
    
    Returns:
        str: Filename of saved QR code
    """
    replit_domain = os.environ.get('REPLIT_DOMAINS', '')
    
    # Déterminer l'URL selon le type de profil
    if profile_type == 'cinema':
        if replit_domain:
            if not replit_domain.startswith('http'):
                profile_url = f"https://{replit_domain}/cinema/profile/{unique_code}"
            else:
                profile_url = f"{replit_domain}/cinema/profile/{unique_code}"
        else:
            profile_url = f"http://localhost:5004/cinema/profile/{unique_code}"
    else:  # user profile (default)
        if replit_domain:
            if not replit_domain.startswith('http'):
                profile_url = f"https://{replit_domain}/profile/view/{unique_code}"
            else:
                profile_url = f"{replit_domain}/profile/view/{unique_code}"
        else:
            profile_url = f"http://localhost:5004/profile/view/{unique_code}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(profile_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    filename = f"qr_{unique_code}.png"
    filepath = os.path.join(save_path, filename)
    
    os.makedirs(save_path, exist_ok=True)
    img.save(filepath)
    
    return filename


def generate_cinema_qr_code(unique_code, save_path):
    """
    Generate QR code specifically for cinema talent profiles
    
    Args:
        unique_code (str): Unique code of the cinema talent
        save_path (str): Path to save the QR code image
    
    Returns:
        str: Filename of saved QR code
    """
    return generate_qr_code(unique_code, save_path, profile_type='cinema')
