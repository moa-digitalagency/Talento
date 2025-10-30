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
    omdb_key = AppSettings.get('omdb_api_key', '') or os.environ.get('OMDB_API_KEY', '')
    sender_email = AppSettings.get('sender_email', 'noreply@myoneart.com')
    
    sendgrid_configured = bool(sendgrid_key)
    openrouter_configured = bool(openrouter_key)
    omdb_configured = bool(omdb_key)
    
    def mask_key(key):
        if not key or len(key) < 8:
            return ''
        return key[:4] + '*' * (len(key) - 8) + key[-4:]
    
    config_info = {
        'sendgrid': sendgrid_configured,
        'openrouter': openrouter_configured,
        'omdb': omdb_configured,
        'sendgrid_key_masked': mask_key(sendgrid_key) if sendgrid_configured else '',
        'openrouter_key_masked': mask_key(openrouter_key) if openrouter_configured else '',
        'omdb_key_masked': mask_key(omdb_key) if omdb_configured else '',
        'sendgrid_from': sender_email
    }
    
    return render_template('admin/settings/api_keys.html', config=config_info)

@bp.route('/settings/email-templates')
@login_required
@admin_required
def settings_email_templates():
    return render_template('admin/settings/email_templates.html')

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
    logs = LoggingService.get_recent_activities(limit=100)
    return render_template('admin/settings/activity_logs.html', logs=logs)

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
    return render_template('admin/settings/github_updates.html', git_info=git_info, update_history=update_history)

@bp.route('/git/pull', methods=['POST'])
@login_required
@admin_required
def git_pull():
    try:
        result = UpdateService.git_pull()
        if result.get('success'):
            flash(f'Mise à jour réussie! {result.get("message", "")}', 'success')
        else:
            flash(f'Erreur lors de la mise à jour: {result.get("message", "")}', 'error')
    except Exception as e:
        flash(f'Erreur: {str(e)}', 'error')
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
    omdb_key = request.form.get('omdb_api_key', '').strip()
    sender_email = request.form.get('sender_email', '').strip() or 'noreply@myoneart.com'
    
    if sendgrid_key and not sendgrid_key.startswith('*'):
        AppSettings.set('sendgrid_api_key', sendgrid_key)
    
    if openrouter_key and not openrouter_key.startswith('*'):
        AppSettings.set('openrouter_api_key', openrouter_key)
    
    if omdb_key and not omdb_key.startswith('*'):
        AppSettings.set('omdb_api_key', omdb_key)
    
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
    import requests
    
    openrouter_key = AppSettings.get('openrouter_api_key', '') or os.environ.get('OPENROUTER_API_KEY', '')
    
    if not openrouter_key:
        flash('Clé OpenRouter API non configurée.', 'error')
        return redirect(url_for('admin.settings'))
    
    try:
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {openrouter_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': request.host_url,
            },
            json={
                'model': 'google/gemini-2.5-flash',
                'messages': [
                    {
                        'role': 'user',
                        'content': 'Réponds juste "OK" si tu me reçois.'
                    }
                ],
                'max_tokens': 10
            },
            timeout=15
        )
        
        if response.status_code == 200:
            flash('OpenRouter API fonctionne correctement! ✅', 'success')
        else:
            flash(f'Erreur OpenRouter: {response.status_code} - {response.text[:200]}', 'error')
    except Exception as e:
        flash(f'Erreur lors du test OpenRouter: {str(e)}', 'error')
    
    return redirect(url_for('admin.settings'))

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

