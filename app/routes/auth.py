from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user
from app import db
from app.models.user import User
from datetime import datetime
import json
import os

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile.dashboard'))
    
    if request.method == 'POST':
        identifier = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=identifier).first()
        if not user:
            user = User.query.filter_by(unique_code=identifier).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            if user.is_admin:
                return redirect(next_page or url_for('admin.dashboard'))
            return redirect(next_page or url_for('profile.dashboard'))
        else:
            flash('Identifiant ou mot de passe incorrect.', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    flash('Vous avez été déconnecté avec succès.', 'success')
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile.dashboard'))
    
    if request.method == 'POST':
        from app.models.talent import UserTalent
        from app.models.location import Country, City
        from app.utils.id_generator import generate_unique_user_code
        from app.utils.qr_generator import generate_qr_code
        from app.utils.email_service import generate_random_password
        from app.utils.file_handler import save_file
        from app.services.email_service import email_service
        from app.services.cv_analyzer import CVAnalyzerService
        import os
        
        try:
            user = User()
            user.first_name = request.form.get('first_name')
            user.last_name = request.form.get('last_name')
            user.email = request.form.get('email')
            user.phone = request.form.get('phone')
            user.whatsapp = request.form.get('whatsapp')
            user.address = request.form.get('address')
            user.gender = request.form.get('gender')
            
            country_id = request.form.get('country_id')
            city_id = request.form.get('city_id')
            user.country_id = int(country_id) if country_id else None
            user.city_id = int(city_id) if city_id else None
            
            user.portfolio_url = request.form.get('portfolio_url')
            user.linkedin = request.form.get('linkedin')
            user.instagram = request.form.get('instagram')
            user.twitter = request.form.get('twitter')
            user.facebook = request.form.get('facebook')
            user.tiktok = request.form.get('tiktok')
            user.youtube = request.form.get('youtube')
            user.github = request.form.get('github')
            user.behance = request.form.get('behance')
            user.dribbble = request.form.get('dribbble')
            user.pinterest = request.form.get('pinterest')
            user.snapchat = request.form.get('snapchat')
            user.telegram = request.form.get('telegram')
            
            user.bio = request.form.get('bio')
            years_exp = request.form.get('years_experience')
            user.years_experience = int(years_exp) if years_exp else None
            
            date_of_birth = request.form.get('date_of_birth')
            if date_of_birth:
                user.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            
            existing_user = User.query.filter_by(email=user.email).first()
            if existing_user:
                flash('Cet email est déjà utilisé.', 'error')
                return render_template('auth/register.html')
            
            country = Country.query.get(user.country_id)
            city = City.query.get(user.city_id)
            
            if not country or not city:
                flash('Veuillez sélectionner un pays et une ville.', 'error')
                return render_template('auth/register.html')
            
            user.unique_code = generate_unique_user_code(
                country.code,
                city.code,
                user.gender or 'N'
            )
            
            password = generate_random_password()
            user.set_password(password)
            
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo.filename:
                    filename = save_file(photo, 'photo')
                    if filename:
                        user.photo_filename = filename
            
            cv_file_path = None
            if 'cv' in request.files:
                cv = request.files['cv']
                if cv.filename:
                    filename = save_file(cv, 'cv')
                    if filename:
                        user.cv_filename = filename
                        cv_file_path = os.path.join('app', 'static', 'uploads', 'cvs', filename)
            
            db.session.add(user)
            db.session.flush()
            
            talent_ids = request.form.getlist('talents')
            for talent_id in talent_ids:
                user_talent = UserTalent(user_id=user.id, talent_id=int(talent_id))
                db.session.add(user_talent)
            
            qr_path = os.path.join('app', 'static', 'uploads', 'qrcodes')
            qr_filename = generate_qr_code(user.unique_code, qr_path)
            user.qr_code_filename = qr_filename
            
            if cv_file_path and os.path.exists(cv_file_path):
                try:
                    analysis_result = CVAnalyzerService.analyze_cv(user.cv_filename, {
                        'name': user.full_name,
                        'talents': [talent_id for talent_id in talent_ids],
                        'location': f"{user.city.name if user.city else ''}, {user.country.name if user.country else ''}"
                    })
                    
                    if analysis_result.get('success'):
                        user.cv_analysis = json.dumps(analysis_result, ensure_ascii=False)
                        user.profile_score = analysis_result.get('score', 0)
                        user.cv_analyzed_at = datetime.utcnow()
                except Exception as e:
                    current_app.logger.error(f"Erreur analyse CV: {str(e)}")
            
            db.session.commit()
            
            try:
                email_service.send_application_confirmation(user)
                email_service.send_login_credentials(user, password)
            except Exception as e:
                current_app.logger.error(f"Erreur envoi emails: {str(e)}")
            
            flash('Votre profil a été créé avec succès ! Vérifiez votre email pour vos identifiants de connexion.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Une erreur est survenue: {str(e)}', 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')
