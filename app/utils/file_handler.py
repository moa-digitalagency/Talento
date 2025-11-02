"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

import os
import shutil
from werkzeug.utils import secure_filename
from flask import current_app
import uuid

ALLOWED_PHOTO_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_CV_EXTENSIONS = {'pdf', 'doc', 'docx'}
ALLOWED_LOGO_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg'}

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(file, upload_type='photo'):
    """
    Save uploaded file and return filename
    upload_type: 'photo', 'cv', 'cinema_photos', etc.
    """
    if not file or file.filename == '':
        return None
    
    # Déterminer les extensions autorisées basées sur le type
    if 'photo' in upload_type.lower():
        allowed_extensions = ALLOWED_PHOTO_EXTENSIONS
    elif upload_type == 'cv':
        allowed_extensions = ALLOWED_CV_EXTENSIONS
    else:
        allowed_extensions = ALLOWED_PHOTO_EXTENSIONS
    
    if not allowed_file(file.filename, allowed_extensions):
        return None
    
    original_filename = secure_filename(file.filename)
    extension = original_filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    
    # Utiliser le upload_type comme nom de dossier, sauf pour 'photo' qui devient 'photos'
    if upload_type == 'photo':
        folder = 'photos'
    elif upload_type == 'cv':
        folder = 'cvs'
    else:
        folder = upload_type
    
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
    os.makedirs(upload_path, exist_ok=True)
    
    file_path = os.path.join(upload_path, unique_filename)
    file.save(file_path)
    
    return unique_filename

def delete_file(filename, upload_type='photo'):
    """Delete a file from uploads"""
    if not filename:
        return
    
    # Utiliser le même mapping que save_file pour le dossier
    if upload_type == 'photo':
        folder = 'photos'
    elif upload_type == 'cv':
        folder = 'cvs'
    else:
        folder = upload_type
    
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder, filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)

def copy_file_between_folders(filename, source_upload_type, dest_upload_type):
    """
    Copy a file from one upload folder to another
    Returns: True if successful, False otherwise
    """
    if not filename:
        return False
    
    # Map upload types to folder names
    def get_folder_name(upload_type):
        if upload_type == 'photo':
            return 'photos'
        elif upload_type == 'cv':
            return 'cvs'
        else:
            return upload_type
    
    source_folder = get_folder_name(source_upload_type)
    dest_folder = get_folder_name(dest_upload_type)
    
    source_path = os.path.join(current_app.config['UPLOAD_FOLDER'], source_folder, filename)
    dest_path = os.path.join(current_app.config['UPLOAD_FOLDER'], dest_folder, filename)
    
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Copy file if source exists
    if os.path.exists(source_path):
        shutil.copy2(source_path, dest_path)
        return True
    
    return False

class FileHandler:
    """Gestionnaire de fichiers pour uploads"""
    
    @staticmethod
    def save_production_logo(file):
        """
        Sauvegarder le logo d'une production
        Retourne l'URL du logo sauvegardé
        """
        if not file or file.filename == '':
            return None
        
        if not allowed_file(file.filename, ALLOWED_LOGO_EXTENSIONS):
            return None
        
        original_filename = secure_filename(file.filename)
        extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"production_logo_{uuid.uuid4().hex}.{extension}"
        
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'production_logos')
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)
        
        return f"/uploads/production_logos/{unique_filename}"
