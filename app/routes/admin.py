from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, jsonify, current_app, after_this_request
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime
from sqlalchemy import or_, and_, func
from urllib.parse import urlparse, urljoin
from app import db
from app.models.user import User
from app.models.talent import Talent, UserTalent
from app.models.location import Country, City
from app.models.settings import AppSettings
from app.services.export_service import ExportService
from app.services.cv_analyzer import CVAnalyzerService
from app.services.email_service import EmailService
from app.services.database_service import DatabaseService
from app.services.update_service import UpdateService
from app.services.backup_service import BackupService
from app.services.seo_service import SEOService
from app.services.maintenance_service import MaintenanceService
import io
import os
import shutil
import secrets
import string

def is_safe_url(target):
    """Vérifie qu'une URL est sûre pour la redirection (même domaine)"""
    if not target:
        return False
    ref_url = urlparse(urljoin(request.host_url, target))
    test_url = urlparse(request.host_url)
    return ref_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Accès réservé aux administrateurs.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def recruiter_or_admin_required(f):
    """Décorateur pour vérifier que l'utilisateur a le rôle 'recruteur' ou est admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Veuillez vous connecter pour accéder à cette page.', 'error')
            return redirect(url_for('auth.login'))
        
        if not (current_user.is_admin or current_user.role == 'recruteur'):
            flash('Vous n\'avez pas les droits d\'accès à cette section.', 'error')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function

# Rediriger l'ancien /admin/dashboard vers /
@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return redirect(url_for('main.index'))

@bp.route('/users')
@login_required
@recruiter_or_admin_required
def users():
    search_query = request.args.get('search', '').strip()
    search_code = request.args.get('search_code', '').strip()
    availability_filter = request.args.get('availability')
    work_mode_filter = request.args.get('work_mode')
    gender_filter = request.args.get('gender')
    city_filter = request.args.get('city')
    talent_filter = request.args.getlist('talent')
    
    query = User.query.filter(User.is_admin == False)
    
    if search_query:
        search_pattern = f'%{search_query}%'
        query = query.filter(
            or_(
                User.first_name.ilike(search_pattern),
                User.last_name.ilike(search_pattern),
                User.email.ilike(search_pattern)
            )
        )
    
    if search_code:
        code_clean = search_code.replace('-', '').upper()
        query = query.filter(User.unique_code.ilike(f'%{code_clean}%'))
    
    if availability_filter:
        query = query.filter(User.availability == availability_filter)
    
    if work_mode_filter:
        query = query.filter(User.work_mode == work_mode_filter)
    
    if gender_filter:
        query = query.filter(User.gender == gender_filter)
    
    if city_filter:
        query = query.filter(User.city_id == int(city_filter))
    
    if talent_filter:
        talent_ids = [int(tid) for tid in talent_filter]
        query = query.join(User.talents).filter(UserTalent.talent_id.in_(talent_ids)).group_by(User.id).having(func.count(func.distinct(UserTalent.talent_id)) == len(talent_ids))
    
    all_users = query.order_by(User.created_at.desc()).all()
    
    all_talents = Talent.query.order_by(Talent.category, Talent.name).all()
    all_cities = City.query.order_by(City.name).all()
    
    return render_template('admin/users.html', users=all_users, talents=all_talents, cities=all_cities)


@bp.route('/user/<int:user_id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_active(user_id):
    user = User.query.get_or_404(user_id)
    user.account_active = not user.account_active
    db.session.commit()
    flash(f"Compte {'activé' if user.account_active else 'désactivé'} avec succès.", 'success')
    return redirect(url_for('main.index'))

@bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('Impossible de supprimer un compte administrateur.', 'error')
        next_page = request.referrer if is_safe_url(request.referrer) else url_for('main.index')
        return redirect(next_page)
    
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé avec succès.', 'success')
    next_page = request.referrer if is_safe_url(request.referrer) else url_for('main.index')
    return redirect(next_page)

@bp.route('/export/excel')
@login_required
@recruiter_or_admin_required
def export_excel():
    users = User.query.filter(User.is_admin == False).all()
    excel_bytes = ExportService.export_to_excel(users)
    
    buffer = io.BytesIO(excel_bytes)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'talento_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    )

@bp.route('/export/csv')
@login_required
@recruiter_or_admin_required
def export_csv():
    users = User.query.filter(User.is_admin == False).all()
    csv_data = ExportService.export_to_csv(users)
    
    buffer = io.BytesIO()
    buffer.write(csv_data.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'talento_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@bp.route('/export/pdf')
@login_required
@recruiter_or_admin_required
def export_pdf():
    try:
        users = User.query.filter(User.is_admin == False).all()
        pdf_bytes = ExportService.export_list_to_pdf(users, current_user=current_user)
        
        from app.services.logging_service import LoggingService
        LoggingService.log_activity(
            user=current_user,
            action_type='export',
            action_category='pdf',
            description=f'Export PDF en lot de {len(users)} utilisateurs',
            resource_type='User',
            status='success'
        )
        
        buffer = io.BytesIO(pdf_bytes)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'talento_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
    except Exception as e:
        from app.services.logging_service import LoggingService
        LoggingService.log_activity(
            user=current_user,
            action_type='export',
            action_category='pdf',
            description='Échec de l\'export PDF en lot des utilisateurs',
            resource_type='User',
            status='error',
            error_message=str(e)
        )
        flash(f'Erreur lors de l\'export PDF: {str(e)}', 'error')
        return redirect(url_for('admin.users'))

@bp.route('/export/pdf/<int:user_id>')
@login_required
@recruiter_or_admin_required
def export_pdf_individual(user_id):
    try:
        user = User.query.get_or_404(user_id)
        pdf_bytes = ExportService.export_talent_card_pdf(user)
        
        from app.services.logging_service import LoggingService
        LoggingService.log_activity(
            user=current_user,
            action_type='export',
            action_category='pdf',
            description=f'Export PDF individuel du profil de {user.first_name} {user.last_name} ({user.unique_code})',
            resource_type='User',
            resource_id=user_id,
            status='success'
        )
        
        buffer = io.BytesIO(pdf_bytes)
        buffer.seek(0)
        
        filename = f'talento_{user.unique_code}_{datetime.now().strftime("%Y%m%d")}.pdf'
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        from app.services.logging_service import LoggingService
        LoggingService.log_activity(
            user=current_user,
            action_type='export',
            action_category='pdf',
            description=f'Échec de l\'export PDF individuel (ID: {user_id})',
            resource_type='User',
            resource_id=user_id,
            status='error',
            error_message=str(e)
        )
        flash(f'Erreur lors de l\'export PDF: {str(e)}', 'error')
        return redirect(url_for('admin.users'))

@bp.route('/analyze-cv/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def analyze_cv(user_id):
    user = User.query.get_or_404(user_id)
    
    if not user.cv_filename:
        return jsonify({'error': 'Aucun CV disponible pour cet utilisateur'}), 400
    
    try:
        analysis = CVAnalyzerService.analyze_cv(user)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/talent/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_talent():
    if request.method == 'POST':
        name = request.form.get('name')
        emoji = request.form.get('emoji')
        category = request.form.get('category')
        
        if not all([name, emoji, category]):
            from app.services.logging_service import LoggingService
            LoggingService.log_activity(
                user=current_user,
                action_type='create',
                action_category='talent',
                description=f'Tentative de création de talent bloquée (champs manquants)',
                resource_type='Talent',
                status='blocked'
            )
            flash('Tous les champs sont requis.', 'error')
            return redirect(url_for('admin.new_talent'))
        
        existing = Talent.query.filter_by(name=name).first()
        if existing:
            from app.services.logging_service import LoggingService
            LoggingService.log_activity(
                user=current_user,
                action_type='create',
                action_category='talent',
                description=f'Tentative de création du talent "{name}" bloquée (doublon)',
                resource_type='Talent',
                status='blocked'
            )
            flash('Ce talent existe déjà.', 'error')
            return redirect(url_for('admin.new_talent'))
        
        try:
            talent = Talent(name=name, emoji=emoji, category=category)
            db.session.add(talent)
            db.session.commit()
            
            from app.services.logging_service import LoggingService
            LoggingService.log_activity(
                user=current_user,
                action_type='create',
                action_category='talent',
                description=f'Création du talent "{name}" ({category})',
                resource_type='Talent',
                resource_id=talent.id,
                status='success'
            )
            
            flash('Talent ajouté avec succès.', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            from app.services.logging_service import LoggingService
            LoggingService.log_activity(
                user=current_user,
                action_type='create',
                action_category='talent',
                description=f'Échec de création du talent "{name}"',
                resource_type='Talent',
                status='error',
                error_message=str(e)
            )
            flash(f'Erreur lors de la création du talent: {str(e)}', 'error')
            return redirect(url_for('admin.new_talent'))
    
    return render_template('admin/talent_form.html')

@bp.route('/talents')
@login_required
@admin_required
def talents_list():
    talents = Talent.query.order_by(Talent.category, Talent.name).all()
    return render_template('admin/talents_list.html', talents=talents)

@bp.route('/talent/<int:talent_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_talent(talent_id):
    talent = Talent.query.get_or_404(talent_id)
    talent_name = talent.name
    
    usage_count = UserTalent.query.filter_by(talent_id=talent_id).count()
    if usage_count > 0:
        from app.services.logging_service import LoggingService
        LoggingService.log_activity(
            user=current_user,
            action_type='delete',
            action_category='talent',
            description=f'Tentative de suppression du talent "{talent_name}" bloquée (utilisé par {usage_count} profil(s))',
            resource_type='Talent',
            resource_id=talent_id,
            status='blocked'
        )
        flash(f'Impossible de supprimer ce talent. Il est utilisé par {usage_count} profil(s).', 'error')
        return redirect(url_for('admin.talents_list'))
    
    db.session.delete(talent)
    db.session.commit()
    
    from app.services.logging_service import LoggingService
    LoggingService.log_activity(
        user=current_user,
        action_type='delete',
        action_category='talent',
        description=f'Suppression du talent "{talent_name}"',
        resource_type='Talent',
        resource_id=talent_id,
        status='success'
    )
    
    flash('Talent supprimé avec succès.', 'success')
    return redirect(url_for('admin.talents_list'))

@bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.first_name = request.form.get('first_name', '').strip()
        user.last_name = request.form.get('last_name', '').strip()
        user.email = request.form.get('email', '').strip()
        
        dob_str = request.form.get('date_of_birth')
        if dob_str:
            try:
                from datetime import datetime as dt
                user.date_of_birth = dt.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        user.gender = request.form.get('gender')
        user.phone = request.form.get('phone', '').strip() or None
        user.whatsapp = request.form.get('whatsapp', '').strip() or None
        user.address = request.form.get('address', '').strip() or None
        
        country_id = request.form.get('country_id')
        user.country_id = int(country_id) if country_id else None
        
        city_id = request.form.get('city_id')
        user.city_id = int(city_id) if city_id else None
        
        user.nationality = request.form.get('nationality', '').strip() or None
        
        residence_country_id = request.form.get('residence_country_id')
        user.residence_country_id = int(residence_country_id) if residence_country_id else None
        
        residence_city_id = request.form.get('residence_city_id')
        user.residence_city_id = int(residence_city_id) if residence_city_id else None
        
        user.availability = request.form.get('availability')
        user.work_mode = request.form.get('work_mode')
        user.rate_range = request.form.get('rate_range', '').strip() or None
        user.years_experience = request.form.get('years_experience') or None
        
        user.bio = request.form.get('bio', '').strip() or None
        user.portfolio_url = request.form.get('portfolio_url', '').strip() or None
        
        user.linkedin = request.form.get('linkedin', '').strip() or None
        user.instagram = request.form.get('instagram', '').strip() or None
        user.twitter = request.form.get('twitter', '').strip() or None
        user.facebook = request.form.get('facebook', '').strip() or None
        user.github = request.form.get('github', '').strip() or None
        user.behance = request.form.get('behance', '').strip() or None
        user.dribbble = request.form.get('dribbble', '').strip() or None
        user.youtube = request.form.get('youtube', '').strip() or None
        
        talent_ids = request.form.getlist('talents')
        UserTalent.query.filter_by(user_id=user.id).delete()
        for talent_id in talent_ids:
            if talent_id:
                user_talent = UserTalent(user_id=user.id, talent_id=int(talent_id))
                db.session.add(user_talent)
        
        db.session.commit()
        flash('Profil mis à jour avec succès.', 'success')
        return redirect(url_for('profile.view', unique_code=user.unique_code))
    
    countries = Country.query.order_by(Country.name).all()
    cities = City.query.order_by(City.name).all()
    all_talents = Talent.query.order_by(Talent.category, Talent.name).all()
    user_talent_ids = [ut.talent_id for ut in user.talents]
    
    return render_template('admin/user_edit.html', 
                         user=user, 
                         countries=countries, 
                         cities=cities,
                         all_talents=all_talents,
                         user_talent_ids=user_talent_ids)

@bp.route('/settings')
@login_required
@admin_required
def settings():
    admin_users = User.query.filter(User.is_admin == True).order_by(User.created_at).all()
    
    sendgrid_key = AppSettings.get('sendgrid_api_key', '') or os.environ.get('SENDGRID_API_KEY', '')
    openrouter_key = AppSettings.get('openrouter_api_key', '') or os.environ.get('OPENROUTER_API_KEY', '')
    sender_email = AppSettings.get('sender_email', 'noreply@myoneart.com')
    
    sendgrid_configured = bool(sendgrid_key)
    openrouter_configured = bool(openrouter_key)
    
    def mask_key(key):
        if not key or len(key) < 8:
            return ''
        return key[:4] + '*' * (len(key) - 8) + key[-4:]
    
    config_info = {
        'sendgrid': sendgrid_configured,
        'openrouter': openrouter_configured,
        'sendgrid_key_masked': mask_key(sendgrid_key) if sendgrid_configured else '',
        'openrouter_key_masked': mask_key(openrouter_key) if openrouter_configured else '',
        'sendgrid_from': sender_email,
        'database_type': 'PostgreSQL' if 'postgresql' in current_app.config.get('SQLALCHEMY_DATABASE_URI', '').lower() else 'SQLite'
    }
    
    db_diagnostics = DatabaseService.get_full_diagnostics()
    git_info = UpdateService.get_git_info()
    update_history = UpdateService.get_update_history(5)
    
    return render_template('admin/settings.html', admin_users=admin_users, config=config_info, db_diagnostics=db_diagnostics, git_info=git_info, update_history=update_history)


@bp.route('/settings/api-keys')
@login_required
@admin_required
def settings_api_keys():
    sendgrid_key = AppSettings.get('sendgrid_api_key', '') or os.environ.get('SENDGRID_API_KEY', '')
    openrouter_key = AppSettings.get('openrouter_api_key', '') or os.environ.get('OPENROUTER_API_KEY', '')
    perplexity_key = AppSettings.get('perplexity_api_key', '')
    openai_key = AppSettings.get('openai_api_key', '')
    gemini_key = AppSettings.get('gemini_api_key', '')
    omdb_key = AppSettings.get('omdb_api_key', '') or os.environ.get('OMDB_API_KEY', '')
    sender_email = AppSettings.get('sender_email', 'noreply@myoneart.com')
    
    # Configuration IA
    ai_provider = AppSettings.get('ai_provider', 'openrouter')
    openrouter_model = AppSettings.get('openrouter_model', 'google/gemini-2.0-flash-001:free')
    perplexity_model = AppSettings.get('perplexity_model', 'sonar')
    openai_model = AppSettings.get('openai_model', 'gpt-4o-mini')
    gemini_model = AppSettings.get('gemini_model', 'gemini-2.0-flash-exp')
    
    sendgrid_configured = bool(sendgrid_key)
    openrouter_configured = bool(openrouter_key)
    perplexity_configured = bool(perplexity_key)
    openai_configured = bool(openai_key)
    gemini_configured = bool(gemini_key)
    omdb_configured = bool(omdb_key)
    
    def mask_key(key):
        if not key or len(key) < 8:
            return ''
        return key[:4] + '*' * (len(key) - 8) + key[-4:]
    
    config_info = {
        'sendgrid': sendgrid_configured,
        'openrouter': openrouter_configured,
        'perplexity': perplexity_configured,
        'openai': openai_configured,
        'gemini': gemini_configured,
        'omdb': omdb_configured,
        'sendgrid_key_masked': mask_key(sendgrid_key) if sendgrid_configured else '',
        'openrouter_key_masked': mask_key(openrouter_key) if openrouter_configured else '',
        'perplexity_key_masked': mask_key(perplexity_key) if perplexity_configured else '',
        'openai_key_masked': mask_key(openai_key) if openai_configured else '',
        'gemini_key_masked': mask_key(gemini_key) if gemini_configured else '',
        'omdb_key_masked': mask_key(omdb_key) if omdb_configured else '',
        'sendgrid_from': sender_email,
        'ai_provider': ai_provider,
        'openrouter_model': openrouter_model,
        'perplexity_model': perplexity_model,
        'openai_model': openai_model,
        'gemini_model': gemini_model
    }
    
    return render_template('admin/settings/api_keys.html', config=config_info)

@bp.route('/settings/email-templates')
@login_required
@admin_required
def settings_email_templates():
    return render_template('admin/settings/email_templates.html')

@bp.route('/settings/email-templates/view/<template_type>')
@login_required
@admin_required
def view_email_template(template_type):
    """Affiche un template email individuel"""
    from app.services.email_service import EmailService
    
    email_service = EmailService()
    
    # Données d'exemple pour l'aperçu
    sample_data = {
        'talent_registration': {
            'full_name': 'Jean Dupont',
            'unique_code': 'MAN0001RAB',
            'email': 'jean.dupont@example.com'
        },
        'cinema_talent_registration': {
            'full_name': 'Marie Martin',
            'unique_code': 'MAV0001CAS',
            'email': 'marie.martin@example.com'
        },
        'ai_talent_match': {
            'full_name': 'Pierre Bernard',
            'job_description': 'Recherche développeur Python avec 3 ans d\'expérience',
            'match_score': 85,
            'match_reason': 'Compétences en Python et expérience correspondante'
        },
        'ai_cinema_match': {
            'full_name': 'Sophie Dubois',
            'role_description': 'Recherche actrice pour rôle principal, 25-35 ans',
            'match_score': 92,
            'match_reason': 'Profil parfait pour le rôle: âge, expérience et compétences'
        },
        'project_selection': {
            'full_name': 'Lucas Martin',
            'project_name': 'Projet Cinéma - La Grande Aventure',
            'role': 'Acteur principal'
        },
        'login_credentials': {
            'full_name': 'Emma Petit',
            'email': 'emma.petit@example.com',
            'unique_code': 'FEM0002PAR',
            'password': 'MotDePasse123!'
        }
    }
    
    # Générer l'aperçu HTML du template
    template_html = email_service.get_template_preview(template_type, sample_data.get(template_type, {}))
    
    if not template_html:
        flash('Template non trouvé', 'error')
        return redirect(url_for('admin.settings_email_notifications'))
    
    # Afficher le template brut dans le navigateur
    return template_html

@bp.route('/settings/email-notifications')
@login_required
@admin_required
def settings_email_notifications():
    """Page de gestion des notifications email et logs"""
    from app.models.email_log import EmailLog
    from sqlalchemy import desc
    
    # Récupérer les paramètres de pagination et filtrage
    page = request.args.get('page', 1, type=int)
    per_page = 50
    template_filter = request.args.get('template', '')
    status_filter = request.args.get('status', '')
    
    # Construire la requête
    query = EmailLog.query
    
    if template_filter:
        query = query.filter(EmailLog.template_type == template_filter)
    
    if status_filter:
        query = query.filter(EmailLog.status == status_filter)
    
    # Pagination
    email_logs = query.order_by(desc(EmailLog.sent_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Statistiques
    total_emails = EmailLog.query.count()
    sent_emails = EmailLog.query.filter_by(status='sent').count()
    failed_emails = EmailLog.query.filter_by(status='failed').count()
    
    # Types de templates disponibles
    template_types = db.session.query(EmailLog.template_type).distinct().all()
    template_types = [t[0] for t in template_types if t[0]]
    
    # Configuration des templates email (enabled/disabled)
    email_config = AppSettings.get('email_notifications_config', {})
    
    # Configuration CC admin
    email_cc_admin = AppSettings.get('email_cc_admin', {})
    
    # Templates disponibles avec leur configuration par défaut
    if not isinstance(email_config, dict):
        email_config = {}
    
    if not isinstance(email_cc_admin, dict):
        email_cc_admin = {}
    
    available_templates = {
        'talent_registration': {
            'name': 'Inscription Talent',
            'description': 'Email envoyé après l\'inscription d\'un nouveau talent',
            'enabled': email_config.get('talent_registration', {}).get('enabled', True) if isinstance(email_config.get('talent_registration'), dict) else True,
            'cc_admin': email_cc_admin.get('talent_registration', False)
        },
        'cinema_talent_registration': {
            'name': 'Inscription Talent Cinéma',
            'description': 'Email envoyé après l\'inscription d\'un nouveau talent cinéma',
            'enabled': email_config.get('cinema_talent_registration', {}).get('enabled', True) if isinstance(email_config.get('cinema_talent_registration'), dict) else True,
            'cc_admin': email_cc_admin.get('cinema_talent_registration', False)
        },
        'ai_talent_match': {
            'name': 'Match IA - Talents',
            'description': 'Notification envoyée aux talents lorsque leur profil correspond à une recherche IA',
            'enabled': email_config.get('ai_talent_match', {}).get('enabled', True) if isinstance(email_config.get('ai_talent_match'), dict) else True,
            'cc_admin': email_cc_admin.get('ai_talent_match', False)
        },
        'ai_cinema_match': {
            'name': 'Match IA - Cinéma',
            'description': 'Notification envoyée aux talents cinéma lorsque leur profil correspond à un rôle',
            'enabled': email_config.get('ai_cinema_match', {}).get('enabled', True) if isinstance(email_config.get('ai_cinema_match'), dict) else True,
            'cc_admin': email_cc_admin.get('ai_cinema_match', False)
        },
        'project_selection': {
            'name': 'Sélection Projet',
            'description': 'Email de confirmation envoyé aux talents sélectionnés pour un projet',
            'enabled': email_config.get('project_selection', {}).get('enabled', True) if isinstance(email_config.get('project_selection'), dict) else True,
            'cc_admin': email_cc_admin.get('project_selection', False)
        },
        'login_credentials': {
            'name': 'Identifiants de Connexion',
            'description': 'Email contenant les identifiants de connexion',
            'enabled': email_config.get('login_credentials', {}).get('enabled', True) if isinstance(email_config.get('login_credentials'), dict) else True,
            'cc_admin': email_cc_admin.get('login_credentials', False)
        },
        'weekly_recap_talents': {
            'name': 'Récapitulatif Hebdomadaire - Talents',
            'description': 'Email récapitulatif des nouvelles inscriptions de talents envoyé chaque dimanche',
            'enabled': email_config.get('weekly_recap_talents', {}).get('enabled', True) if isinstance(email_config.get('weekly_recap_talents'), dict) else True,
            'cc_admin': email_cc_admin.get('weekly_recap_talents', False)
        },
        'weekly_recap_cinema': {
            'name': 'Récapitulatif Hebdomadaire - Talents Cinéma',
            'description': 'Email récapitulatif des nouvelles inscriptions de talents cinéma envoyé chaque dimanche',
            'enabled': email_config.get('weekly_recap_cinema', {}).get('enabled', True) if isinstance(email_config.get('weekly_recap_cinema'), dict) else True,
            'cc_admin': email_cc_admin.get('weekly_recap_cinema', False)
        },
        'name_detection': {
            'name': 'Détection de Nom',
            'description': 'Email de notification lors de la détection d\'un nom existant dans le système',
            'enabled': email_config.get('name_detection', {}).get('enabled', True) if isinstance(email_config.get('name_detection'), dict) else True,
            'cc_admin': email_cc_admin.get('name_detection', False)
        }
    }
    
    stats = {
        'total': total_emails,
        'sent': sent_emails,
        'failed': failed_emails,
        'success_rate': round((sent_emails / total_emails * 100) if total_emails > 0 else 0, 1)
    }
    
    from app.services.database_service import DatabaseService
    db_diagnostics = DatabaseService.get_full_diagnostics()
    
    # Charger le pied de page configuré
    email_footer = AppSettings.get('email_footer', '© 2024 taalentio.com - Plateforme de valorisation des talents\nCeci est un email automatique, merci de ne pas y répondre.')
    
    return render_template('admin/settings/email_notifications.html',
                         email_logs=email_logs,
                         stats=stats,
                         template_types=template_types,
                         available_templates=available_templates,
                         template_filter=template_filter,
                         status_filter=status_filter,
                         db_diagnostics=db_diagnostics,
                         email_footer=email_footer)

@bp.route('/settings/email-notifications/save-footer', methods=['POST'])
@login_required
@admin_required
def save_email_footer():
    """Sauvegarder le pied de page uniforme des emails"""
    email_footer = request.form.get('email_footer', '')
    
    # Sauvegarder dans les paramètres
    AppSettings.set('email_footer', email_footer)
    
    flash('✅ Pied de page des emails mis à jour avec succès', 'success')
    return redirect(url_for('admin.settings_email_notifications'))

@bp.route('/settings/email-notifications/toggle/<template_type>', methods=['POST'])
@login_required
@admin_required
def toggle_email_notification(template_type):
    """Activer/désactiver un type de notification email"""
    from app.models.email_log import EmailLog
    
    # Récupérer la config actuelle
    email_config = AppSettings.get('email_notifications_config', {})
    
    # Initialiser le template s'il n'existe pas
    if template_type not in email_config:
        email_config[template_type] = {}
    
    # Inverser l'état enabled
    current_state = email_config[template_type].get('enabled', True)
    email_config[template_type]['enabled'] = not current_state
    
    # Sauvegarder
    AppSettings.set('email_notifications_config', email_config)
    
    new_state = 'activé' if email_config[template_type]['enabled'] else 'désactivé'
    flash(f'✅ Notification "{template_type}" {new_state}', 'success')
    
    return redirect(url_for('admin.settings_email_notifications'))

@bp.route('/settings/email-notifications/toggle-cc-admin/<template_type>', methods=['POST'])
@login_required
@admin_required
def toggle_email_cc_admin(template_type):
    """Activer/désactiver la copie admin pour un type de notification email"""
    # Récupérer les paramètres actuels
    email_cc_admin = AppSettings.get('email_cc_admin', {})
    
    # Toggle la valeur pour ce template
    current_value = email_cc_admin.get(template_type, False)
    email_cc_admin[template_type] = not current_value
    
    # Sauvegarder
    AppSettings.set('email_cc_admin', email_cc_admin)
    
    status = "activée" if email_cc_admin[template_type] else "désactivée"
    flash(f'✅ Copie admin {status} pour {template_type}', 'success')
    
    return redirect(url_for('admin.settings_email_notifications'))

@bp.route('/settings/email-notifications/<int:log_id>/view')
@login_required
@admin_required
def view_email_log(log_id):
    """Voir le contenu HTML d'un email"""
    from app.models.email_log import EmailLog
    
    email_log = EmailLog.query.get_or_404(log_id)
    return render_template('admin/settings/email_log_detail.html', email_log=email_log)

@bp.route('/settings/customization')
@login_required
@admin_required
def settings_customization():
    """Page de personnalisation du site"""
    from datetime import datetime
    
    # Footer settings
    footer_text = AppSettings.get('footer_text', '')
    footer_contact_email = AppSettings.get('footer_contact_email', '')
    footer_contact_phone = AppSettings.get('footer_contact_phone', '')
    
    # Logo and images
    logo_url = AppSettings.get('logo_url', '')
    favicon_url = AppSettings.get('favicon_url', '')
    hero_image_url = AppSettings.get('hero_image_url', '')
    
    # Social links
    social_links = AppSettings.get('social_links', {})
    
    # Legal pages
    legal_pages = AppSettings.get('legal_pages', {})
    legal_pages_enabled = AppSettings.get('legal_pages_enabled', {
        'terms': False,
        'privacy': False,
        'about': False,
        'cookies': False,
        'mentions': False
    })
    
    return render_template('admin/settings/customization.html',
                         footer_text=footer_text,
                         footer_contact_email=footer_contact_email,
                         footer_contact_phone=footer_contact_phone,
                         logo_url=logo_url,
                         favicon_url=favicon_url,
                         hero_image_url=hero_image_url,
                         social_links=social_links,
                         legal_pages=legal_pages,
                         legal_pages_enabled=legal_pages_enabled,
                         current_year=datetime.now().year)

@bp.route('/settings/customization/save-footer', methods=['POST'])
@login_required
@admin_required
def save_site_footer():
    """Sauvegarder le pied de page du site"""
    footer_text = request.form.get('footer_text', '').strip()
    footer_contact_email = request.form.get('footer_contact_email', '').strip()
    footer_contact_phone = request.form.get('footer_contact_phone', '').strip()
    
    # Sauvegarder dans les paramètres
    AppSettings.set('footer_text', footer_text)
    AppSettings.set('footer_contact_email', footer_contact_email)
    AppSettings.set('footer_contact_phone', footer_contact_phone)
    
    flash('✅ Pied de page du site mis à jour avec succès', 'success')
    return redirect(url_for('admin.settings_customization'))

@bp.route('/settings/customization/save-logo-images', methods=['POST'])
@login_required
@admin_required
def save_logo_images():
    """Sauvegarder le logo et les images"""
    from app.utils.file_handler import FileHandler
    
    # URLs (priorité aux URLs si fournies)
    logo_url = request.form.get('logo_url', '').strip()
    favicon_url = request.form.get('favicon_url', '').strip()
    hero_image_url = request.form.get('hero_image_url', '').strip()
    
    # Gestion des fichiers uploadés
    logo_file = request.files.get('logo_file')
    favicon_file = request.files.get('favicon_file')
    hero_image_file = request.files.get('hero_image_file')
    
    try:
        # Upload logo si fourni
        if logo_file and logo_file.filename:
            result = FileHandler.save_uploaded_file(logo_file, 'logos', allowed_extensions=['png', 'jpg', 'jpeg', 'svg', 'gif'])
            if result['success']:
                logo_url = f"/static/uploads/logos/{result['filename']}"
        
        # Upload favicon si fourni
        if favicon_file and favicon_file.filename:
            result = FileHandler.save_uploaded_file(favicon_file, 'favicons', allowed_extensions=['ico', 'png'])
            if result['success']:
                favicon_url = f"/static/uploads/favicons/{result['filename']}"
        
        # Upload hero image si fourni
        if hero_image_file and hero_image_file.filename:
            result = FileHandler.save_uploaded_file(hero_image_file, 'hero_images', allowed_extensions=['png', 'jpg', 'jpeg', 'webp'])
            if result['success']:
                hero_image_url = f"/static/uploads/hero_images/{result['filename']}"
        
        # Sauvegarder les URLs
        AppSettings.set('logo_url', logo_url)
        AppSettings.set('favicon_url', favicon_url)
        AppSettings.set('hero_image_url', hero_image_url)
        
        flash('✅ Logo et images mis à jour avec succès', 'success')
    except Exception as e:
        flash(f'❌ Erreur lors de la sauvegarde des images: {str(e)}', 'error')
    
    return redirect(url_for('admin.settings_customization'))

@bp.route('/settings/customization/save-social-links', methods=['POST'])
@login_required
@admin_required
def save_social_links():
    """Sauvegarder les liens réseaux sociaux"""
    social_links = {
        'facebook': request.form.get('facebook_url', '').strip(),
        'instagram': request.form.get('instagram_url', '').strip(),
        'twitter': request.form.get('twitter_url', '').strip(),
        'linkedin': request.form.get('linkedin_url', '').strip(),
        'tiktok': request.form.get('tiktok_url', '').strip(),
        'youtube': request.form.get('youtube_url', '').strip(),
        'whatsapp': request.form.get('whatsapp_number', '').strip(),
        'telegram': request.form.get('telegram_url', '').strip()
    }
    
    # Supprimer les entrées vides
    social_links = {k: v for k, v in social_links.items() if v}
    
    # Sauvegarder
    AppSettings.set('social_links', social_links)
    
    flash('✅ Liens réseaux sociaux mis à jour avec succès', 'success')
    return redirect(url_for('admin.settings_customization'))

@bp.route('/settings/customization/save-legal-pages', methods=['POST'])
@login_required
@admin_required
def save_legal_pages():
    """Sauvegarder les pages légales"""
    legal_pages = {
        # Contenu des pages - utiliser les clés correctes pour correspondre à legal.py
        'terms_page': request.form.get('terms_of_service', '').strip(),
        'privacy_page': request.form.get('privacy_policy', '').strip(),
        'about_page': request.form.get('about_page', '').strip(),
        'cookies_page': request.form.get('cookie_policy', '').strip(),
        'mentions_page': request.form.get('mentions_legales', '').strip(),
        
        # Informations de l'entreprise pour les mentions légales
        'company_name': request.form.get('company_name', '').strip(),
        'company_type': request.form.get('company_type', '').strip(),
        'registration_number': request.form.get('registration_number', '').strip(),
        'capital': request.form.get('capital', '').strip(),
        'company_address': request.form.get('company_address', '').strip(),
        'company_phone': request.form.get('company_phone', '').strip(),
        'company_email': request.form.get('company_email', '').strip(),
        'company_website': request.form.get('company_website', '').strip(),
        'company_whatsapp': request.form.get('company_whatsapp', '').strip(),
        'director_name': request.form.get('director_name', '').strip(),
        'director_role': request.form.get('director_role', '').strip(),
        'hosting_provider': request.form.get('hosting_provider', '').strip(),
        'hosting_address': request.form.get('hosting_address', '').strip(),
        'hosting_phone': request.form.get('hosting_phone', '').strip()
    }
    
    # Options d'activation des pages
    legal_pages_enabled = {
        'terms': request.form.get('enable_terms') == '1',
        'privacy': request.form.get('enable_privacy') == '1',
        'about': request.form.get('enable_about') == '1',
        'cookies': request.form.get('enable_cookies') == '1',
        'mentions': request.form.get('enable_mentions') == '1'
    }
    
    # Sauvegarder
    AppSettings.set('legal_pages', legal_pages)
    AppSettings.set('legal_pages_enabled', legal_pages_enabled)
    
    # Logger l'activité
    from app.services.logging_service import LoggingService
    LoggingService.log_activity(
        user=current_user,
        action_type='update',
        action_category='settings',
        description='Mise à jour des pages légales',
        resource_type='LegalPages',
        status='success'
    )
    
    flash('✅ Pages légales mises à jour avec succès', 'success')
    return redirect(url_for('admin.settings_customization'))

@bp.route('/settings/recap-config', methods=['GET', 'POST'])
@login_required
@admin_required
def settings_recap_config():
    """Configuration du récapitulatif hebdomadaire d'inscriptions"""
    
    # Champs disponibles pour les talents
    available_talent_fields = {
        'full_name': 'Nom complet',
        'email': 'Email',
        'phone': 'Téléphone',
        'unique_code': 'Code unique',
        'created_at': 'Date d\'inscription',
        'city': 'Ville',
        'country': 'Pays',
        'gender': 'Genre',
        'age': 'Âge'
    }
    
    # Champs disponibles pour les talents cinéma
    available_cinema_fields = {
        'full_name': 'Nom complet',
        'email': 'Email',
        'phone': 'Téléphone',
        'unique_code': 'Code unique',
        'created_at': 'Date d\'inscription',
        'city': 'Ville',
        'country': 'Pays',
        'gender': 'Genre',
        'age': 'Âge',
        'role': 'Rôle'
    }
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        talent_enabled = request.form.get('talent_enabled') == 'on'
        cinema_enabled = request.form.get('cinema_enabled') == 'on'
        
        talent_fields = request.form.getlist('talent_fields[]')
        cinema_fields = request.form.getlist('cinema_fields[]')
        
        # Valider les champs sélectionnés
        talent_fields = [f for f in talent_fields if f in available_talent_fields]
        cinema_fields = [f for f in cinema_fields if f in available_cinema_fields]
        
        # Si aucun champ sélectionné, utiliser tous les champs par défaut
        if not talent_fields:
            talent_fields = list(available_talent_fields.keys())
        if not cinema_fields:
            cinema_fields = list(available_cinema_fields.keys())
        
        # Créer la configuration
        recap_config = {
            'talents': {
                'enabled': talent_enabled,
                'fields': talent_fields
            },
            'cinema_talents': {
                'enabled': cinema_enabled,
                'fields': cinema_fields
            }
        }
        
        # Sauvegarder
        AppSettings.set('weekly_recap_config', recap_config)
        flash('✅ Configuration du récapitulatif hebdomadaire mise à jour', 'success')
        return redirect(url_for('admin.settings_recap_config'))
    
    # GET: Charger la configuration existante
    recap_config = AppSettings.get('weekly_recap_config', {
        'talents': {
            'enabled': True,
            'fields': list(available_talent_fields.keys())
        },
        'cinema_talents': {
            'enabled': True,
            'fields': list(available_cinema_fields.keys())
        }
    })
    
    return render_template('admin/settings/recap_config.html',
                         recap_config=recap_config,
                         available_talent_fields=available_talent_fields,
                         available_cinema_fields=available_cinema_fields)

@bp.route('/settings/backups')
@login_required
@admin_required
def settings_backups():
    try:
        backups = BackupService.list_backups()
    except Exception as e:
        backups = []
        flash(f'Erreur lors de la récupération des sauvegardes: {str(e)}', 'error')
    return render_template('admin/settings/backups.html', backups=backups)

@bp.route('/settings/roles')
@login_required
@admin_required
def settings_roles():
    return render_template('admin/settings/roles.html')

@bp.route('/settings/system')
@login_required
@admin_required
def settings_system():
    import sys
    import flask
    from app.models.production import Production
    
    # Informations de la base de données
    db_info = {
        'type': 'PostgreSQL',
        'connected': True,
        'tables_count': len(db.metadata.tables)
    }
    
    # Statistiques
    stats = {
        'users': User.query.count(),
        'talents': Talent.query.count(),
        'productions': Production.query.count(),
        'admins': User.query.filter(User.is_admin == True).count()
    }
    
    # Informations système
    system_info = {
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'flask_version': flask.__version__,
        'environment': os.environ.get('FLASK_ENV', 'development'),
        'debug': current_app.debug
    }
    
    # Récupérer le code personnalisé pour le <head>
    custom_head_code = AppSettings.get('custom_head_code', '')
    
    # Récupérer les paramètres SEO
    seo_settings = SEOService.get_all_settings()
    
    return render_template('admin/settings/system.html', 
                         db_info=db_info, 
                         stats=stats, 
                         system_info=system_info,
                         custom_head_code=custom_head_code,
                         seo_settings=seo_settings)

@bp.route('/save-custom-head-code', methods=['POST'])
@login_required
@admin_required
def save_custom_head_code():
    custom_head_code = request.form.get('custom_head_code', '').strip()
    
    # Enregistrer le code personnalisé
    AppSettings.set('custom_head_code', custom_head_code)
    
    flash('Code personnalisé enregistré avec succès.', 'success')
    return redirect(url_for('admin.settings_system'))

@bp.route('/save-seo-settings', methods=['POST'])
@login_required
@admin_required
def save_seo_settings():
    from app.services.logging_service import LoggingService
    from werkzeug.utils import secure_filename
    
    # Charger les paramètres SEO existants pour préserver les valeurs non modifiées
    existing_settings = SEOService.get_all_settings()
    
    # Récupérer tous les champs SEO du formulaire
    seo_data = {
        'seo_site_name': request.form.get('seo_site_name', '').strip(),
        'seo_site_description': request.form.get('seo_site_description', '').strip(),
        'seo_keywords': request.form.get('seo_keywords', '').strip(),
        'seo_author': request.form.get('seo_author', '').strip(),
        'seo_og_type': request.form.get('seo_og_type', 'website').strip(),
        'seo_og_image': existing_settings.get('seo_og_image', ''),
        'seo_twitter_card': request.form.get('seo_twitter_card', 'summary_large_image').strip(),
        'seo_twitter_handle': request.form.get('seo_twitter_handle', '').strip(),
        'seo_robots': request.form.get('seo_robots', 'index, follow').strip(),
        'seo_canonical_url': request.form.get('seo_canonical_url', '').strip(),
        'seo_language': request.form.get('seo_language', 'fr').strip(),
        'seo_region': request.form.get('seo_region', 'MA').strip()
    }
    
    # Gérer l'upload de l'image OpenGraph
    if 'seo_og_image_file' in request.files:
        file = request.files['seo_og_image_file']
        if file and file.filename and file.filename != '':
            # Vérifier que c'est bien une image
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
            file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            
            if file_ext in allowed_extensions:
                # Créer un nom unique pour éviter les conflits
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"og_image_{timestamp}.{file_ext}"
                
                # Créer le dossier de destination s'il n'existe pas
                upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'seo')
                os.makedirs(upload_folder, exist_ok=True)
                
                # Sauvegarder le fichier
                file_path = os.path.join(upload_folder, unique_filename)
                file.save(file_path)
                
                # Mettre à jour le chemin dans seo_data
                seo_data['seo_og_image'] = f"/static/uploads/seo/{unique_filename}"
                flash('Image OpenGraph téléchargée avec succès.', 'success')
            else:
                flash('Format d\'image non supporté. Utilisez PNG, JPG, JPEG, GIF ou WEBP.', 'error')
    
    # Enregistrer les paramètres SEO
    SEOService.update_settings(seo_data)
    
    # Logger l'activité
    LoggingService.log_activity(
        user=current_user,
        action_type='update',
        action_category='settings',
        description='Mise à jour des paramètres SEO',
        resource_type='SEOSettings',
        status='success'
    )
    
    flash('Paramètres SEO enregistrés avec succès.', 'success')
    return redirect(url_for('admin.settings_system'))

@bp.route('/settings/activity-logs')
@login_required
@admin_required
def settings_activity_logs():
    from app.services.logging_service import LoggingService
    from flask import request
    
    action_type = request.args.get('action_type', 'all')
    username = request.args.get('username', '')
    date_start = request.args.get('date_start', '')
    date_end = request.args.get('date_end', '')
    
    if action_type != 'all' or username or date_start or date_end:
        logs = LoggingService.get_filtered_activities(
            action_type=action_type,
            username=username if username else None,
            date_start=date_start if date_start else None,
            date_end=date_end if date_end else None,
            limit=100
        )
    else:
        logs = LoggingService.get_recent_activities(limit=100)
    
    action_types = LoggingService.get_distinct_action_types()
    
    return render_template('admin/settings/activity_logs.html', 
                         logs=logs, 
                         action_types=action_types,
                         current_action_type=action_type,
                         current_username=username,
                         current_date_start=date_start,
                         current_date_end=date_end)

@bp.route('/settings/security-logs')
@login_required
@admin_required
def settings_security_logs():
    from app.services.logging_service import LoggingService
    from app.models.security_log import SecurityLog
    
    # Calculer les statistiques
    failed_attempts = SecurityLog.query.filter_by(event_type='failed_login').count()
    suspicious = SecurityLog.query.filter_by(severity='warning').count()
    critical = SecurityLog.query.filter_by(severity='critical').count()
    unresolved = SecurityLog.query.filter_by(resolved=False).count()
    
    security_stats = {
        'failed_attempts': failed_attempts,
        'suspicious': suspicious,
        'blocked_ips': 0,  # À implémenter plus tard
        'alerts': critical + unresolved
    }
    
    security_logs = LoggingService.get_security_logs(limit=100)
    return render_template('admin/settings/security_logs.html', 
                         security_stats=security_stats, 
                         security_logs=security_logs)

@bp.route('/settings/users')
@login_required
@admin_required
def settings_users():
    admins = User.query.filter(User.is_admin == True).all()
    recruiters = User.query.filter(User.role == 'recruteur').all()
    regular_users = User.query.filter(and_(User.is_admin == False, User.role != 'recruteur', User.role != 'presence')).order_by(User.first_name).all()
    return render_template('admin/settings/users.html', admins=admins, recruiters=recruiters, regular_users=regular_users)

@bp.route('/settings/cache')
@login_required
@admin_required
def settings_cache():
    from app.services.cache_service import CacheService
    cache_stats = CacheService.get_cache_stats()
    last_clear = CacheService.get_last_clear()
    return render_template('admin/settings/cache.html', cache_stats=cache_stats, last_clear=last_clear)

@bp.route('/cache/clear-system', methods=['POST'])
@login_required
@admin_required
def cache_clear_system():
    from app.services.cache_service import CacheService
    result = CacheService.clear_system_cache()
    flash(f'Cache système nettoyé! {result.get("removed", 0)} éléments supprimés.', 'success')
    return redirect(url_for('admin.settings_cache'))

@bp.route('/cache/clear-flask', methods=['POST'])
@login_required
@admin_required
def cache_clear_flask():
    from app.services.cache_service import CacheService
    result = CacheService.clear_flask_cache()
    if result.get('success'):
        flash(result.get('message', 'Cache Flask nettoyé!'), 'success')
    else:
        flash(f'Erreur: {result.get("message")}', 'error')
    return redirect(url_for('admin.settings_cache'))

@bp.route('/cache/clear-temp', methods=['POST'])
@login_required
@admin_required
def cache_clear_temp():
    from app.services.cache_service import CacheService
    result = CacheService.clear_temp_files()
    if result.get('success'):
        flash(f'Fichiers temporaires nettoyés! {result.get("removed", 0)} fichiers supprimés.', 'success')
    else:
        flash(f'Erreur: {result.get("message")}', 'error')
    return redirect(url_for('admin.settings_cache'))

@bp.route('/cache/clear-all', methods=['POST'])
@login_required
@admin_required
def cache_clear_all():
    from app.services.cache_service import CacheService
    result = CacheService.clear_all()
    if result.get('success'):
        messages = '<br>'.join(result.get('results', []))
        flash(f'Tous les caches nettoyés!<br>{messages}', 'success')
    else:
        flash('Erreur lors du nettoyage du cache', 'error')
    return redirect(url_for('admin.settings_cache'))

@bp.route('/settings/github')
@login_required
@admin_required
def settings_github():
    git_info = UpdateService.get_git_info()
    update_history = UpdateService.get_update_history(10)
    
    # Charger la configuration Git
    git_config = AppSettings.get('git_config', {
        'repo_url': '',
        'branch': 'main',
        'auto_migrate': True
    })
    
    return render_template('admin/settings/github_updates.html', 
                         git_info=git_info, 
                         update_history=update_history,
                         git_config=git_config)

@bp.route('/settings/github/save-config', methods=['POST'])
@login_required
@admin_required
def save_git_config():
    """Sauvegarder la configuration Git"""
    git_repo_url = request.form.get('git_repo_url', '').strip()
    git_branch = request.form.get('git_branch', 'main').strip()
    auto_migrate = request.form.get('auto_migrate') == 'on'
    
    git_config = {
        'repo_url': git_repo_url,
        'branch': git_branch,
        'auto_migrate': auto_migrate
    }
    
    # Sauvegarder
    AppSettings.set('git_config', git_config)
    
    # Si une URL est fournie, configurer le remote Git
    if git_repo_url:
        try:
            success, message = UpdateService.configure_git_remote(git_repo_url, git_branch)
            if success:
                flash('✅ Configuration Git enregistrée et remote configuré avec succès', 'success')
            else:
                flash(f'⚠️ Configuration enregistrée mais erreur lors de la configuration du remote: {message}', 'warning')
        except Exception as e:
            flash(f'⚠️ Configuration enregistrée mais erreur: {str(e)}', 'warning')
    else:
        flash('✅ Configuration Git enregistrée', 'success')
    
    return redirect(url_for('admin.settings_github'))

@bp.route('/git/pull', methods=['POST'])
@login_required
@admin_required
def git_pull():
    try:
        # Charger la configuration
        git_config = AppSettings.get('git_config', {'auto_migrate': True})
        
        result = UpdateService.git_pull_with_migration(auto_migrate=git_config.get('auto_migrate', True))
        if result.get('success'):
            flash(f'✅ Mise à jour réussie! {result.get("message", "")}', 'success')
        else:
            flash(f'❌ Erreur lors de la mise à jour: {result.get("message", "")}', 'error')
    except Exception as e:
        flash(f'❌ Erreur: {str(e)}', 'error')
    return redirect(url_for('admin.settings_github'))

@bp.route('/git/status', methods=['POST'])
@login_required
@admin_required
def git_status():
    try:
        result = UpdateService.git_status()
        if result.get('success'):
            flash(f'État Git: {result.get("message", "")}', 'info')
        else:
            flash(f'Erreur: {result.get("message", "")}', 'error')
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
    return redirect(url_for('admin.settings_github'))

@bp.route('/maintenance/optimize-database', methods=['POST'])
@login_required
@admin_required
def maintenance_optimize_database():
    from app.services.logging_service import LoggingService
    
    try:
        result = MaintenanceService.optimize_database()
        if result.get('success'):
            flash(f'✅ {result.get("message")}', 'success')
            LoggingService.log_activity(
                user=current_user,
                action_type='maintenance',
                action_category='database',
                description='Optimisation de la base de données',
                status='success'
            )
        else:
            flash(f'⚠️  {result.get("message")}', 'error')
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
    return redirect(url_for('admin.settings_system'))

@bp.route('/maintenance/clean-temp-files', methods=['POST'])
@login_required
@admin_required
def maintenance_clean_temp_files():
    from app.services.logging_service import LoggingService
    
    try:
        result = MaintenanceService.clean_temp_files()
        if result.get('success'):
            flash(f'✅ {result.get("message")}', 'success')
            LoggingService.log_activity(
                user=current_user,
                action_type='maintenance',
                action_category='files',
                description='Nettoyage des fichiers temporaires',
                status='success'
            )
        else:
            flash(f'⚠️  {result.get("message")}', 'error')
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
    return redirect(url_for('admin.settings_system'))

@bp.route('/maintenance/analyze-performance', methods=['POST'])
@login_required
@admin_required
def maintenance_analyze_performance():
    from app.services.logging_service import LoggingService
    
    try:
        result = MaintenanceService.analyze_performance()
        if result.get('success'):
            metrics_html = '<br>'.join(result.get('metrics', []))
            status_icon = '✅' if result.get('status') == 'good' else ('⚠️' if result.get('status') == 'warning' else '🚨')
            flash(f'{status_icon} Analyse terminée:<br>{metrics_html}', 'success' if result.get('status') == 'good' else 'warning')
            LoggingService.log_activity(
                user=current_user,
                action_type='maintenance',
                action_category='performance',
                description='Analyse des performances',
                status='success'
            )
        else:
            flash(f'⚠️  {result.get("message")}', 'error')
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
    return redirect(url_for('admin.settings_system'))

@bp.route('/maintenance/verify-data-integrity', methods=['POST'])
@login_required
@admin_required
def maintenance_verify_data_integrity():
    from app.services.logging_service import LoggingService
    
    try:
        result = MaintenanceService.verify_data_integrity()
        if result.get('success'):
            issues_html = '<br>'.join(result.get('issues', []))
            status_icon = '✅' if result.get('status') == 'healthy' else ('⚠️' if result.get('status') == 'warning' else '🚨')
            flash(f'{status_icon} {result.get("message")}:<br>{issues_html}', 'success' if result.get('status') == 'healthy' else 'warning')
            LoggingService.log_activity(
                user=current_user,
                action_type='maintenance',
                action_category='integrity',
                description='Vérification de l\'intégrité des données',
                status='success'
            )
        else:
            flash(f'⚠️  {result.get("message")}', 'error')
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
    return redirect(url_for('admin.settings_system'))

@bp.route('/user/<int:user_id>/promote-admin', methods=['POST'])
@login_required
@admin_required
def promote_admin(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.is_admin:
        flash('Cet utilisateur est déjà administrateur.', 'error')
        return redirect(url_for('admin.settings'))
    
    user.is_admin = True
    db.session.commit()
    flash(f'{user.full_name} est maintenant administrateur.', 'success')
    return redirect(url_for('admin.settings'))

@bp.route('/user/<int:user_id>/demote-admin', methods=['POST'])
@login_required
@admin_required
def demote_admin(user_id):
    user = User.query.get_or_404(user_id)
    
    if not user.is_admin:
        flash('Cet utilisateur n\'est pas administrateur.', 'error')
        return redirect(url_for('admin.settings'))
    
    if user.id == current_user.id:
        flash('Vous ne pouvez pas retirer vos propres droits d\'administrateur.', 'error')
        return redirect(url_for('admin.settings'))
    
    admin_count = User.query.filter(User.is_admin == True).count()
    if admin_count <= 1:
        flash('Impossible de retirer les droits du dernier administrateur.', 'error')
        return redirect(url_for('admin.settings'))
    
    user.is_admin = False
    db.session.commit()
    flash(f'{user.full_name} n\'est plus administrateur.', 'success')
    return redirect(url_for('admin.settings'))

@bp.route('/user/<int:user_id>/promote-recruiter', methods=['POST'])
@login_required
@admin_required
def promote_recruiter(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.is_admin:
        flash('Cet utilisateur est administrateur. Retirez d\'abord ses droits d\'administrateur.', 'error')
        return redirect(url_for('admin.settings_users'))
    
    if user.role == 'recruteur':
        flash('Cet utilisateur est déjà recruteur.', 'error')
        return redirect(url_for('admin.settings_users'))
    
    user.role = 'recruteur'
    db.session.commit()
    flash(f'{user.full_name} est maintenant recruteur.', 'success')
    return redirect(url_for('admin.settings_users'))

@bp.route('/user/<int:user_id>/demote-recruiter', methods=['POST'])
@login_required
@admin_required
def demote_recruiter(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.role != 'recruteur':
        flash('Cet utilisateur n\'est pas recruteur.', 'error')
        return redirect(url_for('admin.settings_users'))
    
    user.role = 'user'
    db.session.commit()
    flash(f'{user.full_name} n\'est plus recruteur.', 'success')
    return redirect(url_for('admin.settings_users'))

@bp.route('/save-settings', methods=['POST'])
@login_required
@admin_required
def save_settings():
    sendgrid_key = request.form.get('sendgrid_api_key', '').strip()
    openrouter_key = request.form.get('openrouter_api_key', '').strip()
    perplexity_key = request.form.get('perplexity_api_key', '').strip()
    openai_key = request.form.get('openai_api_key', '').strip()
    gemini_key = request.form.get('gemini_api_key', '').strip()
    omdb_key = request.form.get('omdb_api_key', '').strip()
    sender_email = request.form.get('sender_email', '').strip() or 'noreply@myoneart.com'
    
    # Configuration IA
    ai_provider = request.form.get('ai_provider', '').strip() or 'openrouter'
    openrouter_model = request.form.get('openrouter_model', '').strip() or 'google/gemini-2.0-flash-001:free'
    perplexity_model = request.form.get('perplexity_model', '').strip() or 'sonar'
    openai_model = request.form.get('openai_model', '').strip() or 'gpt-4o-mini'
    gemini_model = request.form.get('gemini_model', '').strip() or 'gemini-2.0-flash-exp'
    
    # Enregistrer les clés API si elles ne commencent pas par '*' (masquées)
    if sendgrid_key and not sendgrid_key.startswith('*'):
        AppSettings.set('sendgrid_api_key', sendgrid_key)
    
    if openrouter_key and not openrouter_key.startswith('*'):
        AppSettings.set('openrouter_api_key', openrouter_key)
    
    if perplexity_key and not perplexity_key.startswith('*'):
        AppSettings.set('perplexity_api_key', perplexity_key)
    
    if openai_key and not openai_key.startswith('*'):
        AppSettings.set('openai_api_key', openai_key)
    
    if gemini_key and not gemini_key.startswith('*'):
        AppSettings.set('gemini_api_key', gemini_key)
    
    if omdb_key and not omdb_key.startswith('*'):
        AppSettings.set('omdb_api_key', omdb_key)
    
    # Enregistrer les paramètres IA
    AppSettings.set('ai_provider', ai_provider)
    AppSettings.set('openrouter_model', openrouter_model)
    AppSettings.set('perplexity_model', perplexity_model)
    AppSettings.set('openai_model', openai_model)
    AppSettings.set('gemini_model', gemini_model)
    AppSettings.set('sender_email', sender_email)
    
    flash('Paramètres sauvegardés avec succès.', 'success')
    return redirect(url_for('admin.settings_api_keys'))

@bp.route('/test-email', methods=['POST'])
@login_required
@admin_required
def test_email():
    test_email_address = request.form.get('test_email', '').strip()
    
    if not test_email_address:
        flash('Veuillez saisir une adresse email.', 'error')
        return redirect(url_for('admin.settings'))
    
    sendgrid_key = AppSettings.get('sendgrid_api_key', '') or os.environ.get('SENDGRID_API_KEY', '')
    sender_email = AppSettings.get('sender_email', 'noreply@myoneart.com')
    
    if not sendgrid_key:
        flash('Clé SendGrid API non configurée.', 'error')
        return redirect(url_for('admin.settings'))
    
    try:
        email_service = EmailService(sendgrid_key, sender_email)
        success = email_service.send_test_email(test_email_address)
        
        if success:
            flash(f'Email de test envoyé avec succès à {test_email_address}', 'success')
        else:
            flash('Échec de l\'envoi de l\'email de test.', 'error')
    except Exception as e:
        flash(f'Erreur lors de l\'envoi de l\'email: {str(e)}', 'error')
    
    return redirect(url_for('admin.settings'))

@bp.route('/test-openrouter', methods=['POST'])
@login_required
@admin_required
def test_openrouter():
    from app.services.ai_provider_service import AIProviderService
    
    config = AIProviderService.get_ai_config()
    provider = config['provider']
    api_key = config['api_key']
    model = config['model']
    
    if not api_key:
        flash(f'Clé API {provider.upper()} non configurée.', 'error')
        return redirect(url_for('admin.settings_api_keys'))
    
    if not model:
        flash(f'Modèle pour {provider.upper()} non sélectionné.', 'error')
        return redirect(url_for('admin.settings_api_keys'))
    
    try:
        result = AIProviderService.call_ai(
            prompt='Réponds juste "OK" si tu me reçois.',
            temperature=0.3,
            timeout=15
        )
        
        if result['success']:
            response_content = result['content'][:100]
            flash(f'{provider.upper()} API fonctionne correctement! ✅<br>Modèle: {model}<br>Réponse: {response_content}', 'success')
        else:
            error_msg = result.get('error', 'Erreur inconnue')
            
            # Messages d'aide spécifiques selon l'erreur
            help_msg = ""
            if '401' in str(error_msg):
                if provider == 'perplexity':
                    help_msg = "<br><br><b>💡 Solutions possibles:</b><br>"
                    help_msg += "1. Vérifiez que votre clé API est valide sur <a href='https://www.perplexity.ai/settings/api' target='_blank' class='underline'>perplexity.ai/settings/api</a><br>"
                    help_msg += "2. Assurez-vous d'avoir des crédits sur votre compte Perplexity<br>"
                    help_msg += "3. Vérifiez que vous avez bien copié la clé complète (commence par 'pplx-')<br>"
                    help_msg += "4. Essayez de régénérer une nouvelle clé API"
                elif provider == 'openai':
                    help_msg = "<br><br><b>💡 Vérifiez:</b><br>"
                    help_msg += "• Clé API valide sur <a href='https://platform.openai.com/api-keys' target='_blank' class='underline'>platform.openai.com</a><br>"
                    help_msg += "• Crédits disponibles sur votre compte"
                elif provider == 'openrouter':
                    help_msg = "<br><br><b>💡 Vérifiez:</b><br>"
                    help_msg += "• Clé API valide sur <a href='https://openrouter.ai/keys' target='_blank' class='underline'>openrouter.ai/keys</a><br>"
                    help_msg += "• Crédits disponibles"
            
            flash(f'Erreur {provider.upper()}: {error_msg}{help_msg}', 'error')
    except Exception as e:
        flash(f'Erreur lors du test {provider.upper()}: {str(e)}', 'error')
    
    return redirect(url_for('admin.settings_api_keys'))

@bp.route('/create-admin-user', methods=['GET', 'POST'])
@login_required
@admin_required
def create_admin_user():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        country_id = request.form.get('country_id')
        city_id = request.form.get('city_id')
        
        if not all([first_name, last_name, email, country_id, city_id]):
            flash('Tous les champs sont obligatoires.', 'error')
            return redirect(url_for('admin.create_admin_user'))
        
        if User.query.filter(User.email == email).first():
            flash('Cet email est déjà utilisé.', 'error')
            return redirect(url_for('admin.create_admin_user'))
        
        country = Country.query.get(country_id)
        city = City.query.get(city_id)
        
        if not country or not city:
            flash('Pays ou ville invalide.', 'error')
            return redirect(url_for('admin.create_admin_user'))
        
        gender = request.form.get('gender', 'M')
        random_password = ''.join(secrets.choice(string.ascii_letters + string.digits + '@#$%') for _ in range(12))
        
        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.password = random_password
        user.country_id = country_id
        user.city_id = city_id
        user.gender = gender
        user.is_admin = True
        user.account_active = True
        
        db.session.add(user)
        db.session.flush()
        
        from app.utils.id_generator import generate_unique_code
        from app.utils.qr_generator import generate_qr_code
        
        user.unique_code = generate_unique_code(country.code, city.code, user.id, gender)
        
        try:
            qr_filename = generate_qr_code(user.unique_code, user.id)
            user.qr_code_filename = qr_filename
        except Exception as e:
            print(f"Erreur génération QR code: {e}")
        
        db.session.commit()
        
        flash(f'Administrateur créé avec succès! Email: {email}, Mot de passe: {random_password}', 'success')
        return redirect(url_for('admin.settings'))
    
    countries = Country.query.order_by(Country.name).all()
    cities = City.query.order_by(City.name).all()
    
    return render_template('admin/create_admin.html', countries=countries, cities=cities)

@bp.route('/perform-update', methods=['POST'])
@login_required
@admin_required
def perform_update():
    if not UpdateService.check_git_available():
        flash('Git n\'est pas disponible sur ce système.', 'error')
        return redirect(url_for('admin.settings'))
    
    try:
        success, log_entry = UpdateService.perform_full_update()
        
        if success:
            flash('✅ Mise à jour effectuée avec succès! L\'application va redémarrer pour appliquer les changements.', 'success')
        else:
            failed_step = next((step['name'] for step in log_entry['steps'] if not step['success']), 'Unknown')
            flash(f'❌ Échec de la mise à jour à l\'étape: {failed_step}. Consultez les logs pour plus de détails.', 'error')
    except Exception as e:
        flash(f'Erreur lors de la mise à jour: {str(e)}', 'error')
    
    return redirect(url_for('admin.settings'))

@bp.route('/check-updates', methods=['POST'])
@login_required
@admin_required
def check_updates():
    if not UpdateService.check_git_available():
        return jsonify({'error': 'Git non disponible'}), 400
    
    try:
        has_updates, count = UpdateService.check_updates_available()
        recent_commits = UpdateService.get_commit_logs(5)
        
        return jsonify({
            'has_updates': has_updates,
            'count': count,
            'recent_commits': recent_commits
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/bulk/export')
@login_required
@admin_required
def bulk_export():
    format_type = request.args.get('format', 'excel')
    ids_str = request.args.get('ids', '')
    
    if not ids_str:
        flash('Aucun utilisateur sélectionné.', 'error')
        return redirect(url_for('main.index'))
    
    try:
        user_ids = [int(id_str) for id_str in ids_str.split(',')]
        users = User.query.filter(User.id.in_(user_ids)).all()
        
        if not users:
            flash('Aucun utilisateur trouvé.', 'error')
            return redirect(url_for('main.index'))
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format_type == 'excel':
            excel_bytes = ExportService.export_to_excel(users)
            buffer = io.BytesIO(excel_bytes)
            buffer.seek(0)
            return send_file(
                buffer,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=f'talents_selection_{timestamp}.xlsx'
            )
        
        elif format_type == 'csv':
            csv_data = ExportService.export_to_csv(users)
            buffer = io.BytesIO(csv_data.encode('utf-8'))
            buffer.seek(0)
            return send_file(
                buffer,
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'talents_selection_{timestamp}.csv'
            )
        
        elif format_type == 'pdf':
            pdf_bytes = ExportService.export_list_to_pdf(users, current_user=current_user)
            buffer = io.BytesIO(pdf_bytes)
            buffer.seek(0)
            return send_file(
                buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'talents_selection_{timestamp}.pdf'
            )
        
        else:
            flash('Format non supporté.', 'error')
            return redirect(url_for('main.index'))
    
    except Exception as e:
        current_app.logger.error(f'Erreur lors de l\'export en masse: {e}')
        flash(f'Erreur lors de l\'export: {str(e)}', 'error')
        return redirect(url_for('main.index'))

@bp.route('/bulk/delete', methods=['POST'])
@login_required
@admin_required
def bulk_delete():
    try:
        data = request.get_json()
        user_ids = data.get('ids', [])
        
        if not user_ids:
            return jsonify({'success': False, 'error': 'Aucun utilisateur sélectionné'}), 400
        
        users = User.query.filter(
            User.id.in_(user_ids),
            User.is_admin == False
        ).all()
        
        if len(users) != len(user_ids):
            admin_count = len(user_ids) - len(users)
            return jsonify({
                'success': False, 
                'error': f'{admin_count} administrateur(s) ne peuvent pas être supprimés. Seuls les utilisateurs non-admin peuvent être supprimés en masse.'
            }), 400
        
        deleted_count = 0
        errors = []
        
        for user in users:
            try:
                db.session.delete(user)
                deleted_count += 1
            except Exception as e:
                db.session.rollback()
                errors.append(f'Erreur lors de la suppression de {user.full_name}: {str(e)}')
        
        if deleted_count > 0:
            db.session.commit()
        
        response = {
            'success': True,
            'deleted_count': deleted_count,
            'errors': errors
        }
        
        if errors:
            response['warning'] = f'{len(errors)} utilisateur(s) n\'ont pas pu être supprimés'
        
        return jsonify(response)
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erreur lors de la suppression en masse: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/backup/create', methods=['POST'])
@login_required
@admin_required
def create_backup():
    """Créer une sauvegarde complète de l'application"""
    from app.services.logging_service import LoggingService
    
    zip_path = None
    temp_dir = None
    
    try:
        # Créer le backup
        zip_path, temp_dir = BackupService.create_full_backup()
        
        # Log backup creation
        LoggingService.log_activity(
            user=current_user,
            action_type='create',
            action_category='settings',
            description='Création d\'une sauvegarde complète',
            resource_type='Backup',
            status='success'
        )
        LoggingService.log_security_event(
            event_type='backup_created',
            description=f'Sauvegarde créée par {current_user.email}',
            severity='info',
            user=current_user
        )
        
        # Définir le nettoyage après l'envoi de la réponse
        @after_this_request
        def cleanup(response):
            try:
                if temp_dir and os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            except Exception as e:
                current_app.logger.warning(f"Impossible de nettoyer le temp_dir: {e}")
            return response
        
        # Envoyer le fichier ZIP au client
        return send_file(
            zip_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name=os.path.basename(zip_path)
        )
    
    except Exception as e:
        # Nettoyer en cas d'erreur
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
        
        current_app.logger.error(f'Erreur lors de la création du backup: {e}')
        flash(f'Erreur lors de la création de la sauvegarde: {str(e)}', 'error')
        return redirect(url_for('admin.settings'))


@bp.route('/backup/restore', methods=['POST'])
@login_required
@admin_required
def restore_backup():
    """Restaurer l'application depuis un fichier de sauvegarde"""
    from app.services.logging_service import LoggingService
    
    try:
        # Vérifier qu'un fichier a été uploadé
        if 'backup_file' not in request.files:
            flash('Aucun fichier de sauvegarde fourni.', 'error')
            return redirect(url_for('admin.settings'))
        
        backup_file = request.files['backup_file']
        
        if backup_file.filename == '':
            flash('Aucun fichier sélectionné.', 'error')
            return redirect(url_for('admin.settings'))
        
        # Vérifier que c'est un fichier ZIP
        if not backup_file.filename.endswith('.zip'):
            flash('Le fichier doit être un fichier ZIP de sauvegarde taalentio.com.', 'error')
            return redirect(url_for('admin.settings'))
        
        # Sauvegarder temporairement le fichier
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        backup_file.save(temp_file.name)
        temp_file.close()
        
        # Restaurer depuis le backup
        result = BackupService.restore_from_backup(temp_file.name)
        
        # Nettoyer le fichier temporaire
        os.unlink(temp_file.name)
        
        if result['success']:
            # Log successful restoration
            LoggingService.log_activity(
                user=current_user,
                action_type='update',
                action_category='settings',
                description='Restauration réussie depuis une sauvegarde',
                resource_type='Backup',
                status='success'
            )
            LoggingService.log_security_event(
                event_type='backup_restored',
                description=f'Restauration effectuée par {current_user.email}',
                severity='warning',
                user=current_user,
                action_taken='database_restored'
            )
            flash('Restauration réussie ! L\'application a été restaurée depuis la sauvegarde.', 'success')
        else:
            # Log failed restoration
            LoggingService.log_activity(
                user=current_user,
                action_type='update',
                action_category='settings',
                description=f'Échec de restauration : {result.get("message", "Erreur inconnue")}',
                resource_type='Backup',
                status='error',
                error_message=result.get("message", "Erreur inconnue")
            )
            flash(f'Erreur lors de la restauration: {result.get("message", "Erreur inconnue")}', 'error')
        
        return redirect(url_for('admin.settings'))
    
    except Exception as e:
        current_app.logger.error(f'Erreur lors de la restauration du backup: {e}')
        flash(f'Erreur lors de la restauration: {str(e)}', 'error')
        return redirect(url_for('admin.settings'))

# ==================== Watchlist Routes ====================

@bp.route('/settings/watchlist')
@login_required
@admin_required
def settings_watchlist():
    """
    Page de gestion de la liste de surveillance des inscriptions
    """
    from app.models.settings import AppSettings
    from app.models.user import User
    from app.models.cinema_talent import CinemaTalent
    import unicodedata
    import re
    
    # Récupérer la configuration
    watchlist_names_raw = AppSettings.get('watchlist_names', '')
    watchlist_notification_email = AppSettings.get('watchlist_notification_email', '')
    watchlist_enabled = AppSettings.get('watchlist_enabled', False)
    
    # Récupérer les personnes détectées
    detected_registrations = []
    
    if watchlist_names_raw:
        # Normaliser les noms de la watchlist
        watchlist_names = [name.strip().lower() for name in watchlist_names_raw.split('\n') if name.strip()]
        
        def normalize_name(text):
            """Normalise un nom en retirant les accents et les caractères spéciaux"""
            if not text:
                return ""
            # Supprimer les accents
            nfkd_form = unicodedata.normalize('NFKD', text.lower())
            return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
        
        # Chercher dans les talents
        all_talents = User.query.filter_by(role='user').all()
        for talent in all_talents:
            full_name_normalized = normalize_name(talent.full_name)
            first_name_normalized = normalize_name(talent.first_name)
            last_name_normalized = normalize_name(talent.last_name)
            
            for watch_name in watchlist_names:
                watch_name_normalized = normalize_name(watch_name)
                if (watch_name_normalized in full_name_normalized or 
                    watch_name_normalized == first_name_normalized or 
                    watch_name_normalized == last_name_normalized):
                    detected_registrations.append({
                        'full_name': talent.full_name,
                        'unique_code': talent.unique_code,
                        'type': 'talent',
                        'city': talent.city.name if talent.city else None,
                        'country': talent.country.name if talent.country else None,
                        'created_at': talent.created_at
                    })
                    break
        
        # Chercher dans les talents cinéma
        all_cinema_talents = CinemaTalent.query.all()
        for cinema_talent in all_cinema_talents:
            full_name_normalized = normalize_name(cinema_talent.full_name)
            first_name_normalized = normalize_name(cinema_talent.first_name)
            last_name_normalized = normalize_name(cinema_talent.last_name)
            
            for watch_name in watchlist_names:
                watch_name_normalized = normalize_name(watch_name)
                if (watch_name_normalized in full_name_normalized or 
                    watch_name_normalized == first_name_normalized or 
                    watch_name_normalized == last_name_normalized):
                    detected_registrations.append({
                        'full_name': cinema_talent.full_name,
                        'unique_code': cinema_talent.unique_code,
                        'type': 'cinema',
                        'city': cinema_talent.city,
                        'country': cinema_talent.country,
                        'created_at': cinema_talent.created_at
                    })
                    break
        
        # Trier par date (plus récent en premier)
        detected_registrations.sort(key=lambda x: x['created_at'] if x['created_at'] else '', reverse=True)
    
    return render_template(
        'admin/settings/watchlist.html',
        watchlist_names=watchlist_names_raw,
        watchlist_notification_email=watchlist_notification_email,
        watchlist_enabled=watchlist_enabled,
        detected_registrations=detected_registrations
    )

@bp.route('/settings/watchlist/save', methods=['POST'])
@login_required
@admin_required
def save_watchlist():
    """
    Sauvegarde la configuration de la liste de surveillance
    """
    from app.models.settings import AppSettings
    from app.services.logging_service import LoggingService
    
    try:
        watchlist_names = request.form.get('watchlist_names', '')
        watchlist_notification_email = request.form.get('watchlist_notification_email', '')
        watchlist_enabled = 'watchlist_enabled' in request.form
        
        # Sauvegarder la configuration
        AppSettings.set('watchlist_names', watchlist_names)
        AppSettings.set('watchlist_notification_email', watchlist_notification_email)
        AppSettings.set('watchlist_enabled', watchlist_enabled)
        
        # Logger l'activité
        LoggingService.log_activity(
            user=current_user,
            action_type='update',
            action_category='settings',
            description=f'Configuration de la liste de surveillance mise à jour',
            status='success'
        )
        
        flash('✅ Configuration de la liste de surveillance enregistrée avec succès!', 'success')
        
    except Exception as e:
        current_app.logger.error(f'Erreur lors de la sauvegarde de la watchlist: {e}')
        flash(f'❌ Erreur lors de la sauvegarde: {str(e)}', 'error')
    
    return redirect(url_for('admin.settings_watchlist'))
