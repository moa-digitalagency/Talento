from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from sqlalchemy import event

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    unique_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(1))
    
    phone_encrypted = db.Column(db.Text)
    whatsapp_encrypted = db.Column(db.Text)
    address_encrypted = db.Column(db.Text)
    
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    
    photo_filename = db.Column(db.String(255))
    cv_filename = db.Column(db.String(255))
    portfolio_url = db.Column(db.String(500))
    
    linkedin_encrypted = db.Column(db.Text)
    instagram_encrypted = db.Column(db.Text)
    twitter_encrypted = db.Column(db.Text)
    facebook_encrypted = db.Column(db.Text)
    tiktok_encrypted = db.Column(db.Text)
    youtube_encrypted = db.Column(db.Text)
    github_encrypted = db.Column(db.Text)
    behance_encrypted = db.Column(db.Text)
    dribbble_encrypted = db.Column(db.Text)
    pinterest_encrypted = db.Column(db.Text)
    snapchat_encrypted = db.Column(db.Text)
    telegram_encrypted = db.Column(db.Text)
    
    bio = db.Column(db.Text)
    years_experience = db.Column(db.Integer)
    profile_score = db.Column(db.Integer, default=0)
    
    availability = db.Column(db.String(50))
    work_mode = db.Column(db.String(50))
    rate_range = db.Column(db.String(100))
    
    is_admin = db.Column(db.Boolean, default=False)
    account_active = db.Column(db.Boolean, default=True)
    
    qr_code_filename = db.Column(db.String(255))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    country = db.relationship('Country', backref='users')
    city = db.relationship('City', backref='users')
    talents = db.relationship('UserTalent', back_populates='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def formatted_code(self):
        if len(self.unique_code) == 10:
            return f"{self.unique_code[:2]}-{self.unique_code[2:5]}-{self.unique_code[5:9]}-{self.unique_code[9]}"
        return self.unique_code
    
    @property
    def phone(self):
        """Déchiffrer et retourner le numéro de téléphone"""
        if not self.phone_encrypted:
            return None
        try:
            from app.utils.encryption import decrypt_sensitive_data
            return decrypt_sensitive_data(self.phone_encrypted)
        except:
            return None
    
    @phone.setter
    def phone(self, value):
        """Chiffrer et stocker le numéro de téléphone"""
        if value:
            from app.utils.encryption import encrypt_sensitive_data
            self.phone_encrypted = encrypt_sensitive_data(value)
        else:
            self.phone_encrypted = None
    
    @property
    def whatsapp(self):
        """Déchiffrer et retourner le numéro WhatsApp"""
        if not self.whatsapp_encrypted:
            return None
        try:
            from app.utils.encryption import decrypt_sensitive_data
            return decrypt_sensitive_data(self.whatsapp_encrypted)
        except:
            return None
    
    @whatsapp.setter
    def whatsapp(self, value):
        """Chiffrer et stocker le numéro WhatsApp"""
        if value:
            from app.utils.encryption import encrypt_sensitive_data
            self.whatsapp_encrypted = encrypt_sensitive_data(value)
        else:
            self.whatsapp_encrypted = None
    
    @property
    def address(self):
        """Déchiffrer et retourner l'adresse"""
        if not self.address_encrypted:
            return None
        try:
            from app.utils.encryption import decrypt_sensitive_data
            return decrypt_sensitive_data(self.address_encrypted)
        except:
            return None
    
    @address.setter
    def address(self, value):
        """Chiffrer et stocker l'adresse"""
        if value:
            from app.utils.encryption import encrypt_sensitive_data
            self.address_encrypted = encrypt_sensitive_data(value)
        else:
            self.address_encrypted = None
    
    def _get_social_media(self, field_name):
        """Helper pour déchiffrer les réseaux sociaux"""
        encrypted_field = f"{field_name}_encrypted"
        encrypted_value = getattr(self, encrypted_field, None)
        if not encrypted_value:
            return None
        try:
            from app.utils.encryption import decrypt_sensitive_data
            return decrypt_sensitive_data(encrypted_value)
        except:
            return None
    
    def _set_social_media(self, field_name, value):
        """Helper pour chiffrer les réseaux sociaux"""
        encrypted_field = f"{field_name}_encrypted"
        if value:
            from app.utils.encryption import encrypt_sensitive_data
            setattr(self, encrypted_field, encrypt_sensitive_data(value))
        else:
            setattr(self, encrypted_field, None)
    
    @property
    def linkedin(self):
        return self._get_social_media('linkedin')
    
    @linkedin.setter
    def linkedin(self, value):
        self._set_social_media('linkedin', value)
    
    @property
    def instagram(self):
        return self._get_social_media('instagram')
    
    @instagram.setter
    def instagram(self, value):
        self._set_social_media('instagram', value)
    
    @property
    def twitter(self):
        return self._get_social_media('twitter')
    
    @twitter.setter
    def twitter(self, value):
        self._set_social_media('twitter', value)
    
    @property
    def facebook(self):
        return self._get_social_media('facebook')
    
    @facebook.setter
    def facebook(self, value):
        self._set_social_media('facebook', value)
    
    @property
    def tiktok(self):
        return self._get_social_media('tiktok')
    
    @tiktok.setter
    def tiktok(self, value):
        self._set_social_media('tiktok', value)
    
    @property
    def youtube(self):
        return self._get_social_media('youtube')
    
    @youtube.setter
    def youtube(self, value):
        self._set_social_media('youtube', value)
    
    @property
    def github(self):
        return self._get_social_media('github')
    
    @github.setter
    def github(self, value):
        self._set_social_media('github', value)
    
    @property
    def behance(self):
        return self._get_social_media('behance')
    
    @behance.setter
    def behance(self, value):
        self._set_social_media('behance', value)
    
    @property
    def dribbble(self):
        return self._get_social_media('dribbble')
    
    @dribbble.setter
    def dribbble(self, value):
        self._set_social_media('dribbble', value)
    
    @property
    def pinterest(self):
        return self._get_social_media('pinterest')
    
    @pinterest.setter
    def pinterest(self, value):
        self._set_social_media('pinterest', value)
    
    @property
    def snapchat(self):
        return self._get_social_media('snapchat')
    
    @snapchat.setter
    def snapchat(self, value):
        self._set_social_media('snapchat', value)
    
    @property
    def telegram(self):
        return self._get_social_media('telegram')
    
    @telegram.setter
    def telegram(self, value):
        self._set_social_media('telegram', value)
    
    def __repr__(self):
        return f'<User {self.email}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
