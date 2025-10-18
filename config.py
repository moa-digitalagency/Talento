import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///talento.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
    
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    UPLOAD_FOLDER = 'app/static/uploads'
    ALLOWED_PHOTO_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    ALLOWED_CV_EXTENSIONS = {'pdf', 'doc', 'docx'}
    MAX_PHOTO_SIZE = 5 * 1024 * 1024
    MAX_CV_SIZE = 10 * 1024 * 1024
    
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@talento.app'
    
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
