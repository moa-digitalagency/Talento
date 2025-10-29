"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from app import db
from datetime import datetime

class AppSettings(db.Model):
    __tablename__ = 'app_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def get(key, default=None):
        """Récupère une valeur de configuration"""
        setting = AppSettings.query.filter_by(key=key).first()
        return setting.value if setting and setting.value else default
    
    @staticmethod
    def set(key, value):
        """Définit une valeur de configuration"""
        setting = AppSettings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            setting.updated_at = datetime.utcnow()
        else:
            setting = AppSettings(key=key, value=value)
            db.session.add(setting)
        db.session.commit()
        return setting
    
    @staticmethod
    def delete(key):
        """Supprime une clé de configuration"""
        setting = AppSettings.query.filter_by(key=key).first()
        if setting:
            db.session.delete(setting)
            db.session.commit()
            return True
        return False
