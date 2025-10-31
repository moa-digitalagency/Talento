"""
Modèle pour le suivi des noms lors des inscriptions
Permet à l'admin de surveiller l'inscription de personnes spécifiques
"""

from app import db
from datetime import datetime


class NameTracking(db.Model):
    """
    Noms à surveiller lors des inscriptions
    """
    __tablename__ = 'name_tracking'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text)  # Note ou raison de la surveillance
    notification_email = db.Column(db.String(255))  # Email où envoyer la notification (par défaut admin)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Suivi des matchs
    matches = db.relationship('NameTrackingMatch', back_populates='tracked_name', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<NameTracking {self.full_name}>'
    
    @staticmethod
    def is_name_tracked(full_name):
        """
        Vérifie si un nom est actuellement surveillé
        
        Args:
            full_name: Nom complet à vérifier
            
        Returns:
            NameTracking object si trouvé et actif, None sinon
        """
        if not full_name:
            return None
        
        # Recherche insensible à la casse
        tracked = NameTracking.query.filter(
            db.func.lower(NameTracking.full_name) == db.func.lower(full_name),
            NameTracking.is_active == True
        ).first()
        
        return tracked


class NameTrackingMatch(db.Model):
    """
    Enregistrement des correspondances trouvées
    """
    __tablename__ = 'name_tracking_matches'
    
    id = db.Column(db.Integer, primary_key=True)
    tracked_name_id = db.Column(db.Integer, db.ForeignKey('name_tracking.id'), nullable=False)
    
    # Référence au talent ou talent cinéma qui a matché
    talent_code = db.Column(db.String(50))  # Code unique du talent
    talent_type = db.Column(db.String(20))  # 'talent' ou 'cinema'
    
    # Informations de base
    registered_name = db.Column(db.String(255))  # Nom tel qu'enregistré
    email = db.Column(db.String(255))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    
    # Statut de la notification
    notification_sent = db.Column(db.Boolean, default=False)
    notification_sent_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    tracked_name = db.relationship('NameTracking', back_populates='matches')
    
    def __repr__(self):
        return f'<NameTrackingMatch {self.registered_name} ({self.talent_code})>'
