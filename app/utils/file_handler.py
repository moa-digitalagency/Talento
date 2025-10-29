"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

import os
from werkzeug.utils import secure_filename
from flask import current_app
import uuid

ALLOWED_PHOTO_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_CV_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(file, upload_type='photo'):
    """
    Save uploaded file and return filename
    upload_type: 'photo' or 'cv'
    """
    if not file or file.filename == '':
        return None
    
    allowed_extensions = ALLOWED_PHOTO_EXTENSIONS if upload_type == 'photo' else ALLOWED_CV_EXTENSIONS
    
    if not allowed_file(file.filename, allowed_extensions):
        return None
    
    original_filename = secure_filename(file.filename)
    extension = original_filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    
    folder = 'photos' if upload_type == 'photo' else 'cvs'
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
    os.makedirs(upload_path, exist_ok=True)
    
    file_path = os.path.join(upload_path, unique_filename)
    file.save(file_path)
    
    return unique_filename

def delete_file(filename, upload_type='photo'):
    """Delete a file from uploads"""
    if not filename:
        return
    
    folder = 'photos' if upload_type == 'photo' else 'cvs'
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder, filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)
