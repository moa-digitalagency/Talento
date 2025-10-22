from datetime import datetime
from app import db

class Production(db.Model):
    """Modèle représentant une boîte de production (société de production)"""
    __tablename__ = 'productions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Informations de base
    name = db.Column(db.String(200), nullable=False)  # Nom de la société
    logo_url = db.Column(db.String(500))  # Logo de la société
    
    # Description
    description = db.Column(db.Text)  # Description de la société
    specialization = db.Column(db.String(200))  # Films, Séries, Documentaires, Publicités, etc.
    
    # Coordonnées
    address = db.Column(db.String(300))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    
    # Contact
    phone = db.Column(db.String(50))
    email = db.Column(db.String(120))
    website = db.Column(db.String(500))
    
    # Réseaux sociaux
    facebook = db.Column(db.String(200))
    instagram = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))
    twitter = db.Column(db.String(200))
    
    # Informations sur l'entreprise
    founded_year = db.Column(db.Integer)  # Année de fondation
    ceo = db.Column(db.String(200))  # Directeur/CEO
    employees_count = db.Column(db.Integer)  # Nombre d'employés
    
    # Productions
    productions_count = db.Column(db.Integer, default=0)  # Nombre de productions réalisées
    notable_productions = db.Column(db.Text)  # JSON list des productions notables
    
    # Services offerts
    services = db.Column(db.Text)  # JSON list des services (Production, Post-production, Distribution, etc.)
    
    # Équipements et studios
    equipment = db.Column(db.Text)  # Description des équipements
    studios = db.Column(db.Text)  # Description des studios
    
    # Certifications et affiliations
    certifications = db.Column(db.Text)  # JSON list des certifications
    memberships = db.Column(db.Text)  # JSON list des affiliations professionnelles
    
    # Récompenses
    awards = db.Column(db.Text)  # JSON list des prix et distinctions
    
    # Statut
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)  # Vérification de la société
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<Production Company {self.name}>'
    
    @property
    def location_display(self):
        """Afficher la localisation complète"""
        parts = [self.city, self.country]
        return ', '.join(filter(None, parts)) or 'Non spécifiée'
