from flask import Blueprint, jsonify, request
from app import db
from app.models.talent import Talent
from app.models.location import Country, City

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/countries')
def get_countries():
    countries = Country.query.order_by(Country.name).all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'code': c.code
    } for c in countries])

@bp.route('/cities')
def get_cities():
    cities = City.query.order_by(City.name).all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'code': c.code
    } for c in cities])

@bp.route('/talents')
def get_talents():
    talents = Talent.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'emoji': t.emoji,
        'category': t.category
    } for t in talents])
