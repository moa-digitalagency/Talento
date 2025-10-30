"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from flask import request, jsonify, current_app
from app.routes.api_v1 import bp
from flask_login import current_user
import json

@bp.route('/log-client-error', methods=['POST'])
def log_client_error():
    """
    Endpoint pour recevoir et logger les erreurs JavaScript côté client
    """
    try:
        # Récupérer les données de l'erreur - gérer à la fois JSON et form data
        data = request.get_json(silent=True)
        
        # Fallback pour les données envoyées en text/plain ou form data
        if not data:
            try:
                # Tenter de parser le body directement
                data = json.loads(request.data.decode('utf-8'))
            except (ValueError, UnicodeDecodeError):
                data = request.form.to_dict()
        
        if not data:
            current_app.logger.warning(f'Client error endpoint called with no data. Content-Type: {request.content_type}')
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Informations sur l'erreur
        error_type = data.get('type', 'unknown')
        error_message = data.get('message', 'No message')
        error_url = data.get('url', 'unknown')
        error_stack = data.get('stack', None)
        error_filename = data.get('filename', None)
        error_line = data.get('line', None)
        
        # Informations utilisateur si disponible
        user_info = 'Anonymous'
        if current_user and current_user.is_authenticated:
            user_info = f"{current_user.first_name} {current_user.last_name} ({current_user.email})"
        
        # Logger l'erreur dans les logs applicatifs
        log_message = f"""
CLIENT ERROR DETECTED
--------------------
Type: {error_type}
Message: {error_message}
URL: {error_url}
File: {error_filename}:{error_line}
User: {user_info}
User Agent: {request.headers.get('User-Agent', 'Unknown')}
IP: {request.remote_addr}
"""
        
        if error_stack:
            log_message += f"\nStack Trace:\n{error_stack}"
        
        current_app.logger.error(log_message)
        
        # Logger dans la base de données via LoggingService si l'utilisateur est connecté
        if current_user and current_user.is_authenticated:
            try:
                from app.services.logging_service import LoggingService
                
                LoggingService.log_activity(
                    user=current_user,
                    action_type='client_error',
                    action_category='frontend',
                    description=f'{error_type}: {error_message}',
                    status='error',
                    error_message=error_message,
                    metadata={
                        'error_type': error_type,
                        'url': error_url,
                        'filename': error_filename,
                        'line': error_line,
                        'stack': error_stack[:500] if error_stack else None  # Limiter la taille
                    }
                )
            except Exception as e:
                current_app.logger.warning(f'Failed to log client error to database: {e}')
        
        return jsonify({
            'success': True,
            'message': 'Error logged successfully'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error in log_client_error endpoint: {e}')
        return jsonify({
            'success': False,
            'error': 'Failed to log error'
        }), 500
