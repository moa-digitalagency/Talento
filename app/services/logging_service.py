"""
Service de logging pour enregistrer les activités et événements de sécurité
"""
from app import db
from app.models.activity_log import ActivityLog
from app.models.security_log import SecurityLog
from flask import request
from datetime import datetime
import json
from user_agents import parse


class LoggingService:
    """Service pour enregistrer les logs d'activité et de sécurité"""
    
    @staticmethod
    def _get_client_info():
        """Extraire les informations du client (IP, user agent, etc.)"""
        user_agent_string = request.headers.get('User-Agent', '')
        user_agent = parse(user_agent_string)
        
        # Récupérer l'IP réelle (prendre en compte les proxies)
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip_address and ',' in ip_address:
            ip_address = ip_address.split(',')[0].strip()
        
        return {
            'ip_address': ip_address or 'Unknown',
            'user_agent': user_agent_string,
            'browser': user_agent.browser.family,
            'browser_version': user_agent.browser.version_string,
            'device_type': 'mobile' if user_agent.is_mobile else ('tablet' if user_agent.is_tablet else 'desktop'),
            'device_brand': user_agent.device.brand or None,
            'device_model': user_agent.device.model or None,
            'operating_system': user_agent.os.family,
            'os_version': user_agent.os.version_string,
            'request_method': request.method,
            'request_url': request.url,
            'request_referrer': request.referrer
        }
    
    @staticmethod
    def log_activity(user, action_type, action_category, description, 
                    resource_type=None, resource_id=None, status='success', 
                    error_message=None, metadata=None):
        """
        Enregistrer une activité utilisateur
        
        Args:
            user: Objet User ou None
            action_type: Type d'action (login, create, update, delete, etc.)
            action_category: Catégorie (auth, cinema, production, etc.)
            description: Description de l'action
            resource_type: Type de ressource concernée (optionnel)
            resource_id: ID de la ressource concernée (optionnel)
            status: Statut de l'action (success, error, warning)
            error_message: Message d'erreur si status = error
            metadata: Données supplémentaires (dict)
        """
        try:
            client_info = LoggingService._get_client_info()
            
            activity_log = ActivityLog(
                user_id=user.id if user else None,
                username=f"{user.first_name} {user.last_name}" if user else "Anonyme",
                user_email=user.email if user else None,
                user_code=user.unique_code if user else None,
                action_type=action_type,
                action_category=action_category,
                action_description=description,
                resource_type=resource_type,
                resource_id=resource_id,
                status=status,
                error_message=error_message,
                extra_data=json.dumps(metadata) if metadata else None,
                **client_info
            )
            
            db.session.add(activity_log)
            db.session.commit()
            
            return activity_log
        except Exception as e:
            print(f"❌ Erreur lors de l'enregistrement de l'activité: {e}")
            db.session.rollback()
            return None
    
    @staticmethod
    def log_security_event(event_type, description, severity='info', 
                          user=None, attempted_username=None, 
                          action_taken=None, metadata=None):
        """
        Enregistrer un événement de sécurité
        
        Args:
            event_type: Type d'événement (failed_login, suspicious_activity, etc.)
            description: Description de l'événement
            severity: Sévérité (info, warning, critical)
            user: Objet User ou None
            attempted_username: Nom d'utilisateur tenté (pour échecs de connexion)
            action_taken: Action prise (account_locked, ip_blocked, etc.)
            metadata: Données supplémentaires (dict)
        """
        try:
            client_info = LoggingService._get_client_info()
            
            security_log = SecurityLog(
                event_type=event_type,
                severity=severity,
                description=description,
                user_id=user.id if user else None,
                attempted_username=attempted_username,
                action_taken=action_taken,
                extra_data=json.dumps(metadata) if metadata else None,
                ip_address=client_info['ip_address'],
                user_agent=client_info['user_agent'],
                browser=client_info['browser'],
                device_type=client_info['device_type'],
                operating_system=client_info['operating_system'],
                request_url=client_info['request_url'],
                request_method=client_info['request_method']
            )
            
            db.session.add(security_log)
            db.session.commit()
            
            return security_log
        except Exception as e:
            print(f"❌ Erreur lors de l'enregistrement de l'événement de sécurité: {e}")
            db.session.rollback()
            return None
    
    @staticmethod
    def get_user_activities(user_id, limit=50):
        """Récupérer les activités d'un utilisateur"""
        return ActivityLog.query.filter_by(user_id=user_id)\
            .order_by(ActivityLog.created_at.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_recent_activities(limit=100):
        """Récupérer les activités récentes"""
        return ActivityLog.query\
            .order_by(ActivityLog.created_at.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_security_logs(severity=None, limit=100):
        """Récupérer les logs de sécurité"""
        query = SecurityLog.query
        
        if severity:
            query = query.filter_by(severity=severity)
        
        return query.order_by(SecurityLog.created_at.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_failed_login_attempts(ip_address=None, hours=24):
        """Récupérer les tentatives de connexion échouées"""
        from datetime import timedelta
        since = datetime.utcnow() - timedelta(hours=hours)
        
        query = SecurityLog.query.filter(
            SecurityLog.event_type == 'failed_login',
            SecurityLog.created_at >= since
        )
        
        if ip_address:
            query = query.filter_by(ip_address=ip_address)
        
        return query.count()
