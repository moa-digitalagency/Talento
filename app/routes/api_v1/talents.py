"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from flask import request, jsonify, current_app
from flask_login import login_required
from app.routes.api_v1 import bp
from app.models.talent import Talent
from app.models.location import Country, City
from app import db


@bp.route('/talents', methods=['GET'])
def get_talents():
    """
    Get all available talents
    ---
    GET /api/v1/talents
    
    Response:
    {
        "success": true,
        "talents": [
            {
                "id": 1,
                "name": "Développeur Web",
                "emoji": "💻",
                "category": "Technologie",
                "is_active": true
            }
        ]
    }
    """
    try:
        talents = Talent.query.filter_by(is_active=True).order_by(Talent.category, Talent.name).all()
        
        talents_data = []
        for talent in talents:
            talents_data.append({
                'id': talent.id,
                'name': talent.name,
                'emoji': talent.emoji,
                'category': talent.category,
                'is_active': talent.is_active
            })
        
        return jsonify({
            'success': True,
            'total': len(talents_data),
            'talents': talents_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get talents API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@bp.route('/countries', methods=['GET'])
def get_countries():
    """
    Get all countries
    ---
    GET /api/v1/countries
    
    Response:
    {
        "success": true,
        "countries": [
            {
                "id": 1,
                "name": "Maroc",
                "code": "MA",
                "flag": "🇲🇦"
            }
        ]
    }
    """
    try:
        countries = Country.query.order_by(Country.name).all()
        
        countries_data = []
        for country in countries:
            countries_data.append({
                'id': country.id,
                'name': country.name,
                'code': country.code,
                'flag': country.flag
            })
        
        return jsonify({
            'success': True,
            'total': len(countries_data),
            'countries': countries_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get countries API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@bp.route('/cities', methods=['GET'])
def get_cities():
    """
    Get all cities, optionally filtered by country
    ---
    GET /api/v1/cities?country_id=1
    
    Response:
    {
        "success": true,
        "cities": [
            {
                "id": 1,
                "name": "Rabat",
                "code": "RAB",
                "country_id": 1
            }
        ]
    }
    """
    try:
        country_id = request.args.get('country_id')
        
        query = City.query
        if country_id:
            query = query.filter_by(country_id=int(country_id))
        
        cities = query.order_by(City.name).all()
        
        cities_data = []
        for city in cities:
            cities_data.append({
                'id': city.id,
                'name': city.name,
                'code': city.code,
                'country_id': city.country_id
            })
        
        return jsonify({
            'success': True,
            'total': len(cities_data),
            'cities': cities_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Get cities API error: {e}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
