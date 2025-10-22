from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_file
from flask_login import login_required, current_user
from app import db
from app.models.cinema_talent import CinemaTalent
from app.models.production import Production
from app.models import Country
from app.constants import (
    LANGUAGES_CINEMA, TALENT_CATEGORIES, CINEMA_TALENT_TYPES,
    EYE_COLORS, HAIR_COLORS, HAIR_TYPES, SKIN_TONES, BUILD_TYPES
)
from app.services.movie_service import search_movies
from app.services.export_service import ExportService
from app.utils.file_handler import save_file
from app.data.world_countries import NATIONALITIES, NATIONALITIES_WITH_FLAGS
from app.data.world_cities import get_cities_by_country
from datetime import datetime
import json
import io

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
    
    # Récupérer tous les pays de la base de données pour les filtres
    countries = Country.query.order_by(Country.name).all()
    
    # Utiliser TOUJOURS les constantes complètes pour les filtres
    # (même principe que le formulaire d'inscription - synchronisation totale)
    return render_template('cinema/talents.html', 
                         talents=talents_list,
                         countries=countries,
                         languages=LANGUAGES_CINEMA,
                         cinema_talent_types=CINEMA_TALENT_TYPES,
                         eye_colors=EYE_COLORS,
                         hair_colors=HAIR_COLORS,
                         hair_types=HAIR_TYPES,
                         skin_tones=SKIN_TONES,
                         build_types=BUILD_TYPES)

@bp.route('/productions')
@login_required
def productions():
    """Boîtes de production CINEMA - Gestion des boîtes de production"""
    productions_list = Production.query.filter_by(is_active=True).order_by(Production.created_at.desc()).all()
    return render_template('cinema/productions.html', productions=productions_list)

@bp.route('/productions/new', methods=['GET', 'POST'])
@login_required
def add_production():
    """Ajouter une nouvelle boîte de production"""
    if request.method == 'POST':
        try:
            production = Production()
            
            # Informations de base
            production.name = request.form.get('name')
            production.logo_url = request.form.get('logo_url')
            production.description = request.form.get('description')
            production.specialization = request.form.get('specialization')
            
            # Coordonnées
            production.address = request.form.get('address')
            production.city = request.form.get('city')
            production.country = request.form.get('country')
            production.postal_code = request.form.get('postal_code')
            
            # Contact
            production.phone = request.form.get('phone')
            production.email = request.form.get('email')
            production.website = request.form.get('website')
            
            # Réseaux sociaux
            production.facebook = request.form.get('facebook')
            production.instagram = request.form.get('instagram')
            production.linkedin = request.form.get('linkedin')
            production.twitter = request.form.get('twitter')
            
            # Informations sur l'entreprise
            founded_year = request.form.get('founded_year')
            if founded_year:
                production.founded_year = int(founded_year)
            
            production.ceo = request.form.get('ceo')
            
            employees_count = request.form.get('employees_count')
            if employees_count:
                production.employees_count = int(employees_count)
            
            # Productions
            productions_count = request.form.get('productions_count')
            if productions_count:
                production.productions_count = int(productions_count)
            
            production.notable_productions = request.form.get('notable_productions')
            
            # Services offerts
            production.services = request.form.get('services')
            
            # Équipements et studios
            production.equipment = request.form.get('equipment')
            production.studios = request.form.get('studios')
            
            # Certifications et affiliations
            production.certifications = request.form.get('certifications')
            production.memberships = request.form.get('memberships')
            
            # Récompenses
            production.awards = request.form.get('awards')
            
            # Statut
            production.is_verified = request.form.get('is_verified') == 'on'
            
            # Métadonnées
            production.created_by = current_user.id
            
            db.session.add(production)
            db.session.commit()
            
            flash(f'Boîte de production "{production.name}" créée avec succès!', 'success')
            return redirect(url_for('cinema.productions'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la création de la boîte de production: {str(e)}', 'error')
    
    return render_template('cinema/production_form.html')

@bp.route('/productions/<int:production_id>')
@login_required
def view_production(production_id):
    """Afficher les détails d'une boîte de production"""
    production = Production.query.get_or_404(production_id)
    return render_template('cinema/production_detail.html', production=production)

@bp.route('/productions/<int:production_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_production(production_id):
    """Modifier une boîte de production existante"""
    production = Production.query.get_or_404(production_id)
    
    if request.method == 'POST':
        try:
            # Informations de base
            production.name = request.form.get('name')
            production.logo_url = request.form.get('logo_url')
            production.description = request.form.get('description')
            production.specialization = request.form.get('specialization')
            
            # Coordonnées
            production.address = request.form.get('address')
            production.city = request.form.get('city')
            production.country = request.form.get('country')
            production.postal_code = request.form.get('postal_code')
            
            # Contact
            production.phone = request.form.get('phone')
            production.email = request.form.get('email')
            production.website = request.form.get('website')
            
            # Réseaux sociaux
            production.facebook = request.form.get('facebook')
            production.instagram = request.form.get('instagram')
            production.linkedin = request.form.get('linkedin')
            production.twitter = request.form.get('twitter')
            
            # Informations sur l'entreprise
            founded_year = request.form.get('founded_year')
            if founded_year:
                production.founded_year = int(founded_year)
            
            production.ceo = request.form.get('ceo')
            
            employees_count = request.form.get('employees_count')
            if employees_count:
                production.employees_count = int(employees_count)
            
            # Productions
            productions_count = request.form.get('productions_count')
            if productions_count:
                production.productions_count = int(productions_count)
            
            production.notable_productions = request.form.get('notable_productions')
            
            # Services offerts
            production.services = request.form.get('services')
            
            # Équipements et studios
            production.equipment = request.form.get('equipment')
            production.studios = request.form.get('studios')
            
            # Certifications et affiliations
            production.certifications = request.form.get('certifications')
            production.memberships = request.form.get('memberships')
            
            # Récompenses
            production.awards = request.form.get('awards')
            
            # Statut
            production.is_verified = request.form.get('is_verified') == 'on'
            
            db.session.commit()
            flash(f'Boîte de production "{production.name}" mise à jour avec succès!', 'success')
            return redirect(url_for('cinema.view_production', production_id=production.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la mise à jour de la boîte de production: {str(e)}', 'error')
    
    return render_template('cinema/production_form.html', production=production)

@bp.route('/productions/<int:production_id>/delete', methods=['POST'])
@login_required
def delete_production(production_id):
    """Supprimer une boîte de production (soft delete)"""
    production = Production.query.get_or_404(production_id)
    try:
        production.is_active = False
        db.session.commit()
        flash(f'Boîte de production "{production.name}" supprimée avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression de la boîte de production: {str(e)}', 'error')
    return redirect(url_for('cinema.productions'))

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
    
    # Get nationalities list with flags (sorted alphabetically)
    nationalities = NATIONALITIES_WITH_FLAGS
    
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
                return render_template('cinema/register_talent.html', 
                                     countries=countries, 
                                     nationalities=nationalities, 
                                     languages=LANGUAGES_CINEMA, 
                                     talent_categories=TALENT_CATEGORIES,
                                     cinema_talent_types=CINEMA_TALENT_TYPES,
                                     eye_colors=EYE_COLORS,
                                     hair_colors=HAIR_COLORS,
                                     hair_types=HAIR_TYPES,
                                     skin_tones=SKIN_TONES,
                                     build_types=BUILD_TYPES)
            
            phone = request.form.get('phone')
            if phone:
                from app.utils.encryption import encrypt_data
                talent.phone_encrypted = encrypt_data(phone)
            
            whatsapp = request.form.get('whatsapp')
            if whatsapp:
                from app.utils.encryption import encrypt_data
                talent.whatsapp_encrypted = encrypt_data(whatsapp)
            
            # Website (not encrypted)
            talent.website = request.form.get('website')
            
            # Social Media (all encrypted)
            social_media = {
                'facebook': request.form.get('facebook'),
                'instagram': request.form.get('instagram'),
                'linkedin': request.form.get('linkedin'),
                'twitter': request.form.get('twitter'),
                'youtube': request.form.get('youtube'),
                'tiktok': request.form.get('tiktok'),
                'snapchat': request.form.get('snapchat'),
                'imdb_url': request.form.get('imdb_url'),
                'threads': request.form.get('threads')
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
                                 talent_categories=TALENT_CATEGORIES,
                                 cinema_talent_types=CINEMA_TALENT_TYPES,
                                 eye_colors=EYE_COLORS,
                                 hair_colors=HAIR_COLORS,
                                 hair_types=HAIR_TYPES,
                                 skin_tones=SKIN_TONES,
                                 build_types=BUILD_TYPES)
    
    return render_template('cinema/register_talent.html', 
                         countries=countries,
                         nationalities=nationalities,
                         languages=LANGUAGES_CINEMA,
                         talent_categories=TALENT_CATEGORIES,
                         cinema_talent_types=CINEMA_TALENT_TYPES,
                         eye_colors=EYE_COLORS,
                         hair_colors=HAIR_COLORS,
                         hair_types=HAIR_TYPES,
                         skin_tones=SKIN_TONES,
                         build_types=BUILD_TYPES)

@bp.route('/profile/<unique_code>')
def view_profile(unique_code):
    """Visualisation publique d'un profil CINEMA via code unique"""
    talent = CinemaTalent.query.filter_by(unique_code=unique_code, is_active=True).first_or_404()
    
    # Décrypter les données sensibles pour l'affichage
    from app.utils.encryption import decrypt_sensitive_data
    
    decrypted_data = {}
    
    # Décrypter numéro de document d'identité
    if talent.id_document_number_encrypted:
        decrypted_data['id_document_number'] = decrypt_sensitive_data(talent.id_document_number_encrypted)
    
    # Décrypter téléphone et WhatsApp
    if talent.phone_encrypted:
        decrypted_data['phone'] = decrypt_sensitive_data(talent.phone_encrypted)
    if talent.whatsapp_encrypted:
        decrypted_data['whatsapp'] = decrypt_sensitive_data(talent.whatsapp_encrypted)
    
    # Décrypter réseaux sociaux
    social_fields = ['facebook', 'instagram', 'linkedin', 'twitter', 'youtube', 'tiktok', 'snapchat', 'telegram', 'imdb_url', 'threads']
    for field in social_fields:
        encrypted_field = f'{field}_encrypted'
        if hasattr(talent, encrypted_field):
            encrypted_value = getattr(talent, encrypted_field)
            if encrypted_value:
                decrypted_data[field] = decrypt_sensitive_data(encrypted_value)
    
    # Parser les données JSON
    parsed_data = {}
    
    if talent.ethnicities:
        try:
            parsed_data['ethnicities'] = json.loads(talent.ethnicities)
        except:
            parsed_data['ethnicities'] = []
    
    if talent.languages_spoken:
        try:
            parsed_data['languages'] = json.loads(talent.languages_spoken)
        except:
            parsed_data['languages'] = []
    
    if talent.talent_types:
        try:
            parsed_data['talent_types'] = json.loads(talent.talent_types)
        except:
            parsed_data['talent_types'] = []
    
    if talent.other_talents:
        try:
            parsed_data['talents'] = json.loads(talent.other_talents)
        except:
            parsed_data['talents'] = []
    
    if talent.previous_productions:
        try:
            parsed_data['productions'] = json.loads(talent.previous_productions)
        except:
            parsed_data['productions'] = []
    
    if talent.gallery_photos:
        try:
            parsed_data['gallery'] = json.loads(talent.gallery_photos)
        except:
            parsed_data['gallery'] = []
    
    # Récupérer les drapeaux des pays
    from app.models.location import Country
    country_flags = {}
    
    # Drapeau du pays d'origine
    if talent.country_of_origin:
        country_obj = Country.query.filter_by(name=talent.country_of_origin).first()
        if country_obj:
            country_flags['origin'] = country_obj.flag
    
    # Drapeau du pays de résidence
    if talent.country_of_residence:
        country_obj = Country.query.filter_by(name=talent.country_of_residence).first()
        if country_obj:
            country_flags['residence'] = country_obj.flag
    
    # Drapeau de la nationalité
    if talent.nationality:
        for nat in NATIONALITIES_WITH_FLAGS:
            if nat['nationality'] == talent.nationality:
                country_flags['nationality'] = nat['flag']
                break
    
    return render_template('cinema/profile_view.html',
                         talent=talent,
                         decrypted=decrypted_data,
                         parsed=parsed_data,
                         country_flags=country_flags)

@bp.route('/export/pdf/<code>')
def export_pdf(code):
    """Télécharger le profil CINEMA en PDF"""
    talent = CinemaTalent.query.filter_by(unique_code=code, is_active=True).first_or_404()
    
    pdf_bytes = ExportService.export_cinema_talent_card_pdf(talent)
    
    buffer = io.BytesIO(pdf_bytes)
    buffer.seek(0)
    
    filename = f'cinema_{talent.unique_code}_{datetime.now().strftime("%Y%m%d")}.pdf'
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

@bp.route('/delete/<int:talent_id>', methods=['POST'])
@login_required
def delete_talent(talent_id):
    """Supprimer un talent individuel"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403
    
    try:
        talent = CinemaTalent.query.get_or_404(talent_id)
        talent_name = f"{talent.first_name} {talent.last_name}"
        
        talent.is_active = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{talent_name} a été supprimé avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la suppression: {str(e)}'
        }), 500

@bp.route('/delete/bulk', methods=['POST'])
@login_required
def delete_talents_bulk():
    """Supprimer plusieurs talents en lot"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Accès non autorisé'}), 403
    
    try:
        data = request.get_json()
        talent_ids = data.get('talent_ids', [])
        
        if not talent_ids:
            return jsonify({'success': False, 'message': 'Aucun talent sélectionné'}), 400
        
        deleted_count = 0
        for talent_id in talent_ids:
            talent = CinemaTalent.query.get(talent_id)
            if talent:
                talent.is_active = False
                deleted_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{deleted_count} talent(s) supprimé(s) avec succès'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la suppression: {str(e)}'
        }), 500

@bp.route('/print/list')
@login_required
def print_talents_list():
    """Imprimer la liste des talents en format paysage PDF"""
    if not current_user.is_admin:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('cinema.talents'))
    
    talents_list = CinemaTalent.query.filter_by(is_active=True).order_by(CinemaTalent.first_name, CinemaTalent.last_name).all()
    
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.enums import TA_CENTER
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), 
                          rightMargin=0.5*cm, leftMargin=0.5*cm,
                          topMargin=0.6*cm, bottomMargin=0.6*cm)
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#6B46C1'),
        spaceAfter=15,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    title = Paragraph("Liste des Talents CINEMA - TalentsMaroc.com", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*cm))
    
    data = [['Nom complet', 'Âge / Genre', 'Document d\'identité', 'Téléphone', 'WhatsApp', 'Ethnicité', 'Type de talent', 'Observations']]
    
    for talent in talents_list:
        from app.utils.encryption import decrypt_sensitive_data
        
        full_name = f"{talent.first_name} {talent.last_name}"
        
        age_gender = ""
        if talent.age:
            age_gender += f"{talent.age} ans"
        if talent.gender_display:
            age_gender += f" / {talent.gender_display}" if age_gender else talent.gender_display
        
        id_document = ""
        if talent.id_document_type:
            id_type = "Passeport" if talent.id_document_type == 'passport' else "CIN"
            id_document = id_type
            if talent.id_document_number_encrypted:
                try:
                    id_number = decrypt_sensitive_data(talent.id_document_number_encrypted)
                    id_document += f"\n{id_number}"
                except:
                    pass
        
        phone = ""
        if talent.phone_encrypted:
            try:
                phone = decrypt_sensitive_data(talent.phone_encrypted)
            except:
                pass
        
        whatsapp = ""
        if talent.whatsapp_encrypted:
            try:
                whatsapp = decrypt_sensitive_data(talent.whatsapp_encrypted)
            except:
                pass
        
        ethnicity = ""
        if talent.ethnicities:
            try:
                ethnicities_list = json.loads(talent.ethnicities)
                ethnicity = ethnicities_list[0] if ethnicities_list else ""
                if len(ethnicities_list) > 1:
                    ethnicity += f" +{len(ethnicities_list)-1}"
            except:
                pass
        
        talent_type = ""
        if talent.talent_types:
            try:
                talent_types_list = json.loads(talent.talent_types)
                talent_type = talent_types_list[0] if talent_types_list else ""
                if len(talent_types_list) > 1:
                    talent_type += f" +{len(talent_types_list)-1}"
            except:
                pass
        
        data.append([
            full_name,
            age_gender or "-",
            id_document or "-",
            phone or "-",
            whatsapp or "-",
            ethnicity or "-",
            talent_type or "-",
            ""
        ])
    
    table = Table(data, colWidths=[3.8*cm, 2.6*cm, 3.2*cm, 2.8*cm, 2.8*cm, 2.8*cm, 4.5*cm, 5.5*cm])
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6B46C1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F5FF')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
    ]))
    
    elements.append(table)
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    elements.append(Spacer(1, 1*cm))
    footer_text = f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} - Total: {len(talents_list)} talent(s)"
    elements.append(Paragraph(footer_text, footer_style))
    
    doc.build(elements)
    
    buffer.seek(0)
    filename = f'liste_talents_cinema_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

# ============================================
# ROUTES POUR LA GESTION DES PROJETS
# ============================================

@bp.route('/projects')
@login_required
def projects():
    """Liste des projets de production en cours"""
    from app.models.project import Project
    projects_list = Project.query.filter_by(is_active=True).order_by(Project.created_at.desc()).all()
    return render_template('cinema/projects.html', projects=projects_list)

@bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
def add_project():
    """Créer un nouveau projet de production"""
    from app.models.project import Project
    
    if request.method == 'POST':
        try:
            project = Project()
            
            # Informations de base
            project.name = request.form.get('name')
            project.production_type = request.form.get('production_type')
            project.production_company_id = request.form.get('production_company_id') or None
            
            # Localisation
            project.origin_country = request.form.get('origin_country')
            project.shooting_locations = request.form.get('shooting_locations')
            
            # Dates
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            
            if start_date_str:
                project.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            if end_date_str:
                project.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            # Statut
            project.status = request.form.get('status', 'en_preparation')
            project.created_by = current_user.id
            
            db.session.add(project)
            db.session.commit()
            
            flash(f'✅ Projet "{project.name}" créé avec succès!', 'success')
            return redirect(url_for('cinema.project_detail', project_id=project.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Erreur lors de la création du projet: {str(e)}', 'error')
    
    # GET request - afficher le formulaire
    productions_list = Production.query.filter_by(is_active=True).order_by(Production.name).all()
    
    production_types = [
        'Film',
        'Série',
        'Court-métrage',
        'Documentaire',
        'Publicité',
        'Clip musical',
        'Téléfilm',
        'Web-série',
        'Autre'
    ]
    
    status_choices = [
        ('en_preparation', 'En préparation'),
        ('en_tournage', 'En tournage'),
        ('post_production', 'Post-production'),
        ('termine', 'Terminé')
    ]
    
    return render_template('cinema/project_form.html',
                         productions=productions_list,
                         production_types=production_types,
                         status_choices=status_choices,
                         nationalities=NATIONALITIES_WITH_FLAGS)

@bp.route('/projects/<int:project_id>')
@login_required
def project_detail(project_id):
    """Détails d'un projet avec la liste des talents assignés"""
    from app.models.project import Project, ProjectTalent
    
    project = Project.query.get_or_404(project_id)
    
    # Récupérer tous les talents assignés au projet
    project_talents = ProjectTalent.query.filter_by(project_id=project_id).order_by(ProjectTalent.assigned_at.desc()).all()
    
    # Récupérer tous les talents CINEMA disponibles pour l'ajout
    all_cinema_talents = CinemaTalent.query.filter_by(is_active=True).order_by(CinemaTalent.first_name, CinemaTalent.last_name).all()
    
    return render_template('cinema/project_detail.html',
                         project=project,
                         project_talents=project_talents,
                         all_cinema_talents=all_cinema_talents,
                         cinema_talent_types=CINEMA_TALENT_TYPES)

@bp.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """Modifier un projet existant"""
    from app.models.project import Project
    
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        try:
            # Informations de base
            project.name = request.form.get('name')
            project.production_type = request.form.get('production_type')
            project.production_company_id = request.form.get('production_company_id') or None
            
            # Localisation
            project.origin_country = request.form.get('origin_country')
            project.shooting_locations = request.form.get('shooting_locations')
            
            # Dates
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            
            if start_date_str:
                project.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            else:
                project.start_date = None
                
            if end_date_str:
                project.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            else:
                project.end_date = None
            
            # Statut
            project.status = request.form.get('status', 'en_preparation')
            
            db.session.commit()
            
            flash(f'✅ Projet "{project.name}" modifié avec succès!', 'success')
            return redirect(url_for('cinema.project_detail', project_id=project.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Erreur lors de la modification du projet: {str(e)}', 'error')
    
    # GET request - afficher le formulaire pré-rempli
    productions_list = Production.query.filter_by(is_active=True).order_by(Production.name).all()
    
    production_types = [
        'Film',
        'Série',
        'Court-métrage',
        'Documentaire',
        'Publicité',
        'Clip musical',
        'Téléfilm',
        'Web-série',
        'Autre'
    ]
    
    status_choices = [
        ('en_preparation', 'En préparation'),
        ('en_tournage', 'En tournage'),
        ('post_production', 'Post-production'),
        ('termine', 'Terminé')
    ]
    
    return render_template('cinema/project_form.html',
                         project=project,
                         productions=productions_list,
                         production_types=production_types,
                         status_choices=status_choices,
                         nationalities=NATIONALITIES_WITH_FLAGS)

@bp.route('/projects/<int:project_id>/assign-talent', methods=['POST'])
@login_required
def assign_talent_to_project(project_id):
    """Assigner un talent CINEMA à un projet"""
    from app.models.project import Project, ProjectTalent
    from app.utils.project_code_generator import generate_project_talent_code
    
    project = Project.query.get_or_404(project_id)
    
    try:
        cinema_talent_id = request.form.get('cinema_talent_id')
        talent_type = request.form.get('talent_type')
        role_description = request.form.get('role_description', '')
        
        if not cinema_talent_id or not talent_type:
            flash('❌ Veuillez sélectionner un talent et un type de talent', 'error')
            return redirect(url_for('cinema.project_detail', project_id=project_id))
        
        # Vérifier si ce talent est déjà assigné au projet
        existing = ProjectTalent.query.filter_by(
            project_id=project_id,
            cinema_talent_id=cinema_talent_id
        ).first()
        
        if existing:
            flash('❌ Ce talent est déjà assigné à ce projet', 'error')
            return redirect(url_for('cinema.project_detail', project_id=project_id))
        
        # Créer l'assignation
        project_talent = ProjectTalent()
        project_talent.project_id = project_id
        project_talent.cinema_talent_id = cinema_talent_id
        project_talent.talent_type = talent_type
        project_talent.role_description = role_description
        project_talent.project_code = generate_project_talent_code(project)
        project_talent.assigned_by = current_user.id
        
        db.session.add(project_talent)
        db.session.commit()
        
        flash(f'✅ Talent assigné avec succès! Code: {project_talent.project_code}', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Erreur lors de l\'assignation du talent: {str(e)}', 'error')
    
    return redirect(url_for('cinema.project_detail', project_id=project_id))

@bp.route('/projects/<int:project_id>/remove-talent/<int:project_talent_id>', methods=['POST'])
@login_required
def remove_talent_from_project(project_id, project_talent_id):
    """Retirer un talent d'un projet"""
    from app.models.project import ProjectTalent
    
    project_talent = ProjectTalent.query.get_or_404(project_talent_id)
    
    # Vérifier que le talent appartient bien à ce projet
    if project_talent.project_id != project_id:
        flash('❌ Erreur: talent non associé à ce projet', 'error')
        return redirect(url_for('cinema.project_detail', project_id=project_id))
    
    try:
        db.session.delete(project_talent)
        db.session.commit()
        flash('✅ Talent retiré du projet avec succès', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Erreur lors du retrait du talent: {str(e)}', 'error')
    
    return redirect(url_for('cinema.project_detail', project_id=project_id))

@bp.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    """Supprimer (soft delete) un projet"""
    from app.models.project import Project
    
    project = Project.query.get_or_404(project_id)
    
    try:
        project.is_active = False
        db.session.commit()
        flash(f'✅ Projet "{project.name}" supprimé avec succès', 'success')
        return redirect(url_for('cinema.projects'))
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Erreur lors de la suppression du projet: {str(e)}', 'error')
        return redirect(url_for('cinema.project_detail', project_id=project_id))

@bp.route('/projects/talent/<int:project_talent_id>/generate-badge')
@login_required
def generate_project_badge(project_talent_id):
    """Générer un badge pour un talent assigné à un projet - 4 badges A6 sur une page A4"""
    from app.models.project import ProjectTalent
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.pdfgen import canvas
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    import qrcode
    import os
    from PIL import Image as PILImage
    
    project_talent = ProjectTalent.query.get_or_404(project_talent_id)
    talent = project_talent.cinema_talent
    project = project_talent.project
    
    try:
        # Créer un buffer pour le PDF
        buffer = io.BytesIO()
        
        # Page A4
        c = canvas.Canvas(buffer, pagesize=A4)
        page_width, page_height = A4
        
        # Dimensions d'un badge A6 (10.5 x 14.8 cm)
        badge_width = 10.5 * cm
        badge_height = 14.8 * cm
        
        # Positions des 4 badges sur la page A4
        positions = [
            (0.5*cm, page_height - badge_height - 0.5*cm),  # Top left
            (page_width/2 + 0.25*cm, page_height - badge_height - 0.5*cm),  # Top right
            (0.5*cm, page_height - 2*badge_height - 1*cm),  # Bottom left
            (page_width/2 + 0.25*cm, page_height - 2*badge_height - 1*cm)  # Bottom right
        ]
        
        # Générer le QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        profile_url = f"https://talentsmaroc.com/cinema/profile/{talent.unique_code}"
        qr.add_data(profile_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_path = f"/tmp/qr_{project_talent.project_code}.png"
        qr_img.save(qr_path)
        
        # Logo path
        logo_path = os.path.join('app', 'static', 'img', 'logo.png')
        if not os.path.exists(logo_path):
            logo_path = os.path.join('static', 'img', 'logo.png')
        
        # Photo path
        photo_path = None
        if talent.profile_photo_filename:
            photo_path = os.path.join('app', 'static', 'uploads', 'photos', talent.profile_photo_filename)
            if not os.path.exists(photo_path):
                photo_path = os.path.join('static', 'uploads', 'photos', talent.profile_photo_filename)
                if not os.path.exists(photo_path):
                    photo_path = None
        
        # Dates du projet
        dates_text = "Dates: Non spécifiées"
        if project.start_date and project.end_date:
            start = project.start_date.strftime('%d/%m/%Y')
            end = project.end_date.strftime('%d/%m/%Y')
            dates_text = f"{start} - {end}"
        elif project.start_date:
            dates_text = f"Début: {project.start_date.strftime('%d/%m/%Y')}"
        
        # Dessiner les 4 badges
        for x, y in positions:
            # Bordure pointillée pour découper
            c.setDash([3, 3], 0)
            c.setStrokeColor(colors.grey)
            c.rect(x, y, badge_width, badge_height)
            c.setDash([], 0)
            
            # Marges internes
            margin = 0.4 * cm
            content_x = x + margin
            content_y = y + badge_height - margin
            content_width = badge_width - 2 * margin
            
            # 1. Logo en haut
            if os.path.exists(logo_path):
                c.drawImage(logo_path, content_x + content_width/2 - 1.5*cm, content_y - 1.8*cm, 
                           width=3*cm, height=1.5*cm, preserveAspectRatio=True, mask='auto')
                content_y -= 2*cm
            else:
                c.setFont("Helvetica-Bold", 10)
                c.setFillColor(colors.HexColor('#8B5CF6'))
                c.drawCentredString(content_x + content_width/2, content_y - 0.5*cm, "TALENTSMAROC.COM")
                content_y -= 1*cm
            
            # 2. Nom de la boîte de production
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.HexColor('#4F46E5'))
            production_name = project.production_company.name if project.production_company else "Production"
            c.drawCentredString(content_x + content_width/2, content_y - 0.4*cm, production_name[:35])
            content_y -= 0.7*cm
            
            # 3. Dates de début et fin
            c.setFont("Helvetica", 7)
            c.setFillColor(colors.HexColor('#6B7280'))
            c.drawCentredString(content_x + content_width/2, content_y - 0.3*cm, dates_text)
            content_y -= 0.8*cm
            
            # 4. Photo du talent cinema
            if photo_path and os.path.exists(photo_path):
                photo_size = 3*cm
                c.drawImage(photo_path, content_x + content_width/2 - photo_size/2, content_y - photo_size - 0.2*cm,
                           width=photo_size, height=photo_size, preserveAspectRatio=True, mask='auto')
                content_y -= photo_size + 0.4*cm
            else:
                c.setFont("Helvetica", 8)
                c.setFillColor(colors.grey)
                c.drawCentredString(content_x + content_width/2, content_y - 1.5*cm, "[Photo non disponible]")
                content_y -= 2*cm
            
            # 5. Code unique projet
            c.setFont("Helvetica-Bold", 11)
            c.setFillColor(colors.HexColor('#8B5CF6'))
            c.drawCentredString(content_x + content_width/2, content_y - 0.4*cm, project_talent.project_code)
            content_y -= 0.7*cm
            
            # 6. Nom du projet
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(colors.black)
            project_name = project.name[:30] + "..." if len(project.name) > 30 else project.name
            c.drawCentredString(content_x + content_width/2, content_y - 0.4*cm, project_name)
            content_y -= 0.7*cm
            
            # 7. Rôle
            c.setFont("Helvetica", 8)
            c.setFillColor(colors.HexColor('#4B5563'))
            role_text = f"Rôle: {project_talent.talent_type}"
            c.drawCentredString(content_x + content_width/2, content_y - 0.3*cm, role_text)
            content_y -= 0.6*cm
            
            # 8. Type de production
            production_type = f"Type: {project.production_type}"
            c.drawCentredString(content_x + content_width/2, content_y - 0.3*cm, production_type)
            content_y -= 0.7*cm
            
            # 9. QR code
            qr_size = 2.5*cm
            c.drawImage(qr_path, content_x + content_width/2 - qr_size/2, content_y - qr_size - 0.2*cm,
                       width=qr_size, height=qr_size)
            content_y -= qr_size + 0.4*cm
            
            # Footer avec code de la plateforme
            c.setFont("Helvetica", 6)
            c.setFillColor(colors.grey)
            c.drawCentredString(content_x + content_width/2, y + 0.3*cm, 
                              f"TalentsMaroc.com | {talent.unique_code} | {datetime.now().strftime('%d/%m/%Y')}")
        
        # Finaliser le PDF
        c.save()
        
        # Nettoyer les fichiers temporaires
        if os.path.exists(qr_path):
            os.remove(qr_path)
        
        # Marquer le badge comme généré
        project_talent.badge_generated = True
        db.session.commit()
        
        buffer.seek(0)
        filename = f'badge_{project_talent.project_code}_x4.pdf'
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        flash(f'❌ Erreur lors de la génération du badge: {str(e)}', 'error')
        return redirect(url_for('cinema.project_detail', project_id=project_talent.project_id))
