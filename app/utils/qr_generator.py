import qrcode
import os
from flask import url_for

def generate_qr_code(unique_code, save_path):
    """
    Generate QR code for user profile
    Returns the filename of saved QR code
    """
    replit_domain = os.environ.get('REPLIT_DEV_DOMAIN', '')
    if replit_domain:
        if not replit_domain.startswith('http'):
            profile_url = f"https://{replit_domain}/profile/view/{unique_code}"
        else:
            profile_url = f"{replit_domain}/profile/view/{unique_code}"
    else:
        profile_url = f"http://localhost:5000/profile/view/{unique_code}"
    
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
