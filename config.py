"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set. Generate one with: python -c 'import secrets; print(secrets.token_hex(32))'")
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///talento.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clé de chiffrement (OBLIGATOIRE pour protéger les données sensibles)
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
    if not ENCRYPTION_KEY:
        raise ValueError("ENCRYPTION_KEY environment variable must be set. Generate one with: python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'") 
    
    # Configuration CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    WTF_CSRF_CHECK_DEFAULT = True
    WTF_CSRF_SSL_STRICT = False
    
    # Session cookie configuration - optimized for VPS and proxy environments
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = None
    SESSION_COOKIE_DOMAIN = None
    
    # Remember cookie configuration
    REMEMBER_COOKIE_SECURE = False
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = None
    REMEMBER_COOKIE_DURATION = 3600 * 24 * 30
    
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
    OMDB_API_KEY = os.environ.get('OMDB_API_KEY')
    
    # URL de base pour les QR codes et liens publics
    # Fonctionne sur Replit, VPS, ou n'importe quelle plateforme
    @staticmethod
    def get_base_url():
        """Retourne l'URL de base de l'application selon l'environnement"""
        # 1. Essayer la variable d'environnement BASE_URL (VPS, production personnalisée)
        base_url = os.environ.get('BASE_URL')
        if base_url:
            return base_url.rstrip('/')
        
        # 2. Essayer REPLIT_DOMAINS (environnement Replit)
        replit_domain = os.environ.get('REPLIT_DOMAINS')
        if replit_domain:
            if not replit_domain.startswith('http'):
                return f'https://{replit_domain}'
            return replit_domain.rstrip('/')
        
        # 3. Fallback pour développement local
        return 'http://localhost:5000'
