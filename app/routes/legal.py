"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from flask import Blueprint, render_template, abort, current_app
from werkzeug.exceptions import HTTPException
from app.models.settings import AppSettings
from app.utils.activity_logger import log_action
import traceback

bp = Blueprint('legal', __name__)

@bp.route('/about')
def about():
    """Page à propos"""
    try:
        legal_pages_enabled = AppSettings.get('legal_pages_enabled', {})
        if not legal_pages_enabled.get('about', False):
            abort(404)
        
        legal_pages = AppSettings.get('legal_pages', {})
        content = legal_pages.get('about_page', '')
        
        return render_template('legal/about.html', content=content)
    except HTTPException:
        # Laisser les erreurs HTTP (404, 500, etc.) se propager normalement
        raise
    except Exception as e:
        error_trace = traceback.format_exc()
        current_app.logger.error(f"Erreur page about: {str(e)}\n{error_trace}")
        log_action('error', f"Erreur affichage page about: {str(e)}", 
                   status='error', error_message=str(e),
                   extra_data={'stack_trace': error_trace, 'page': 'about'})
        abort(500)

@bp.route('/legal/terms')
def terms():
    """Conditions Générales d'Utilisation (CGU)"""
    try:
        legal_pages_enabled = AppSettings.get('legal_pages_enabled', {})
        if not legal_pages_enabled.get('terms', False):
            abort(404)
        
        legal_pages = AppSettings.get('legal_pages', {})
        content = legal_pages.get('terms_page', '')
        
        return render_template('legal/terms.html', content=content)
    except HTTPException:
        # Laisser les erreurs HTTP (404, 500, etc.) se propager normalement
        raise
    except Exception as e:
        error_trace = traceback.format_exc()
        current_app.logger.error(f"Erreur page terms: {str(e)}\n{error_trace}")
        log_action('error', f"Erreur affichage page terms: {str(e)}", 
                   status='error', error_message=str(e),
                   extra_data={'stack_trace': error_trace, 'page': 'terms'})
        abort(500)

@bp.route('/legal/privacy')
def privacy():
    """Politique de confidentialité"""
    try:
        legal_pages_enabled = AppSettings.get('legal_pages_enabled', {})
        if not legal_pages_enabled.get('privacy', False):
            abort(404)
        
        legal_pages = AppSettings.get('legal_pages', {})
        content = legal_pages.get('privacy_page', '')
        
        return render_template('legal/privacy.html', content=content)
    except HTTPException:
        # Laisser les erreurs HTTP (404, 500, etc.) se propager normalement
        raise
    except Exception as e:
        error_trace = traceback.format_exc()
        current_app.logger.error(f"Erreur page privacy: {str(e)}\n{error_trace}")
        log_action('error', f"Erreur affichage page privacy: {str(e)}", 
                   status='error', error_message=str(e),
                   extra_data={'stack_trace': error_trace, 'page': 'privacy'})
        abort(500)

@bp.route('/legal/cookies')
def cookies():
    """Politique des cookies"""
    try:
        legal_pages_enabled = AppSettings.get('legal_pages_enabled', {})
        if not legal_pages_enabled.get('cookies', False):
            abort(404)
        
        legal_pages = AppSettings.get('legal_pages', {})
        content = legal_pages.get('cookies_page', '')
        
        return render_template('legal/cookies.html', content=content)
    except HTTPException:
        # Laisser les erreurs HTTP (404, 500, etc.) se propager normalement
        raise
    except Exception as e:
        error_trace = traceback.format_exc()
        current_app.logger.error(f"Erreur page cookies: {str(e)}\n{error_trace}")
        log_action('error', f"Erreur affichage page cookies: {str(e)}", 
                   status='error', error_message=str(e),
                   extra_data={'stack_trace': error_trace, 'page': 'cookies'})
        abort(500)

@bp.route('/legal/mentions')
def mentions():
    """Mentions légales"""
    try:
        legal_pages_enabled = AppSettings.get('legal_pages_enabled', {})
        if not legal_pages_enabled.get('mentions', False):
            abort(404)
        
        legal_pages = AppSettings.get('legal_pages', {})
        content = legal_pages.get('mentions_page', '')
        
        company_info = {
            'company_name': legal_pages.get('company_name', ''),
            'company_type': legal_pages.get('company_type', ''),
            'registration_number': legal_pages.get('registration_number', ''),
            'capital': legal_pages.get('capital', ''),
            'company_address': legal_pages.get('company_address', ''),
            'director_name': legal_pages.get('director_name', ''),
            'hosting_provider': legal_pages.get('hosting_provider', ''),
            'hosting_phone': legal_pages.get('hosting_phone', '')
        }
        
        return render_template('legal/mentions.html', content=content, company_info=company_info)
    except HTTPException:
        # Laisser les erreurs HTTP (404, 500, etc.) se propager normalement
        raise
    except Exception as e:
        error_trace = traceback.format_exc()
        current_app.logger.error(f"Erreur page mentions: {str(e)}\n{error_trace}")
        log_action('error', f"Erreur affichage page mentions: {str(e)}", 
                   status='error', error_message=str(e),
                   extra_data={'stack_trace': error_trace, 'page': 'mentions'})
        abort(500)
