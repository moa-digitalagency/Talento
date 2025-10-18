import qrcode
import os
from flask import url_for

def generate_qr_code(unique_code, save_path):
    """
    Generate QR code for user profile
    Returns the filename of saved QR code
    """
    profile_url = f"{os.environ.get('REPLIT_DEV_DOMAIN', 'http://localhost:5000')}/profile/view/{unique_code[:2]}-{unique_code[2:5]}-{unique_code[5:9]}-{unique_code[9]}"
    
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
