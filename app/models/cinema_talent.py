from datetime import datetime
from app import db

class CinemaTalent(db.Model):
    __tablename__ = 'cinema_talents'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Personal Information
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    
    # ID Document
    id_document_type = db.Column(db.String(50), nullable=False)
    id_document_number_encrypted = db.Column(db.Text, nullable=False)
    
    # Origins
    ethnicities = db.Column(db.Text)  # JSON list of multiple ethnicities
    country_of_origin = db.Column(db.String(100))
    nationality = db.Column(db.String(100), nullable=False)
    
    # Location
    country_of_residence = db.Column(db.String(100), nullable=False)
    city_of_residence = db.Column(db.String(100), nullable=False)
    
    # Languages & Experience (multiple choices stored as JSON)
    languages_spoken = db.Column(db.Text)  # JSON list
    years_of_experience = db.Column(db.Integer, default=0)
    
    # Talent Types (multiple choices stored as JSON)
    talent_types = db.Column(db.Text)  # JSON list - Acteur Principal, Secondaire, Figurant, etc.
    
    # Physical Characteristics
    eye_color = db.Column(db.String(50))
    hair_color = db.Column(db.String(50))
    hair_type = db.Column(db.String(50))
    height = db.Column(db.Integer)
    skin_tone = db.Column(db.String(50))
    build = db.Column(db.String(50))
    
    # Other Talents (multiple choices stored as JSON)
    other_talents = db.Column(db.Text)  # JSON list
    
    # Photos
    profile_photo_filename = db.Column(db.String(255))
    id_photo_filename = db.Column(db.String(255))
    gallery_photos = db.Column(db.Text)
    
    # Contact Details (encrypted)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone_encrypted = db.Column(db.Text, nullable=False)
    whatsapp_encrypted = db.Column(db.Text)
    website = db.Column(db.String(500))  # Site web personnel/professionnel
    
    # Social Media (encrypted)
    facebook_encrypted = db.Column(db.Text)
    instagram_encrypted = db.Column(db.Text)
    linkedin_encrypted = db.Column(db.Text)
    twitter_encrypted = db.Column(db.Text)
    youtube_encrypted = db.Column(db.Text)
    tiktok_encrypted = db.Column(db.Text)
    snapchat_encrypted = db.Column(db.Text)
    telegram_encrypted = db.Column(db.Text)
    imdb_url_encrypted = db.Column(db.Text)
    threads_encrypted = db.Column(db.Text)
    
    # Previous Experience
    previous_productions = db.Column(db.Text)
    
    # Unique Identification
    unique_code = db.Column(db.String(12), unique=True, nullable=True, index=True)
    qr_code_filename = db.Column(db.String(255))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculer l'âge à partir de la date de naissance"""
        if not self.date_of_birth:
            return None
        from datetime import date
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age
    
    @property
    def gender_display(self):
        """Afficher le genre de manière lisible"""
        if not self.gender:
            return None
        return 'Homme' if self.gender == 'M' else 'Femme'
    
    @property
    def id_document_number_initials(self):
        """Afficher les initiales du numéro de pièce d'identité (format masqué)"""
        if not self.id_document_number_encrypted:
            return None
        
        try:
            from app.utils.encryption import decrypt_sensitive_data
            decrypted_number = decrypt_sensitive_data(self.id_document_number_encrypted)
            
            if not decrypted_number:
                return "***"
            
            # Toujours masquer les données sensibles
            length = len(decrypted_number)
            if length <= 2:
                return "***"
            elif length <= 5:
                # Pour 3-5 caractères: premier + *** + dernier
                return f"{decrypted_number[0]}***{decrypted_number[-1]}"
            else:
                # Pour 6+ caractères: 3 premiers + *** + 3 derniers
                return f"{decrypted_number[:3]}***{decrypted_number[-3:]}"
        except Exception:
            return "***"
    
    def __repr__(self):
        return f'<CinemaTalent {self.first_name} {self.last_name}>'
