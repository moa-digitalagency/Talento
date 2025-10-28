"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.talent import UserTalent, Talent
from app.models.location import Country, City
from app.models.cinema_talent import CinemaTalent
from app.utils.file_handler import save_file
from app.services.cv_analyzer import CVAnalyzerService
import os
import json
from datetime import datetime

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/')
@login_required
def view():
    """Affiche le profil de l'utilisateur connecté selon son type"""
    # Si un unique_code est passé en paramètre, rediriger vers la vue publique
    unique_code = request.args.get('unique_code')
    if unique_code:
        return redirect(url_for('profile.view_public', unique_code=unique_code))
    
    # Déterminer le type d'utilisateur
    profile_type = 'admin' if current_user.is_admin else 'user'
    cinema_talent = None
    
    # Vérifier si l'utilisateur est aussi un talent cinéma via le code unique (sécurisé)
    # Ne jamais utiliser l'email seul pour lier les profils car plusieurs users peuvent avoir le même email
    if current_user.unique_code:
        cinema_talent = CinemaTalent.query.filter_by(unique_code=current_user.unique_code).first()
        if cinema_talent:
            profile_type = 'cinema'
    
    # Préparer l'analyse CV si disponible
    cv_analysis_data = None
    if current_user.cv_analysis:
        try:
            cv_analysis_data = json.loads(current_user.cv_analysis)
        except:
            cv_analysis_data = None
    
    return render_template('profile/view.html', 
                         user=current_user,
                         cinema_talent=cinema_talent,
                         profile_type=profile_type,
                         cv_analysis=cv_analysis_data)

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('profile/dashboard.html', user=current_user)

@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        try:
            # SÉCURITÉ: Les champs suivants sont VERROUILLÉS et ne peuvent pas être modifiés
            # - first_name, last_name (identité)
            # - email (identifiant)
            # - date_of_birth (âge)
            # - gender (identité)
            # - passport_number, residence_card (documents)
            # - unique_code (identifiant unique)
            # Ces champs sont ignorés même si présents dans le POST
            
            # Champs modifiables uniquement
            current_user.phone = request.form.get('phone', '').strip() or None
            current_user.whatsapp = request.form.get('whatsapp', '').strip() or None
            current_user.address = request.form.get('address', '').strip() or None
            
            country_id = request.form.get('country_id')
            current_user.country_id = int(country_id) if country_id else None
            
            city_id = request.form.get('city_id')
            current_user.city_id = int(city_id) if city_id else None
            
            current_user.availability = request.form.get('availability')
            current_user.work_mode = request.form.get('work_mode')
            current_user.rate_range = request.form.get('rate_range', '').strip() or None
            years_exp = request.form.get('years_experience')
            current_user.years_experience = int(years_exp) if years_exp else None
            
            current_user.bio = request.form.get('bio', '').strip() or None
            current_user.portfolio_url = request.form.get('portfolio_url', '').strip() or None
            current_user.website = request.form.get('website', '').strip() or None
            
            current_user.linkedin = request.form.get('linkedin', '').strip() or None
            current_user.instagram = request.form.get('instagram', '').strip() or None
            current_user.twitter = request.form.get('twitter', '').strip() or None
            current_user.facebook = request.form.get('facebook', '').strip() or None
            current_user.github = request.form.get('github', '').strip() or None
            current_user.behance = request.form.get('behance', '').strip() or None
            current_user.dribbble = request.form.get('dribbble', '').strip() or None
            current_user.youtube = request.form.get('youtube', '').strip() or None
            current_user.tiktok = request.form.get('tiktok', '').strip() or None
            current_user.snapchat = request.form.get('snapchat', '').strip() or None
            current_user.telegram = request.form.get('telegram', '').strip() or None
            current_user.pinterest = request.form.get('pinterest', '').strip() or None
            current_user.imdb_url = request.form.get('imdb_url', '').strip() or None
            current_user.threads = request.form.get('threads', '').strip() or None
            
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo.filename:
                    filename = save_file(photo, 'photo')
                    if filename:
                        current_user.photo_filename = filename
            
            cv_file_updated = False
            if 'cv' in request.files:
                cv = request.files['cv']
                if cv.filename:
                    filename = save_file(cv, 'cv')
                    if filename:
                        current_user.cv_filename = filename
                        cv_file_updated = True
            
            talent_ids = request.form.getlist('talents')
            UserTalent.query.filter_by(user_id=current_user.id).delete()
            for talent_id in talent_ids:
                if talent_id:
                    user_talent = UserTalent(user_id=current_user.id, talent_id=int(talent_id))
                    db.session.add(user_talent)
            
            if cv_file_updated and current_user.cv_filename:
                try:
                    cv_path = os.path.join('app', 'static', 'uploads', 'cvs', current_user.cv_filename)
                    if os.path.exists(cv_path):
                        analysis_result = CVAnalyzerService.analyze_cv(current_user.cv_filename, {
                            'name': current_user.full_name,
                            'talents': talent_ids,
                            'location': f"{current_user.city.name if current_user.city else ''}, {current_user.country.name if current_user.country else ''}"
                        })
                        
                        if analysis_result.get('success'):
                            current_user.cv_analysis = json.dumps(analysis_result, ensure_ascii=False)
                            current_user.profile_score = analysis_result.get('score', 0)
                            current_user.cv_analyzed_at = datetime.utcnow()
                except Exception as e:
                    flash(f'Le profil a été mis à jour mais l\'analyse du CV a échoué: {str(e)}', 'warning')
            
            db.session.commit()
            flash('Votre profil a été mis à jour avec succès.', 'success')
            return redirect(url_for('profile.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Une erreur est survenue: {str(e)}', 'error')
    
    countries = Country.query.order_by(Country.name).all()
    cities = City.query.order_by(City.name).all()
    all_talents = Talent.query.order_by(Talent.category, Talent.name).all()
    user_talent_ids = [ut.talent_id for ut in current_user.talents]
    
    return render_template('profile/edit.html', 
                         user=current_user,
                         countries=countries,
                         cities=cities,
                         all_talents=all_talents,
                         user_talent_ids=user_talent_ids)

@bp.route('/view/<unique_code>')
def view_public(unique_code):
    """Affiche le profil public d'un utilisateur via son code unique"""
    user = User.query.filter_by(unique_code=unique_code.replace('-', '')).first_or_404()
    
    cv_analysis_data = None
    if user.cv_analysis:
        try:
            cv_analysis_data = json.loads(user.cv_analysis)
        except:
            cv_analysis_data = None
    
    return render_template('profile/view.html', user=user, cv_analysis=cv_analysis_data, profile_type='user', cinema_talent=None)

@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Permet à l'utilisateur de changer son mot de passe"""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Vérifier l'ancien mot de passe
        if not current_user.check_password(current_password):
            flash('Le mot de passe actuel est incorrect.', 'error')
            return render_template('profile/change_password.html')
        
        # Vérifier que le nouveau mot de passe est différent de l'ancien
        if current_password == new_password:
            flash('Le nouveau mot de passe doit être différent de l\'ancien.', 'error')
            return render_template('profile/change_password.html')
        
        # Vérifier la confirmation
        if new_password != confirm_password:
            flash('Les nouveaux mots de passe ne correspondent pas.', 'error')
            return render_template('profile/change_password.html')
        
        # Vérifier la longueur minimale
        if len(new_password) < 6:
            flash('Le mot de passe doit contenir au moins 6 caractères.', 'error')
            return render_template('profile/change_password.html')
        
        try:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Votre mot de passe a été changé avec succès!', 'success')
            return redirect(url_for('profile.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Une erreur est survenue: {str(e)}', 'error')
    
    return render_template('profile/change_password.html')

@bp.route('/resend_credentials/<unique_code>', methods=['POST'])
@login_required
def resend_credentials(unique_code):
    """Renvoie les identifiants de connexion par email"""
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('main.index'))
    
    user = User.query.filter_by(unique_code=unique_code).first_or_404()
    
    try:
        from app.services.email_service import email_service
        from app.utils.email_service import generate_random_password
        
        # Générer un nouveau mot de passe
        new_password = generate_random_password()
        user.set_password(new_password)
        
        # Envoyer les nouveaux identifiants par email
        email_sent = email_service.send_login_credentials(user, new_password)
        
        if email_sent:
            db.session.commit()
            flash(f'Les identifiants ont été renvoyés à {user.email}', 'success')
        else:
            db.session.rollback()
            flash(f'Erreur lors de l\'envoi de l\'email. Vérifiez la configuration SendGrid.', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur: {str(e)}', 'error')
    
    return redirect(url_for('profile.view_public', unique_code=unique_code))
