from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.talent import UserTalent, Talent
from app.models.location import Country, City
from app.utils.file_handler import save_file
from app.services.cv_analyzer import CVAnalyzerService
import os
import json
from datetime import datetime

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('profile/dashboard.html', user=current_user)

@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        try:
            current_user.first_name = request.form.get('first_name', '').strip()
            current_user.last_name = request.form.get('last_name', '').strip()
            
            dob_str = request.form.get('date_of_birth')
            if dob_str:
                try:
                    current_user.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            current_user.gender = request.form.get('gender')
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
def view(unique_code):
    user = User.query.filter_by(unique_code=unique_code.replace('-', '')).first_or_404()
    
    cv_analysis_data = None
    if user.cv_analysis:
        try:
            cv_analysis_data = json.loads(user.cv_analysis)
        except:
            cv_analysis_data = None
    
    return render_template('profile/view.html', user=user, cv_analysis=cv_analysis_data)
