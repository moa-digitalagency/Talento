"""
Modèle pour les logs d'activité
Enregistre toutes les actions des utilisateurs
"""
from datetime import datetime
from app import db


class ActivityLog(db.Model):
    """Modèle pour enregistrer toutes les activités des utilisateurs"""
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Qui (utilisateur)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', backref='activity_logs')
    username = db.Column(db.String(200))  # Nom complet de l'utilisateur au moment de l'action
    user_email = db.Column(db.String(120))  # Email de l'utilisateur
    user_code = db.Column(db.String(20))  # Code unique de l'utilisateur
    
    # Quoi (action)
    action_type = db.Column(db.String(100), nullable=False)  # create, update, delete, login, logout, view, etc.
    action_category = db.Column(db.String(50))  # auth, cinema, production, project, talent, settings, etc.
    action_description = db.Column(db.Text)  # Description détaillée de l'action
    resource_type = db.Column(db.String(100))  # Type de ressource concernée (User, Talent, Project, etc.)
    resource_id = db.Column(db.Integer)  # ID de la ressource concernée
    
    # Où (localisation)
    ip_address = db.Column(db.String(45))  # IPv4 ou IPv6
    country = db.Column(db.String(100))  # Pays
    city = db.Column(db.String(100))  # Ville
    
    # Périphérique et navigateur
    user_agent = db.Column(db.Text)  # User-Agent complet
    browser = db.Column(db.String(100))  # Nom du navigateur
    browser_version = db.Column(db.String(50))  # Version du navigateur
    device_type = db.Column(db.String(50))  # desktop, mobile, tablet
    device_brand = db.Column(db.String(100))  # Apple, Samsung, etc.
    device_model = db.Column(db.String(100))  # iPhone 12, Galaxy S21, etc.
    operating_system = db.Column(db.String(100))  # Windows, macOS, iOS, Android, Linux
    os_version = db.Column(db.String(50))  # Version du système d'exploitation
    
    # Request info
    request_method = db.Column(db.String(10))  # GET, POST, PUT, DELETE
    request_url = db.Column(db.String(500))  # URL de la requête
    request_referrer = db.Column(db.String(500))  # Page précédente
    
    # Données supplémentaires (JSON)
    extra_data = db.Column(db.Text)  # Données supplémentaires en JSON
    
    # Quand (timestamp)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Statut
    status = db.Column(db.String(50), default='success')  # success, error, warning
    error_message = db.Column(db.Text)  # Message d'erreur si status = error
    
    def __repr__(self):
        return f'<ActivityLog {self.user_email} - {self.action_type} - {self.created_at}>'
    
    @property
    def formatted_date(self):
        """Retourne la date formatée"""
        return self.created_at.strftime('%d/%m/%Y %H:%M:%S')
    
    @property
    def action_display(self):
        """Affichage lisible de l'action"""
        action_map = {
            'login': '🔐 Connexion',
            'logout': '🚪 Déconnexion',
            'create': '➕ Création',
            'update': '✏️ Modification',
            'delete': '🗑️ Suppression',
            'view': '👁️ Consultation',
            'export': '📥 Export',
            'import': '📤 Import',
            'search': '🔍 Recherche',
            'download': '⬇️ Téléchargement',
            'upload': '⬆️ Upload',
        }
        return action_map.get(self.action_type, self.action_type)
    
    @property
    def extra_data_parsed(self):
        """Parse le JSON extra_data"""
        import json
        if self.extra_data:
            try:
                return json.loads(self.extra_data)
            except:
                return {}
        return {}
