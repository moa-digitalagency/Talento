from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('cinema', __name__, url_prefix='/cinema')

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard CINEMA - Aperçu général du module cinéma"""
    return render_template('cinema/dashboard.html')

@bp.route('/talents')
@login_required
def talents():
    """Talents CINEMA - Gestion des talents spécifiques au cinéma"""
    return render_template('cinema/talents.html')
