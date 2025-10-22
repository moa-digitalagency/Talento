"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from datetime import datetime
from app import db
import json

class Project(db.Model):
    """Modèle représentant un projet de production en cours"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Informations de base
    name = db.Column(db.String(200), nullable=False)
    production_type = db.Column(db.String(100), nullable=False)  # Film, Série, Publicité, etc.
    
    # Société de production
    production_company_id = db.Column(db.Integer, db.ForeignKey('productions.id'))
    production_company = db.relationship('Production', backref='projects')
    
    # Localisation
    origin_country = db.Column(db.String(100))
    shooting_locations = db.Column(db.Text)  # Lieux de tournage (texte libre ou JSON)
    
    # Dates
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # Statut
    status = db.Column(db.String(50), default='en_preparation')  # en_preparation, en_tournage, post_production, termine
    is_active = db.Column(db.Boolean, default=True)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relations
    project_talents = db.relationship('ProjectTalent', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Project {self.name}>'
    
    @property
    def dates_display(self):
        """Afficher les dates du projet"""
        if self.start_date and self.end_date:
            return f"{self.start_date.strftime('%d/%m/%Y')} - {self.end_date.strftime('%d/%m/%Y')}"
        elif self.start_date:
            return f"Début: {self.start_date.strftime('%d/%m/%Y')}"
        elif self.end_date:
            return f"Fin: {self.end_date.strftime('%d/%m/%Y')}"
        return "Dates non définies"
    
    @property
    def status_display(self):
        """Afficher le statut de manière lisible"""
        status_map = {
            'en_preparation': 'En préparation',
            'en_tournage': 'En tournage',
            'post_production': 'Post-production',
            'termine': 'Terminé'
        }
        return status_map.get(self.status, self.status)


class ProjectTalent(db.Model):
    """Modèle représentant l'assignation d'un talent CINEMA à un projet"""
    __tablename__ = 'project_talents'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Relations
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    cinema_talent_id = db.Column(db.Integer, db.ForeignKey('cinema_talents.id'), nullable=False)
    cinema_talent = db.relationship('CinemaTalent', backref='project_assignments')
    
    # Rôle dans le projet
    talent_type = db.Column(db.String(100), nullable=False)  # Type de talent assigné pour ce projet
    role_description = db.Column(db.Text)  # Description du rôle (optionnel)
    
    # Code unique pour ce projet
    project_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    
    # Badge
    badge_generated = db.Column(db.Boolean, default=False)
    badge_filename = db.Column(db.String(255))
    
    # Métadonnées
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<ProjectTalent {self.project_code}>'
    
    @property
    def full_name(self):
        """Nom complet du talent"""
        if self.cinema_talent:
            return f"{self.cinema_talent.first_name} {self.cinema_talent.last_name}"
        return "N/A"
