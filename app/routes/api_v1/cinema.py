from flask import request, jsonify, current_app
from flask_login import login_required, current_user
from app.routes.api_v1 import bp
from app.models.cinema_talent import CinemaTalent
from app.models.location import Country
from app import db
from functools import wraps
import json

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({
                'success': False,
                'error': 'Admin access required'
            }), 403
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/cinema/talents', methods=['GET'])
@login_required
def get_cinema_talents():
    """
    Get all CINEMA talents with optional filters
    ---
    GET /api/v1/cinema/talents?search=name&gender=M&page=1&limit=20
    
    Response:
    {
        "success": true,
        "total": 50,
        "page": 1,
        "limit": 20,
        "talents": [...]
    }
    """
    try:
        # Query parameters
        search = request.args.get('search', '').strip()
        gender = request.args.get('gender')
        country_origin_id = request.args.get('country_origin_id')
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 20)), 100)
        
        # Base query
        query = CinemaTalent.query.filter(CinemaTalent.is_active == True)
        
        # Filters
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                db.or_(
                    CinemaTalent.first_name.ilike(search_pattern),
                    CinemaTalent.last_name.ilike(search_pattern),
                    CinemaTalent.email_encrypted.ilike(search_pattern)
                )
            )
        
        if gender:
            query = query.filter(CinemaTalent.gender == gender)
        
        if country_origin_id:
            query = query.filter(CinemaTalent.country_origin_id == int(country_origin_id))
        
        # Pagination
        total = query.count()
        talents = query.order_by(CinemaTalent.created_at.desc()).paginate(
            page=page, per_page=limit, error_out=False
        )
        
        talents_data = []
        for talent in talents.items:
            talent_dict = {
                'id': talent.id,
                'first_name': talent.first_name,
                'last_name': talent.last_name,
                'gender': talent.gender,
                'date_of_birth': talent.date_of_birth.isoformat() if talent.date_of_birth else None,
                'country_origin': talent.country_origin.name if talent.country_origin else None,
                'country_residence': talent.country_residence.name if talent.country_residence else None,
                'photo_profile_url': talent.photo_profile_url,
                'is_active': talent.is_active,
                'created_at': talent.created_at.isoformat() if talent.created_at else None
            }
            
            # Add encrypted fields (decrypted)
            if talent.email:
                talent_dict['email'] = talent.email
            
            # Add JSON fields
            if talent.ethnicities:
                try:
                    talent_dict['ethnicities'] = json.loads(talent.ethnicities)
                except:
                    talent_dict['ethnicities'] = []
            
            if talent.languages_spoken:
                try:
                    talent_dict['languages_spoken'] = json.loads(talent.languages_spoken)
                except:
                    talent_dict['languages_spoken'] = []
            
            if talent.other_talents:
                try:
                    talent_dict['other_talents'] = json.loads(talent.other_talents)
                except:
                    talent_dict['other_talents'] = []
            
            talents_data.append(talent_dict)
        
        return jsonify({
            'success': True,
            'total': total,
            'page': page,
            'limit': limit,
            'talents': talents_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get cinema talents API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@bp.route('/cinema/talents/<int:talent_id>', methods=['GET'])
@login_required
def get_cinema_talent(talent_id):
    """
    Get CINEMA talent details by ID
    ---
    GET /api/v1/cinema/talents/123
    
    Response:
    {
        "success": true,
        "talent": {...}
    }
    """
    try:
        talent = CinemaTalent.query.get_or_404(talent_id)
        
        talent_dict = {
            'id': talent.id,
            'first_name': talent.first_name,
            'last_name': talent.last_name,
            'gender': talent.gender,
            'date_of_birth': talent.date_of_birth.isoformat() if talent.date_of_birth else None,
            'id_document_type': talent.id_document_type,
            'country_origin': {'id': talent.country_origin.id, 'name': talent.country_origin.name, 'flag': talent.country_origin.flag} if talent.country_origin else None,
            'nationality_country': {'id': talent.nationality_country.id, 'name': talent.nationality_country.name, 'flag': talent.nationality_country.flag} if talent.nationality_country else None,
            'country_residence': {'id': talent.country_residence.id, 'name': talent.country_residence.name, 'flag': talent.country_residence.flag} if talent.country_residence else None,
            'city_residence': talent.city_residence,
            'eye_color': talent.eye_color,
            'hair_color': talent.hair_color,
            'hair_type': talent.hair_type,
            'height': talent.height,
            'skin_tone': talent.skin_tone,
            'build': talent.build,
            'photo_profile_url': talent.photo_profile_url,
            'photo_id_url': talent.photo_id_url,
            'photo_gallery_1_url': talent.photo_gallery_1_url,
            'photo_gallery_2_url': talent.photo_gallery_2_url,
            'photo_gallery_3_url': talent.photo_gallery_3_url,
            'is_active': talent.is_active,
            'created_at': talent.created_at.isoformat() if talent.created_at else None
        }
        
        # Decrypted fields
        if talent.email:
            talent_dict['email'] = talent.email
        if talent.phone:
            talent_dict['phone'] = talent.phone
        if talent.facebook:
            talent_dict['facebook'] = talent.facebook
        if talent.instagram:
            talent_dict['instagram'] = talent.instagram
        if talent.tiktok:
            talent_dict['tiktok'] = talent.tiktok
        if talent.snapchat:
            talent_dict['snapchat'] = talent.snapchat
        if talent.youtube:
            talent_dict['youtube'] = talent.youtube
        if talent.twitter:
            talent_dict['twitter'] = talent.twitter
        if talent.linkedin:
            talent_dict['linkedin'] = talent.linkedin
        
        # JSON fields
        if talent.ethnicities:
            try:
                talent_dict['ethnicities'] = json.loads(talent.ethnicities)
            except:
                talent_dict['ethnicities'] = []
        
        if talent.languages_spoken:
            try:
                talent_dict['languages_spoken'] = json.loads(talent.languages_spoken)
            except:
                talent_dict['languages_spoken'] = []
        
        if talent.other_talents:
            try:
                talent_dict['other_talents'] = json.loads(talent.other_talents)
            except:
                talent_dict['other_talents'] = []
        
        if talent.previous_productions:
            try:
                talent_dict['previous_productions'] = json.loads(talent.previous_productions)
            except:
                talent_dict['previous_productions'] = []
        
        return jsonify({
            'success': True,
            'talent': talent_dict
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get cinema talent API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Talent not found'
        }), 404


@bp.route('/cinema/stats', methods=['GET'])
@login_required
def get_cinema_stats():
    """
    Get CINEMA module statistics
    ---
    GET /api/v1/cinema/stats
    
    Response:
    {
        "success": true,
        "stats": {
            "total_talents": 150,
            "active_talents": 145,
            "by_gender": {...},
            "by_country": {...}
        }
    }
    """
    try:
        total_talents = CinemaTalent.query.count()
        active_talents = CinemaTalent.query.filter_by(is_active=True).count()
        
        # By gender
        by_gender = {}
        for gender in ['M', 'F', 'N']:
            count = CinemaTalent.query.filter_by(gender=gender, is_active=True).count()
            if count > 0:
                by_gender[gender] = count
        
        # By country of origin
        by_country = {}
        countries = db.session.query(
            Country.name, db.func.count(CinemaTalent.id)
        ).join(
            CinemaTalent, CinemaTalent.country_origin_id == Country.id
        ).filter(
            CinemaTalent.is_active == True
        ).group_by(Country.name).all()
        
        for country_name, count in countries:
            by_country[country_name] = count
        
        return jsonify({
            'success': True,
            'stats': {
                'total_talents': total_talents,
                'active_talents': active_talents,
                'inactive_talents': total_talents - active_talents,
                'by_gender': by_gender,
                'by_country': by_country
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get cinema stats API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
