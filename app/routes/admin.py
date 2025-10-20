from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, jsonify, current_app
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime
from sqlalchemy import or_, and_, func
from app import db
from app.models.user import User
from app.models.talent import Talent, UserTalent
from app.models.location import Country, City
from app.models.settings import AppSettings
from app.services.export_service import ExportService
from app.services.cv_analyzer import CVAnalyzerService
from app.services.email_service import EmailService
import io
import os
import secrets
import string

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Accès réservé aux administrateurs.', 'error')
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
@admin_required
def users():
    all_users = User.query.filter(User.is_admin == False).order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users)


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
        return redirect(url_for('main.index'))
    
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé avec succès.', 'success')
    return redirect(url_for('main.index'))

@bp.route('/export/excel')
@login_required
@admin_required
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
@admin_required
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
@admin_required
def export_pdf():
    users = User.query.filter(User.is_admin == False).all()
    pdf_bytes = ExportService.export_list_to_pdf(users, current_user=current_user)
    
    buffer = io.BytesIO(pdf_bytes)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'talento_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )

@bp.route('/export/pdf/<int:user_id>')
@login_required
@admin_required
def export_pdf_individual(user_id):
    user = User.query.get_or_404(user_id)
    pdf_bytes = ExportService.export_talent_card_pdf(user)
    
    buffer = io.BytesIO(pdf_bytes)
    buffer.seek(0)
    
    filename = f'talento_{user.unique_code}_{datetime.now().strftime("%Y%m%d")}.pdf'
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

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
            flash('Tous les champs sont requis.', 'error')
            return redirect(url_for('admin.new_talent'))
        
        existing = Talent.query.filter_by(name=name).first()
        if existing:
            flash('Ce talent existe déjà.', 'error')
            return redirect(url_for('admin.new_talent'))
        
        talent = Talent(name=name, emoji=emoji, category=category)
        db.session.add(talent)
        db.session.commit()
        
        flash('Talent ajouté avec succès.', 'success')
        return redirect(url_for('main.index'))
    
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
    
    usage_count = UserTalent.query.filter_by(talent_id=talent_id).count()
    if usage_count > 0:
        flash(f'Impossible de supprimer ce talent. Il est utilisé par {usage_count} profil(s).', 'error')
        return redirect(url_for('admin.talents_list'))
    
    db.session.delete(talent)
    db.session.commit()
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
    
    return render_template('admin/settings.html', admin_users=admin_users, config=config_info)

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

@bp.route('/save-settings', methods=['POST'])
@login_required
@admin_required
def save_settings():
    sendgrid_key = request.form.get('sendgrid_api_key', '').strip()
    openrouter_key = request.form.get('openrouter_api_key', '').strip()
    sender_email = request.form.get('sender_email', '').strip() or 'noreply@myoneart.com'
    
    if sendgrid_key and not sendgrid_key.startswith('*'):
        AppSettings.set('sendgrid_api_key', sendgrid_key)
    
    if openrouter_key and not openrouter_key.startswith('*'):
        AppSettings.set('openrouter_api_key', openrouter_key)
    
    AppSettings.set('sender_email', sender_email)
    
    flash('Paramètres sauvegardés avec succès.', 'success')
    return redirect(url_for('admin.settings'))

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
