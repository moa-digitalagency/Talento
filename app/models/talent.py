from app import db
from datetime import datetime

class Talent(db.Model):
    __tablename__ = 'talents'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    emoji = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    
    users = db.relationship('UserTalent', back_populates='talent')
    
    def __repr__(self):
        return f'<Talent {self.emoji} {self.name}>'

class UserTalent(db.Model):
    __tablename__ = 'user_talents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    talent_id = db.Column(db.Integer, db.ForeignKey('talents.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='talents')
    talent = db.relationship('Talent', back_populates='users')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'talent_id', name='_user_talent_uc'),)
    
    def __repr__(self):
        return f'<UserTalent user_id={self.user_id} talent_id={self.talent_id}>'
