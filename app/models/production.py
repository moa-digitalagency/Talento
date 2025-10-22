from datetime import datetime
from app import db

class Production(db.Model):
    __tablename__ = 'productions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Informations de base
    title = db.Column(db.String(200), nullable=False)
    original_title = db.Column(db.String(200))
    production_type = db.Column(db.String(50), nullable=False)  # Film, Série, Court-métrage, Documentaire, etc.
    genre = db.Column(db.String(100))  # Drame, Comédie, Action, etc.
    
    # Détails de production
    director = db.Column(db.String(200))
    producer = db.Column(db.String(200))
    production_company = db.Column(db.String(200))
    country = db.Column(db.String(100))
    language = db.Column(db.String(100))
    
    # Dates
    production_year = db.Column(db.Integer)
    release_date = db.Column(db.Date)
    start_date = db.Column(db.Date)  # Date de début de tournage
    end_date = db.Column(db.Date)  # Date de fin de tournage
    
    # Description
    synopsis = db.Column(db.Text)
    description = db.Column(db.Text)
    
    # Budget et revenus
    budget = db.Column(db.String(100))
    box_office = db.Column(db.String(100))
    
    # Médias
    poster_url = db.Column(db.String(500))
    trailer_url = db.Column(db.String(500))
    
    # Informations techniques
    duration = db.Column(db.Integer)  # Durée en minutes
    rating = db.Column(db.String(50))  # Classification (PG, R, etc.)
    
    # Casting et équipe (stockés en JSON)
    cast = db.Column(db.Text)  # JSON list des acteurs
    crew = db.Column(db.Text)  # JSON list de l'équipe technique
    
    # Récompenses et festivals
    awards = db.Column(db.Text)  # JSON list des prix et nominations
    festivals = db.Column(db.Text)  # JSON list des festivals
    
    # Liens et références
    imdb_id = db.Column(db.String(50))
    tmdb_id = db.Column(db.String(50))
    website = db.Column(db.String(500))
    
    # Statut
    status = db.Column(db.String(50), default='En production')  # En production, Post-production, Sortie, Annulé
    is_active = db.Column(db.Boolean, default=True)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<Production {self.title}>'
    
    @property
    def year_display(self):
        """Afficher l'année de production"""
        return self.production_year or (self.release_date.year if self.release_date else None)
