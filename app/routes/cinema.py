from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_file
from flask_login import login_required, current_user
from app import db
from app.models.cinema_talent import CinemaTalent
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
    
    # Récupérer les valeurs uniques des caractéristiques des talents existants
    ethnicities_set = set()
    eye_colors_set = set()
    hair_colors_set = set()
    skin_tones_set = set()
    
    for talent in talents_list:
        if talent.ethnicities:
            try:
                ethnicities = json.loads(talent.ethnicities)
                ethnicities_set.update(ethnicities)
            except:
                pass
        if talent.eye_color:
            eye_colors_set.add(talent.eye_color)
        if talent.hair_color:
            hair_colors_set.add(talent.hair_color)
        if talent.skin_tone:
            skin_tones_set.add(talent.skin_tone)
    
    return render_template('cinema/talents.html', 
                         talents=talents_list,
                         countries=countries,
                         languages=LANGUAGES_CINEMA,
                         cinema_talent_types=CINEMA_TALENT_TYPES,
                         eye_colors=sorted(eye_colors_set) if eye_colors_set else EYE_COLORS,
                         hair_colors=sorted(hair_colors_set) if hair_colors_set else HAIR_COLORS,
                         skin_tones=sorted(skin_tones_set) if skin_tones_set else SKIN_TONES)

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
                          rightMargin=0.8*cm, leftMargin=0.8*cm,
                          topMargin=1*cm, bottomMargin=1*cm)
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#6B46C1'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    title = Paragraph("Liste des Talents CINEMA - TalentsMaroc.com", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.5*cm))
    
    data = [['Nom complet', 'Âge / Genre', 'Document d\'identité', 'Ethnicité', 'Type de talent']]
    
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
            ethnicity or "-",
            talent_type or "-"
        ])
    
    table = Table(data, colWidths=[5*cm, 3.5*cm, 4*cm, 4*cm, 6*cm])
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6B46C1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E0E0E0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F5FF')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
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
