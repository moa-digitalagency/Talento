"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from flask import Blueprint, render_template, abort
from app.models.settings import AppSettings

bp = Blueprint('legal', __name__)

@bp.route('/about')
def about():
    """Page à propos"""
    legal_pages_enabled = AppSettings.get('legal_pages_enabled', {})
    if not legal_pages_enabled.get('about', False):
        abort(404)
    
    legal_pages = AppSettings.get('legal_pages', {})
    content = legal_pages.get('about_page', '')
    
    return render_template('legal/about.html', content=content)

@bp.route('/legal/terms')
def terms():
    """Conditions Générales d'Utilisation (CGU)"""
    legal_pages_enabled = AppSettings.get('legal_pages_enabled', {})
    if not legal_pages_enabled.get('terms', False):
        abort(404)
    
    legal_pages = AppSettings.get('legal_pages', {})
    content = legal_pages.get('terms_page', '')
    
    return render_template('legal/terms.html', content=content)

@bp.route('/legal/privacy')
def privacy():
    """Politique de confidentialité"""
    legal_pages_enabled = AppSettings.get('legal_pages_enabled', {})
    if not legal_pages_enabled.get('privacy', False):
        abort(404)
    
    legal_pages = AppSettings.get('legal_pages', {})
    content = legal_pages.get('privacy_page', '')
    
    return render_template('legal/privacy.html', content=content)

@bp.route('/legal/cookies')
def cookies():
    """Politique des cookies"""
    legal_pages_enabled = AppSettings.get('legal_pages_enabled', {})
    if not legal_pages_enabled.get('cookies', False):
        abort(404)
    
    legal_pages = AppSettings.get('legal_pages', {})
    content = legal_pages.get('cookies_page', '')
    
    return render_template('legal/cookies.html', content=content)

@bp.route('/legal/mentions')
def mentions():
    """Mentions légales"""
    legal_pages_enabled = AppSettings.get('legal_pages_enabled', {})
    if not legal_pages_enabled.get('mentions', False):
        abort(404)
    
    legal_pages = AppSettings.get('legal_pages', {})
    content = legal_pages.get('mentions_page', '')
    
    return render_template('legal/mentions.html', content=content)
