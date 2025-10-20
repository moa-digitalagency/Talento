from flask import Blueprint, redirect, url_for, render_template
from app.models.user import User
from app.models.talent import Talent, UserTalent
from app.models.location import Country, City
from app import db
from sqlalchemy import func, desc

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Statistiques générales
    total_users = User.query.filter_by(account_active=True, is_admin=False).count()
    total_talents_unique = Talent.query.count()
    total_countries = Country.query.count()
    total_cities = City.query.count()
    
    # Utilisateurs récents (derniers 6)
    recent_users = User.query.filter_by(account_active=True, is_admin=False).order_by(desc(User.created_at)).limit(6).all()
    
    # Statistiques par disponibilité
    available_users = User.query.filter_by(availability='available', account_active=True).count()
    partially_available_users = User.query.filter_by(availability='partially_available', account_active=True).count()
    
    # Top talents les plus utilisés (top 10)
    top_talents = db.session.query(
        Talent.name,
        Talent.emoji,
        Talent.category,
        func.count(UserTalent.talent_id).label('count')
    ).join(UserTalent).group_by(Talent.id, Talent.name, Talent.emoji, Talent.category).order_by(desc('count')).limit(10).all()
    
    # Statistiques par catégorie
    category_stats = db.session.query(
        Talent.category,
        func.count(func.distinct(UserTalent.user_id)).label('user_count')
    ).join(UserTalent).group_by(Talent.category).all()
    
    # Statistiques par mode de travail
    work_mode_stats = db.session.query(
        User.work_mode,
        func.count(User.id).label('count')
    ).filter(User.account_active == True, User.work_mode != None).group_by(User.work_mode).all()
    
    # Top 5 villes avec le plus de talents
    top_cities = db.session.query(
        City.name,
        func.count(User.id).label('user_count')
    ).join(User).filter(User.account_active == True).group_by(City.id, City.name).order_by(desc('user_count')).limit(5).all()
    
    return render_template('index.html',
                         total_users=total_users,
                         total_talents_unique=total_talents_unique,
                         total_countries=total_countries,
                         total_cities=total_cities,
                         recent_users=recent_users,
                         available_users=available_users,
                         partially_available_users=partially_available_users,
                         top_talents=top_talents,
                         category_stats=category_stats,
                         work_mode_stats=work_mode_stats,
                         top_cities=top_cities)
