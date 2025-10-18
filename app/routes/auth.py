from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('profile.dashboard'))
        else:
            flash('Email ou mot de passe incorrect.', 'error')
    
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
        from app.utils.email_service import generate_random_password, send_confirmation_email
        from app.utils.file_handler import save_file
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
                from datetime import datetime
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
            
            if 'cv' in request.files:
                cv = request.files['cv']
                if cv.filename:
                    filename = save_file(cv, 'cv')
                    if filename:
                        user.cv_filename = filename
            
            db.session.add(user)
            db.session.flush()
            
            talent_ids = request.form.getlist('talents')
            for talent_id in talent_ids:
                user_talent = UserTalent(user_id=user.id, talent_id=int(talent_id))
                db.session.add(user_talent)
            
            qr_path = os.path.join('app', 'static', 'uploads', 'qrcodes')
            qr_filename = generate_qr_code(user.unique_code, qr_path)
            user.qr_code_filename = qr_filename
            
            db.session.commit()
            
            send_confirmation_email(user, password)
            
            flash('Votre profil a été créé avec succès ! Vérifiez votre email pour vos identifiants de connexion.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Une erreur est survenue: {str(e)}', 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')
