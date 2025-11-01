"""
Middleware de logging automatique pour enregistrer les activités utilisateurs
Enregistre automatiquement toutes les consultations de pages et actions
"""
from functools import wraps
from flask import request, g
from flask_login import current_user
from app import db
from app.models.activity_log import ActivityLog
from user_agents import parse
import json
from datetime import datetime


class ActivityLogger:
    """Classe pour gérer le logging automatique des activités"""
    
    @staticmethod
    def _get_client_info():
        """Extraire les informations du client (IP, user agent, device info, etc.)"""
        try:
            user_agent_string = request.headers.get('User-Agent', '')
            user_agent = parse(user_agent_string)
            
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
        except Exception as e:
            print(f"⚠️ Erreur lors de l'extraction des infos client: {e}")
            return {
                'ip_address': request.remote_addr or 'Unknown',
                'user_agent': request.headers.get('User-Agent', ''),
                'browser': None,
                'browser_version': None,
                'device_type': 'desktop',
                'device_brand': None,
                'device_model': None,
                'operating_system': None,
                'os_version': None,
                'request_method': request.method,
                'request_url': request.url,
                'request_referrer': request.referrer
            }
    
    @staticmethod
    def _is_static_resource(path):
        """Vérifier si la requête concerne un fichier statique"""
        static_extensions = [
            '.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.ico', 
            '.svg', '.woff', '.woff2', '.ttf', '.eot', '.map',
            '.webp', '.mp4', '.webm', '.ogg', '.mp3', '.wav'
        ]
        
        static_paths = ['/static/', '/favicon.ico']
        
        for ext in static_extensions:
            if path.lower().endswith(ext):
                return True
        
        for static_path in static_paths:
            if static_path in path:
                return True
        
        return False
    
    @staticmethod
    def _should_log_request():
        """Déterminer si la requête doit être loggée"""
        if ActivityLogger._is_static_resource(request.path):
            return False
        
        if request.path.startswith('/api/') and request.path.endswith('/logs'):
            return False
        
        return True
    
    @staticmethod
    def _create_log_entry(user, action_type, action_category, description, 
                         resource_type=None, resource_id=None, status='success', 
                         error_message=None, extra_data=None):
        """
        Créer une entrée de log dans la base de données
        Gestion gracieuse des erreurs pour ne pas impacter l'application
        """
        try:
            client_info = ActivityLogger._get_client_info()
            
            activity_log = ActivityLog(
                user_id=user.id if user and hasattr(user, 'id') else None,
                username=f"{user.first_name} {user.last_name}" if user and hasattr(user, 'first_name') else "Anonyme",
                user_email=user.email if user and hasattr(user, 'email') else None,
                user_code=user.unique_code if user and hasattr(user, 'unique_code') else None,
                action_type=action_type,
                action_category=action_category,
                action_description=description,
                resource_type=resource_type,
                resource_id=resource_id,
                status=status,
                error_message=error_message,
                extra_data=json.dumps(extra_data) if extra_data else None,
                **client_info
            )
            
            db.session.add(activity_log)
            db.session.commit()
            
            return activity_log
        except Exception as e:
            try:
                db.session.rollback()
            except:
                pass
            print(f"⚠️ Erreur logging (non-bloquante): {e}")
            return None


def log_activity(action_type, action_category, resource_type=None):
    """
    Decorator pour logger automatiquement une action
    
    Usage:
        @log_activity('create', 'cinema', 'Production')
        def create_production():
            ...
    
    Args:
        action_type: Type d'action (create, update, delete, view, etc.)
        action_category: Catégorie (auth, cinema, production, project, talent, settings, etc.)
        resource_type: Type de ressource concernée (optionnel)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = current_user if current_user.is_authenticated else None
            
            try:
                result = f(*args, **kwargs)
                
                description = f"{action_type.capitalize()} - {f.__name__}"
                
                try:
                    ActivityLogger._create_log_entry(
                        user=user,
                        action_type=action_type,
                        action_category=action_category,
                        description=description,
                        resource_type=resource_type,
                        status='success'
                    )
                except Exception as log_error:
                    print(f"⚠️ Erreur lors du logging (non-bloquante): {log_error}")
                
                return result
            
            except Exception as e:
                description = f"{action_type.capitalize()} - {f.__name__} (échec)"
                
                try:
                    ActivityLogger._create_log_entry(
                        user=user,
                        action_type=action_type,
                        action_category=action_category,
                        description=description,
                        resource_type=resource_type,
                        status='error',
                        error_message=str(e)
                    )
                except Exception as log_error:
                    print(f"⚠️ Erreur lors du logging d'erreur (non-bloquante): {log_error}")
                
                raise
        
        return decorated_function
    return decorator


def log_page_view(url=None, user=None):
    """
    Logger une consultation de page
    
    Args:
        url: URL de la page (optionnel, utilise request.url par défaut)
        user: Utilisateur (optionnel, utilise current_user par défaut)
    """
    try:
        if user is None:
            user = current_user if current_user.is_authenticated else None
        
        if url is None:
            url = request.url if request else 'Unknown'
        
        page_name = request.path if request else url
        
        ActivityLogger._create_log_entry(
            user=user,
            action_type='view',
            action_category='navigation',
            description=f"Consultation de page: {page_name}",
            resource_type='page',
            status='success'
        )
    except Exception as e:
        print(f"⚠️ Erreur log_page_view (non-bloquante): {e}")


def log_action(action_type, description, resource_type=None, resource_id=None, 
               status='success', error_message=None, user=None, extra_data=None):
    """
    Logger une action personnalisée
    
    Args:
        action_type: Type d'action (create, update, delete, etc.)
        description: Description de l'action
        resource_type: Type de ressource concernée (optionnel)
        resource_id: ID de la ressource (optionnel)
        status: Statut (success, error, warning)
        error_message: Message d'erreur si status = error (optionnel)
        user: Utilisateur (optionnel, utilise current_user par défaut)
        extra_data: Données supplémentaires (dict, optionnel)
    """
    try:
        if user is None:
            user = current_user if current_user.is_authenticated else None
        
        action_category = 'general'
        if resource_type:
            resource_type_lower = resource_type.lower()
            if 'cinema' in resource_type_lower or 'production' in resource_type_lower:
                action_category = 'cinema'
            elif 'project' in resource_type_lower:
                action_category = 'project'
            elif 'talent' in resource_type_lower:
                action_category = 'talent'
            elif 'user' in resource_type_lower:
                action_category = 'user'
            elif 'settings' in resource_type_lower or 'setting' in resource_type_lower:
                action_category = 'settings'
        
        ActivityLogger._create_log_entry(
            user=user,
            action_type=action_type,
            action_category=action_category,
            description=description,
            resource_type=resource_type,
            resource_id=resource_id,
            status=status,
            error_message=error_message,
            extra_data=extra_data
        )
    except Exception as e:
        print(f"⚠️ Erreur log_action (non-bloquante): {e}")


def log_settings_change(setting_name, old_value, new_value, user=None):
    """
    Logger un changement de paramètres
    
    Args:
        setting_name: Nom du paramètre modifié
        old_value: Ancienne valeur
        new_value: Nouvelle valeur
        user: Utilisateur (optionnel, utilise current_user par défaut)
    """
    try:
        if user is None:
            user = current_user if current_user.is_authenticated else None
        
        description = f"Modification du paramètre '{setting_name}'"
        
        extra_data = {
            'setting_name': setting_name,
            'old_value': str(old_value)[:200] if old_value else None,
            'new_value': str(new_value)[:200] if new_value else None,
            'changed_at': datetime.utcnow().isoformat()
        }
        
        ActivityLogger._create_log_entry(
            user=user,
            action_type='update',
            action_category='settings',
            description=description,
            resource_type='AppSettings',
            status='success',
            extra_data=extra_data
        )
    except Exception as e:
        print(f"⚠️ Erreur log_settings_change (non-bloquante): {e}")


def init_activity_logging_middleware(app):
    """
    Initialiser le middleware de logging automatique
    À appeler dans app/__init__.py après l'initialisation de la BDD
    
    Args:
        app: Instance Flask
    """
    @app.before_request
    def log_request():
        """Logger automatiquement les requêtes entrantes"""
        if not ActivityLogger._should_log_request():
            return
        
        g.request_start_time = datetime.utcnow()
    
    @app.after_request
    def log_response(response):
        """Logger automatiquement les réponses après traitement"""
        try:
            if not ActivityLogger._should_log_request():
                return response
            
            user = current_user if current_user.is_authenticated else None
            method = request.method
            path = request.path
            status_code = response.status_code
            
            if method == 'GET' and 200 <= status_code < 300:
                log_page_view(url=request.url, user=user)
            
            elif method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                action_type_map = {
                    'POST': 'create',
                    'PUT': 'update',
                    'PATCH': 'update',
                    'DELETE': 'delete'
                }
                
                action_type = action_type_map.get(method, 'action')
                
                action_category = 'general'
                if '/cinema/' in path:
                    action_category = 'cinema'
                elif '/production/' in path:
                    action_category = 'production'
                elif '/project/' in path:
                    action_category = 'project'
                elif '/talent/' in path:
                    action_category = 'talent'
                elif '/admin/' in path:
                    action_category = 'admin'
                elif '/auth/' in path:
                    action_category = 'auth'
                elif '/settings/' in path:
                    action_category = 'settings'
                
                status = 'success' if 200 <= status_code < 300 else ('error' if status_code >= 400 else 'warning')
                
                description = f"{method} {path} - Status {status_code}"
                
                try:
                    ActivityLogger._create_log_entry(
                        user=user,
                        action_type=action_type,
                        action_category=action_category,
                        description=description,
                        status=status
                    )
                except Exception as log_error:
                    print(f"⚠️ Erreur logging response (non-bloquante): {log_error}")
        
        except Exception as e:
            print(f"⚠️ Erreur dans after_request logging (non-bloquante): {e}")
        
        return response
    
    app.logger.info("✅ Middleware de logging automatique initialisé")
