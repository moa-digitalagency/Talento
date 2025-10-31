"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from app import db
from datetime import datetime
import json

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
        if not setting or not setting.value:
            return default
        
        try:
            return json.loads(setting.value)
        except (json.JSONDecodeError, TypeError):
            return setting.value
    
    @staticmethod
    def set(key, value):
        """Définit une valeur de configuration"""
        if isinstance(value, (dict, list)):
            value_str = json.dumps(value, ensure_ascii=False)
        else:
            value_str = str(value) if value is not None else None
            
        setting = AppSettings.query.filter_by(key=key).first()
        if setting:
            setting.value = value_str
            setting.updated_at = datetime.utcnow()
        else:
            setting = AppSettings(key=key, value=value_str)
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
