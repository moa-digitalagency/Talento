from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

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
    
    phone = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    address = db.Column(db.String(255))
    
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    
    photo_filename = db.Column(db.String(255))
    cv_filename = db.Column(db.String(255))
    portfolio_url = db.Column(db.String(500))
    
    linkedin = db.Column(db.String(255))
    instagram = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    facebook = db.Column(db.String(255))
    tiktok = db.Column(db.String(255))
    github = db.Column(db.String(255))
    behance = db.Column(db.String(255))
    dribbble = db.Column(db.String(255))
    
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
    
    def __repr__(self):
        return f'<User {self.email}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
