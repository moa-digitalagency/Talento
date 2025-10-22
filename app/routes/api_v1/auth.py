"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from flask import request, jsonify, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app.routes.api_v1 import bp
from app.models.user import User
from app import db
from datetime import datetime
import json

@bp.route('/auth/login', methods=['POST'])
def api_login():
    """
    API Login endpoint
    ---
    POST /api/v1/auth/login
    
    Request Body:
    {
        "identifier": "email@example.com or UNIQUE_CODE",
        "password": "password123"
    }
    
    Response:
    {
        "success": true,
        "message": "Login successful",
        "user": {
            "id": 1,
            "email": "user@example.com",
            "unique_code": "MARAB0001M",
            "first_name": "John",
            "last_name": "Doe",
            "is_admin": false
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        identifier = data.get('identifier')
        password = data.get('password')
        
        if not identifier or not password:
            return jsonify({
                'success': False,
                'error': 'Missing identifier or password'
            }), 400
        
        # Find user by email or unique code
        user = User.query.filter_by(email=identifier).first()
        if not user:
            user = User.query.filter_by(unique_code=identifier).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'unique_code': user.unique_code,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_admin': user.is_admin
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
            
    except Exception as e:
        current_app.logger.error(f'Login API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@bp.route('/auth/logout', methods=['POST'])
@login_required
def api_logout():
    """
    API Logout endpoint
    ---
    POST /api/v1/auth/logout
    
    Response:
    {
        "success": true,
        "message": "Logout successful"
    }
    """
    try:
        logout_user()
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        }), 200
    except Exception as e:
        current_app.logger.error(f'Logout API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@bp.route('/auth/me', methods=['GET'])
@login_required
def api_current_user():
    """
    Get current authenticated user
    ---
    GET /api/v1/auth/me
    
    Response:
    {
        "success": true,
        "user": {
            "id": 1,
            "email": "user@example.com",
            "unique_code": "MARAB0001M",
            "first_name": "John",
            "last_name": "Doe",
            "is_admin": false,
            "created_at": "2025-01-01T00:00:00"
        }
    }
    """
    try:
        return jsonify({
            'success': True,
            'user': {
                'id': current_user.id,
                'email': current_user.email,
                'unique_code': current_user.unique_code,
                'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                'gender': current_user.gender,
                'is_admin': current_user.is_admin,
                'account_active': current_user.account_active,
                'created_at': current_user.created_at.isoformat() if current_user.created_at else None
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f'Current user API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
