"""
TalentsMaroc.com
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


@bp.route('/users', methods=['GET'])
@login_required
@admin_required
def get_users():
    """
    Get all users with optional filters
    ---
    GET /api/v1/users?search=name&country_id=1&city_id=5&gender=M&page=1&limit=20
    
    Response:
    {
        "success": true,
        "total": 150,
        "page": 1,
        "limit": 20,
        "users": [...]
    }
    """
    try:
        # Query parameters
        search = request.args.get('search', '').strip()
        country_id = request.args.get('country_id')
        city_id = request.args.get('city_id')
        gender = request.args.get('gender')
        availability = request.args.get('availability')
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 20)), 100)
        
        # Base query
        query = User.query.filter(User.is_admin == False)
        
        # Filters
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                db.or_(
                    User.first_name.ilike(search_pattern),
                    User.last_name.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                    User.unique_code.ilike(search_pattern)
                )
            )
        
        if country_id:
            query = query.filter(User.country_id == int(country_id))
        
        if city_id:
            query = query.filter(User.city_id == int(city_id))
        
        if gender:
            query = query.filter(User.gender == gender)
        
        if availability:
            query = query.filter(User.availability == availability)
        
        # Pagination
        total = query.count()
        users = query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=limit, error_out=False
        )
        
        users_data = []
        for user in users.items:
            user_dict = {
                'id': user.id,
                'unique_code': user.unique_code,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'gender': user.gender,
                'availability': user.availability,
                'country': user.country.name if user.country else None,
                'city': user.city.name if user.city else None,
                'account_active': user.account_active,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'talents': [{'id': ut.talent.id, 'name': ut.talent.name, 'emoji': ut.talent.emoji} 
                           for ut in user.talents]
            }
            users_data.append(user_dict)
        
        return jsonify({
            'success': True,
            'total': total,
            'page': page,
            'limit': limit,
            'users': users_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get users API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """
    Get user details by ID
    ---
    GET /api/v1/users/123
    
    Response:
    {
        "success": true,
        "user": {...}
    }
    """
    try:
        user = User.query.get_or_404(user_id)
        
        # Check permissions
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'error': 'Access denied'
            }), 403
        
        user_dict = {
            'id': user.id,
            'unique_code': user.unique_code,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'gender': user.gender,
            'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
            'bio': user.bio,
            'availability': user.availability,
            'work_mode': user.work_mode,
            'rate_range': user.rate_range,
            'years_experience': user.years_experience,
            'country': {'id': user.country.id, 'name': user.country.name} if user.country else None,
            'city': {'id': user.city.id, 'name': user.city.name} if user.city else None,
            'portfolio_url': user.portfolio_url,
            'linkedin': user.linkedin,
            'instagram': user.instagram,
            'twitter': user.twitter,
            'facebook': user.facebook,
            'github': user.github,
            'account_active': user.account_active,
            'photo_url': user.photo_url,
            'cv_url': user.cv_url,
            'qr_code_url': user.qr_code_url,
            'profile_score': user.profile_score,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'talents': [{'id': ut.talent.id, 'name': ut.talent.name, 'emoji': ut.talent.emoji} 
                       for ut in user.talents]
        }
        
        return jsonify({
            'success': True,
            'user': user_dict
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get user API error: {e}')
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404


@bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    """
    Delete a user
    ---
    DELETE /api/v1/users/123
    
    Response:
    {
        "success": true,
        "message": "User deleted successfully"
    }
    """
    try:
        user = User.query.get_or_404(user_id)
        
        if user.is_admin:
            return jsonify({
                'success': False,
                'error': 'Cannot delete admin account'
            }), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Delete user API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@bp.route('/users/<int:user_id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_user_active(user_id):
    """
    Activate/Deactivate a user account
    ---
    POST /api/v1/users/123/toggle-active
    
    Response:
    {
        "success": true,
        "active": true,
        "message": "Account activated"
    }
    """
    try:
        user = User.query.get_or_404(user_id)
        user.account_active = not user.account_active
        db.session.commit()
        
        return jsonify({
            'success': True,
            'active': user.account_active,
            'message': f"Account {'activated' if user.account_active else 'deactivated'}"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Toggle user active API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
