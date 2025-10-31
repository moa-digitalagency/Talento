"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user
from app import db
from app.models.user import User
from app.services.logging_service import LoggingService
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
            
            # Log successful login
            LoggingService.log_activity(
                user=user,
                action_type='login',
                action_category='auth',
                description=f'Connexion réussie',
                status='success'
            )
            LoggingService.log_security_event(
                event_type='successful_login',
                description=f'Connexion réussie pour {user.email}',
                severity='info',
                user=user
            )
            
            next_page = request.args.get('next')
            if user.is_admin:
                return redirect(next_page or url_for('admin.dashboard'))
            elif user.role == 'recruteur':
                return redirect(next_page or url_for('admin.users'))
            return redirect(next_page or url_for('profile.dashboard'))
        else:
            # Log failed login attempt
            LoggingService.log_security_event(
                event_type='failed_login',
                description=f'Tentative de connexion échouée',
                severity='warning',
                attempted_username=identifier
            )
            flash('Identifiant ou mot de passe incorrect.', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        user = current_user._get_current_object()
        
        # Log logout
        LoggingService.log_activity(
            user=user,
            action_type='logout',
            action_category='auth',
            description='Déconnexion',
            status='success'
        )
    
    logout_user()
    flash('Vous avez été déconnecté avec succès.', 'success')
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile.dashboard'))
    
    # Préparer les données pour le formulaire (GET et POST pour affichage après erreur)
    from app.models.location import Country
    from app.models.talent import Talent
    from app.data.world_countries import NATIONALITIES_WITH_FLAGS
    
    countries = Country.query.order_by(Country.name).all()
    talents = Talent.query.order_by(Talent.category, Talent.name).all()
    nationalities = NATIONALITIES_WITH_FLAGS
    
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
            from app.utils.validation_service import ValidationService
            
            # Récupérer et valider l'email et le téléphone avant de créer l'utilisateur
            email_input = request.form.get('email')
            phone_input = request.form.get('phone')
            
            country_id = request.form.get('country_id')
            
            # Déterminer le code pays pour la validation du téléphone
            country_code = 'MA'  # Par défaut Maroc
            if country_id:
                country = Country.query.get(int(country_id))
                if country:
                    country_code = country.code
            
            # Valider l'email
            email_validation = ValidationService.validate_email(email_input, check_deliverability=True)
            if not email_validation.is_valid:
                flash(f"Email invalide: {email_validation.error_message}", 'error')
                return render_template('auth/register.html', countries=countries, talents=talents, nationalities=nationalities)
            
            # Valider le téléphone si fourni
            phone_validation = None
            if phone_input:
                phone_validation = ValidationService.validate_phone(phone_input, country_code)
                if not phone_validation.is_valid:
                    flash(f"Numéro de téléphone invalide: {phone_validation.error_message}", 'error')
                    return render_template('auth/register.html', countries=countries, talents=talents, nationalities=nationalities)
            
            user = User()
            user.first_name = request.form.get('first_name')
            user.last_name = request.form.get('last_name')
            user.email = email_validation.normalized_value  # Utiliser l'email normalisé
            user.phone = phone_validation.normalized_value if phone_validation else None  # Format E.164
            user.whatsapp = request.form.get('whatsapp')
            user.address = request.form.get('address')
            user.gender = request.form.get('gender')
            user.passport_number = request.form.get('passport_number')
            user.residence_card = request.form.get('residence_card')
            
            user.country_id = int(country_id) if country_id else None
            city_id = request.form.get('city_id')
            user.city_id = int(city_id) if city_id else None
            user.nationality = request.form.get('nationality')
            residence_country_id = request.form.get('residence_country_id')
            residence_city_id = request.form.get('residence_city_id')
            user.residence_country_id = int(residence_country_id) if residence_country_id else None
            user.residence_city_id = int(residence_city_id) if residence_city_id else None
            
            user.portfolio_url = request.form.get('portfolio_url')
            user.website = request.form.get('website_url')
            user.linkedin = request.form.get('linkedin_url')
            user.instagram = request.form.get('instagram_url')
            user.twitter = request.form.get('twitter_url')
            user.facebook = request.form.get('facebook_url')
            user.tiktok = request.form.get('tiktok_url')
            user.youtube = request.form.get('youtube_url')
            user.github = request.form.get('github_url')
            user.behance = request.form.get('behance_url')
            user.dribbble = request.form.get('dribbble_url')
            user.pinterest = request.form.get('pinterest_url')
            user.snapchat = request.form.get('snapchat_url')
            user.telegram = request.form.get('telegram_url')
            user.imdb_url = request.form.get('imdb_url')
            user.threads = request.form.get('threads_url')
            
            user.bio = request.form.get('bio')
            user.education = request.form.get('education')
            years_exp = request.form.get('years_experience')
            user.years_experience = int(years_exp) if years_exp else None
            
            # Languages (checkboxes - multiple selection)
            languages = request.form.getlist('languages')
            if languages:
                user.languages = ', '.join(languages)
            
            # Availability and work mode
            user.availability = request.form.get('availability')
            user.work_mode = request.form.get('work_mode')
            
            # Rate range (combine hourly_rate and monthly_rate)
            hourly_rate = request.form.get('hourly_rate')
            monthly_rate = request.form.get('monthly_rate')
            if hourly_rate or monthly_rate:
                rate_parts = []
                if hourly_rate:
                    rate_parts.append(f"{hourly_rate} MAD/h")
                if monthly_rate:
                    rate_parts.append(f"{monthly_rate} MAD/mois")
                user.rate_range = ' | '.join(rate_parts)
            
            date_of_birth = request.form.get('date_of_birth')
            if date_of_birth:
                user.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            
            existing_user = User.query.filter_by(email=user.email).first()
            if existing_user:
                flash('Cet email est déjà utilisé.', 'error')
                return render_template('auth/register.html', countries=countries, talents=talents, nationalities=nationalities)
            
            residence_country = Country.query.get(user.residence_country_id) if user.residence_country_id else None
            residence_city = City.query.get(user.residence_city_id) if user.residence_city_id else None
            
            if not residence_country or not residence_city:
                flash('Veuillez sélectionner un pays de résidence et une ville de résidence.', 'error')
                return render_template('auth/register.html', countries=countries, talents=talents, nationalities=nationalities)
            
            user.unique_code = generate_unique_user_code(
                residence_country.code,
                residence_city.code,
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
            
            # Log registration
            LoggingService.log_activity(
                user=user,
                action_type='create',
                action_category='auth',
                description=f'Nouvelle inscription : {user.full_name} ({user.email})',
                resource_type='User',
                resource_id=user.id,
                status='success',
                metadata={'talents_count': len(talent_ids), 'has_cv': bool(cv_file_path)}
            )
            LoggingService.log_security_event(
                event_type='new_registration',
                description=f'Nouveau compte créé : {user.email}',
                severity='info',
                user=user
            )
            
            try:
                email_service.send_application_confirmation(user)
                email_service.send_login_credentials(user, password)
            except Exception as e:
                current_app.logger.error(f"Erreur envoi emails: {str(e)}")
            
            # Vérifier si la personne est dans la liste de surveillance
            try:
                from app.services.watchlist_service import check_watchlist_and_notify
                check_watchlist_and_notify(user, talent_type='talent')
            except Exception as e:
                current_app.logger.error(f"Erreur watchlist: {str(e)}")
            
            flash('Votre profil a été créé avec succès ! Vérifiez votre email pour vos identifiants de connexion.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Une erreur est survenue: {str(e)}', 'error')
            return render_template('auth/register.html', countries=countries, talents=talents, nationalities=nationalities)
    
    return render_template('auth/register.html', countries=countries, talents=talents, nationalities=nationalities)
