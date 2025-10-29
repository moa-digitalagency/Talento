"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from flask import request, jsonify, current_app
from flask_login import login_required, current_user
from app.routes.api_v1 import bp
from app.models.user import User
from app.models.talent import UserTalent, Talent
from app.models.location import Country, City
from app import db
from functools import wraps

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


@bp.route('/stats/overview', methods=['GET'])
@login_required
@admin_required
def get_stats_overview():
    """
    Get platform overview statistics
    ---
    GET /api/v1/stats/overview
    
    Response:
    {
        "success": true,
        "stats": {
            "total_users": 150,
            "active_users": 145,
            "by_gender": {...},
            "by_country": {...},
            "by_availability": {...},
            "by_talent": {...}
        }
    }
    """
    try:
        total_users = User.query.filter_by(is_admin=False).count()
        active_users = User.query.filter_by(is_admin=False, account_active=True).count()
        
        # By gender
        by_gender = {}
        for gender in ['M', 'F', 'N']:
            count = User.query.filter_by(gender=gender, is_admin=False, account_active=True).count()
            if count > 0:
                by_gender[gender] = count
        
        # By availability
        by_availability = {}
        availabilities = db.session.query(
            User.availability, db.func.count(User.id)
        ).filter(
            User.is_admin == False,
            User.account_active == True,
            User.availability.isnot(None)
        ).group_by(User.availability).all()
        
        for availability, count in availabilities:
            by_availability[availability] = count
        
        # By country
        by_country = {}
        countries = db.session.query(
            Country.name, db.func.count(User.id)
        ).join(
            User, User.country_id == Country.id
        ).filter(
            User.is_admin == False,
            User.account_active == True
        ).group_by(Country.name).all()
        
        for country_name, count in countries:
            by_country[country_name] = count
        
        # By talent (top 10)
        by_talent = {}
        talents = db.session.query(
            Talent.name, Talent.emoji, db.func.count(UserTalent.id)
        ).join(
            UserTalent, UserTalent.talent_id == Talent.id
        ).join(
            User, User.id == UserTalent.user_id
        ).filter(
            User.is_admin == False,
            User.account_active == True
        ).group_by(Talent.id, Talent.name, Talent.emoji).order_by(
            db.func.count(UserTalent.id).desc()
        ).limit(10).all()
        
        by_talent_list = []
        for talent_name, emoji, count in talents:
            by_talent_list.append({
                'name': talent_name,
                'emoji': emoji,
                'count': count
            })
        
        return jsonify({
            'success': True,
            'stats': {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': total_users - active_users,
                'by_gender': by_gender,
                'by_availability': by_availability,
                'by_country': by_country,
                'top_talents': by_talent_list
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get stats overview API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@bp.route('/stats/talents', methods=['GET'])
@login_required
@admin_required
def get_stats_talents():
    """
    Get talent category statistics
    ---
    GET /api/v1/stats/talents
    
    Response:
    {
        "success": true,
        "stats": {
            "by_category": {...},
            "total_talents": 73,
            "total_users_with_talents": 120
        }
    }
    """
    try:
        # Group by category
        by_category = {}
        categories = db.session.query(
            Talent.category, db.func.count(db.distinct(UserTalent.user_id))
        ).join(
            UserTalent, UserTalent.talent_id == Talent.id
        ).join(
            User, User.id == UserTalent.user_id
        ).filter(
            User.is_admin == False,
            User.account_active == True,
            Talent.is_active == True
        ).group_by(Talent.category).all()
        
        for category, count in categories:
            by_category[category] = count
        
        total_talents = Talent.query.filter_by(is_active=True).count()
        total_users_with_talents = db.session.query(
            db.func.count(db.distinct(UserTalent.user_id))
        ).join(
            User, User.id == UserTalent.user_id
        ).filter(
            User.is_admin == False,
            User.account_active == True
        ).scalar()
        
        return jsonify({
            'success': True,
            'stats': {
                'by_category': by_category,
                'total_talents': total_talents,
                'total_users_with_talents': total_users_with_talents
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get stats talents API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
