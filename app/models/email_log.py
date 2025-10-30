"""
Modèle pour logger tous les emails envoyés par le système
"""
from datetime import datetime
from app import db

class EmailLog(db.Model):
    """Modèle pour logger tous les emails envoyés"""
    __tablename__ = 'email_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    recipient_email = db.Column(db.String(255), nullable=False, index=True)
    recipient_name = db.Column(db.String(255))
    subject = db.Column(db.String(500), nullable=False)
    template_type = db.Column(db.String(100), nullable=False, index=True)
    html_content = db.Column(db.Text)
    status = db.Column(db.String(50), default='sent', index=True)
    error_message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    sent_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relations optionnelles pour tracer le contexte
    related_talent_code = db.Column(db.String(50))
    related_project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    related_cinema_talent_id = db.Column(db.Integer, db.ForeignKey('cinema_talents.id'))
    
    # Configuration de l'email (enabled/disabled)
    is_enabled = db.Column(db.Boolean, default=True)
    
    # Relations
    sent_by = db.relationship('User', backref=db.backref('sent_emails', lazy='dynamic'))
    related_project = db.relationship('Project', backref=db.backref('notification_emails', lazy='dynamic'))
    related_cinema_talent = db.relationship('CinemaTalent', backref=db.backref('notification_emails', lazy='dynamic'))
    
    def __repr__(self):
        return f'<EmailLog {self.recipient_email} - {self.template_type} - {self.status}>'
    
    @staticmethod
    def is_template_enabled(template_type):
        """Vérifier si un type de template est activé"""
        from app.models.settings import AppSettings
        email_settings = AppSettings.get('email_notifications_config', {})
        if not email_settings:
            return True
        return email_settings.get(template_type, {}).get('enabled', True)
    
    @staticmethod
    def get_template_config(template_type):
        """Récupérer la configuration d'un template"""
        from app.models.settings import AppSettings
        email_settings = AppSettings.get('email_notifications_config', {})
        return email_settings.get(template_type, {
            'enabled': True,
            'name': template_type,
            'description': 'Notification par email'
        })
