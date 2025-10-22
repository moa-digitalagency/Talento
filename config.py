import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-2024-talento-maroc'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///talento.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clé de chiffrement persistante (générer une seule fois)
    _default_encryption_key = 'gAAAAABmFNqK0qhTMrRCLzprdQycr0cJTIwjm6FfA3G6q9rRkynkFs0='
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or _default_encryption_key
    
    # Configuration CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Session cookie configuration for Replit proxy/iframe environment
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'None'
    
    # Remember cookie configuration
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'None'
    
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
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@myoneart.com'
    
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
