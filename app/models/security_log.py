"""
Modèle pour les logs de sécurité
Enregistre tous les événements de sécurité
"""
from datetime import datetime
from app import db


class SecurityLog(db.Model):
    """Modèle pour enregistrer tous les événements de sécurité"""
    __tablename__ = 'security_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Type d'événement de sécurité
    event_type = db.Column(db.String(100), nullable=False)  # failed_login, suspicious_activity, password_change, etc.
    severity = db.Column(db.String(20), default='info')  # info, warning, critical
    
    # Utilisateur concerné (peut être null pour tentatives échouées)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', foreign_keys=[user_id], backref='security_logs')
    attempted_username = db.Column(db.String(200))  # Email ou code utilisé lors de la tentative
    
    # Informations de connexion
    ip_address = db.Column(db.String(45), nullable=False)  # IPv4 ou IPv6
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    
    # Périphérique
    user_agent = db.Column(db.Text)
    browser = db.Column(db.String(100))
    device_type = db.Column(db.String(50))
    operating_system = db.Column(db.String(100))
    
    # Détails de l'événement
    description = db.Column(db.Text, nullable=False)
    request_url = db.Column(db.String(500))
    request_method = db.Column(db.String(10))
    
    # Données supplémentaires (JSON)
    extra_data = db.Column(db.Text)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Actions prises
    action_taken = db.Column(db.String(200))  # account_locked, ip_blocked, alert_sent, etc.
    resolved = db.Column(db.Boolean, default=False)
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    resolved_by_user = db.relationship('User', foreign_keys=[resolved_by])
    resolution_notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<SecurityLog {self.event_type} - {self.severity} - {self.created_at}>'
    
    @property
    def formatted_date(self):
        """Retourne la date formatée"""
        return self.created_at.strftime('%d/%m/%Y %H:%M:%S')
    
    @property
    def severity_display(self):
        """Affichage lisible de la sévérité"""
        severity_map = {
            'info': '📘 Info',
            'warning': '⚠️ Avertissement',
            'critical': '🚨 Critique'
        }
        return severity_map.get(self.severity, self.severity)
    
    @property
    def event_display(self):
        """Affichage lisible de l'événement"""
        event_map = {
            'failed_login': '🔐 Échec de connexion',
            'successful_login': '✅ Connexion réussie',
            'password_change': '🔑 Changement de mot de passe',
            'account_locked': '🔒 Compte verrouillé',
            'suspicious_activity': '⚠️ Activité suspecte',
            'unauthorized_access': '🚫 Accès non autorisé',
            'data_breach_attempt': '🛡️ Tentative de violation de données',
            'brute_force_attempt': '⚔️ Tentative de force brute',
            'session_hijack_attempt': '🕵️ Tentative de piratage de session',
        }
        return event_map.get(self.event_type, self.event_type)
