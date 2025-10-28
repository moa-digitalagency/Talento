"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

import qrcode
import os
from config import Config

def generate_qr_code(unique_code, save_path, profile_type='user'):
    """
    Generate QR code for user or cinema profile
    Fonctionne sur toutes les plateformes (Replit, VPS, local)
    
    Args:
        unique_code (str): Unique code of the profile
        save_path (str): Path to save the QR code image
        profile_type (str): 'user' for regular profiles, 'cinema' for cinema talents
    
    Returns:
        str: Filename of saved QR code
    """
    # Obtenir l'URL de base selon l'environnement (Replit, VPS, ou local)
    base_url = Config.get_base_url()
    
    # Construire l'URL complète selon le type de profil
    if profile_type == 'cinema':
        profile_url = f"{base_url}/cinema/profile/{unique_code}"
    else:  # user profile (default)
        profile_url = f"{base_url}/profile/view/{unique_code}"
    
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
