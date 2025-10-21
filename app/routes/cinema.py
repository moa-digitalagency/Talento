from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.cinema_talent import CinemaTalent
from app.models import Country
from app.constants import LANGUAGES_CINEMA, TALENT_CATEGORIES
from app.services.movie_service import search_movies
from app.utils.file_handler import save_file
from app.data.world_countries import NATIONALITIES
from app.data.world_cities import get_cities_by_country
from datetime import datetime
import json

bp = Blueprint('cinema', __name__, url_prefix='/cinema')

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard CINEMA - Aperçu général du module cinéma"""
    total_talents = CinemaTalent.query.filter_by(is_active=True).count()
    return render_template('cinema/dashboard.html', total_talents=total_talents)

@bp.route('/talents')
@login_required
def talents():
    """Talents CINEMA - Gestion des talents spécifiques au cinéma"""
    talents_list = CinemaTalent.query.filter_by(is_active=True).order_by(CinemaTalent.created_at.desc()).all()
    return render_template('cinema/talents.html', talents=talents_list)

@bp.route('/productions')
@login_required
def productions():
    """Productions CINEMA - Gestion des productions"""
    return render_template('cinema/productions.html')

@bp.route('/projects')
@login_required
def projects():
    """Projets CINEMA - Gestion des projets"""
    return render_template('cinema/projects.html')

@bp.route('/team')
@login_required
def team():
    """Équipe Technique CINEMA - Gestion de l'équipe technique"""
    return render_template('cinema/team.html')

@bp.route('/api/search_movies', methods=['GET'])
def api_search_movies():
    """API proxy pour rechercher des films via TMDb"""
    query = request.args.get('query', '').strip()
    
    if not query or len(query) < 2:
        return jsonify({'results': []})
    
    result = search_movies(query)
    return jsonify(result)

@bp.route('/api/cities/<country_code>', methods=['GET'])
def api_get_cities(country_code):
    """API pour récupérer les villes d'un pays donné"""
    cities = get_cities_by_country(country_code.upper())
    return jsonify({'cities': cities, 'country_code': country_code.upper()})

@bp.route('/register', methods=['GET', 'POST'])
def register_talent():
    """Inscription d'un nouveau talent CINEMA"""
    # Get countries for dropdowns, sorted alphabetically
    countries = Country.query.order_by(Country.name).all()
    
    # Get nationalities list (sorted alphabetically)
    nationalities = NATIONALITIES
    
    if request.method == 'POST':
        try:
            talent = CinemaTalent()
            
            # Basic Info
            talent.first_name = request.form.get('first_name')
            talent.last_name = request.form.get('last_name')
            talent.gender = request.form.get('gender')
            
            date_of_birth = request.form.get('date_of_birth')
            if date_of_birth:
                talent.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            
            # ID Document
            talent.id_document_type = request.form.get('id_document_type')
            
            id_doc_number = request.form.get('id_document_number')
            if id_doc_number:
                from app.utils.encryption import encrypt_data
                talent.id_document_number_encrypted = encrypt_data(id_doc_number)
            
            # Origins - Multiple ethnicities
            ethnicities = request.form.getlist('ethnicities')
            if ethnicities:
                talent.ethnicities = json.dumps(ethnicities)
            
            talent.country_of_origin = request.form.get('country_of_origin')
            talent.nationality = request.form.get('nationality')
            
            # Residence - Convert country code to name
            country_code = request.form.get('country_of_residence')
            if country_code:
                country = Country.query.filter_by(code=country_code).first()
                talent.country_of_residence = country.name if country else country_code
            talent.city_of_residence = request.form.get('city_of_residence')
            
            # Languages - Multiple choices
            languages = request.form.getlist('languages')
            if languages:
                talent.languages_spoken = json.dumps(languages)
            
            years_exp = request.form.get('years_of_experience')
            talent.years_of_experience = int(years_exp) if years_exp else 0
            
            # Physical Characteristics
            talent.eye_color = request.form.get('eye_color')
            talent.hair_color = request.form.get('hair_color')
            talent.hair_type = request.form.get('hair_type')
            height = request.form.get('height')
            talent.height = int(height) if height else None
            talent.skin_tone = request.form.get('skin_tone')
            talent.build = request.form.get('build')
            
            # Other Talents - Multiple choices
            other_talents = request.form.getlist('other_talents')
            if other_talents:
                talent.other_talents = json.dumps(other_talents)
            
            if 'profile_photo' in request.files:
                photo = request.files['profile_photo']
                if photo.filename:
                    filename = save_file(photo, 'cinema_photos')
                    if filename:
                        talent.profile_photo_filename = filename
            
            if 'id_photo' in request.files:
                id_photo = request.files['id_photo']
                if id_photo.filename:
                    filename = save_file(id_photo, 'cinema_photos')
                    if filename:
                        talent.id_photo_filename = filename
            
            gallery_filenames = []
            if 'gallery_photos' in request.files:
                gallery_files = request.files.getlist('gallery_photos')
                for gallery_file in gallery_files:
                    if gallery_file.filename:
                        filename = save_file(gallery_file, 'cinema_photos')
                        if filename:
                            gallery_filenames.append(filename)
            if gallery_filenames:
                talent.gallery_photos = json.dumps(gallery_filenames)
            
            talent.email = request.form.get('email')
            
            existing_talent = CinemaTalent.query.filter_by(email=talent.email).first()
            if existing_talent:
                flash('Cet email est déjà utilisé dans CINEMA.', 'error')
                return render_template('cinema/register_talent.html', countries=countries, nationalities=nationalities, languages=LANGUAGES_CINEMA, talent_categories=TALENT_CATEGORIES)
            
            phone = request.form.get('phone')
            if phone:
                from app.utils.encryption import encrypt_data
                talent.phone_encrypted = encrypt_data(phone)
            
            whatsapp = request.form.get('whatsapp')
            if whatsapp:
                from app.utils.encryption import encrypt_data
                talent.whatsapp_encrypted = encrypt_data(whatsapp)
            
            # Social Media (all encrypted)
            social_media = {
                'facebook': request.form.get('facebook'),
                'instagram': request.form.get('instagram'),
                'linkedin': request.form.get('linkedin'),
                'twitter': request.form.get('twitter'),
                'youtube': request.form.get('youtube'),
                'tiktok': request.form.get('tiktok'),
                'snapchat': request.form.get('snapchat')
            }
            
            from app.utils.encryption import encrypt_data
            for key, value in social_media.items():
                if value:
                    setattr(talent, f'{key}_encrypted', encrypt_data(value))
            
            # Previous Productions (JSON)
            talent.previous_productions = request.form.get('previous_productions')
            
            db.session.add(talent)
            db.session.commit()
            
            flash(f'Talent {talent.first_name} {talent.last_name} enregistré avec succès dans CINEMA!', 'success')
            return redirect(url_for('cinema.talents'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de l\'enregistrement: {str(e)}', 'error')
            return render_template('cinema/register_talent.html', 
                                 countries=countries,
                                 nationalities=nationalities,
                                 languages=LANGUAGES_CINEMA,
                                 talent_categories=TALENT_CATEGORIES)
    
    return render_template('cinema/register_talent.html', 
                         countries=countries,
                         nationalities=nationalities,
                         languages=LANGUAGES_CINEMA,
                         talent_categories=TALENT_CATEGORIES)
