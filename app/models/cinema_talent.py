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
    
    # Social Media (encrypted)
    facebook_encrypted = db.Column(db.Text)
    instagram_encrypted = db.Column(db.Text)
    linkedin_encrypted = db.Column(db.Text)
    twitter_encrypted = db.Column(db.Text)
    youtube_encrypted = db.Column(db.Text)
    tiktok_encrypted = db.Column(db.Text)
    snapchat_encrypted = db.Column(db.Text)
    
    # Previous Experience
    previous_productions = db.Column(db.Text)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<CinemaTalent {self.first_name} {self.last_name}>'
