from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from app.models.user import User
from app.models.talent import Talent, UserTalent
from app.models.location import Country, City
from app import db
from sqlalchemy import func, desc, or_
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    # Si l'utilisateur est admin, afficher la vue admin avec filtres
    if current_user.is_admin:
        return admin_dashboard()
    else:
        # Sinon, afficher le profil de l'utilisateur
        return render_template('profile/dashboard.html', user=current_user)

def admin_dashboard():
    """Dashboard admin avec statistiques et filtres"""
    search_query = request.args.get('search', '').strip()
    search_code = request.args.get('search_code', '').strip()
    
    talent_filter = request.args.getlist('talent')
    country_filter = request.args.get('country')
    city_filter = request.args.get('city')
    gender_filter = request.args.get('gender')
    availability_filter = request.args.get('availability')
    has_cv = request.args.get('has_cv')
    has_portfolio = request.args.get('has_portfolio')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    # Base query
    query = User.query.filter(User.is_admin == False)
    
    # Filtres de recherche
    if search_query:
        search_pattern = f'%{search_query}%'
        query = query.filter(
            or_(
                User.first_name.ilike(search_pattern),
                User.last_name.ilike(search_pattern),
                User.email.ilike(search_pattern),
                User.unique_code.ilike(search_pattern)
            )
        )
    
    if search_code:
        code_clean = search_code.replace('-', '').upper()
        query = query.filter(User.unique_code.ilike(f'%{code_clean}%'))
    
    if talent_filter:
        for talent_id in talent_filter:
            query = query.join(User.talents).filter(UserTalent.talent_id == int(talent_id))
    
    if country_filter:
        query = query.filter(User.country_id == int(country_filter))
    
    if city_filter:
        query = query.filter(User.city_id == int(city_filter))
    
    if gender_filter:
        query = query.filter(User.gender == gender_filter)
    
    if availability_filter:
        query = query.filter(User.availability == availability_filter)
    
    if has_cv == 'yes':
        query = query.filter(User.cv_filename.isnot(None))
    elif has_cv == 'no':
        query = query.filter(User.cv_filename.is_(None))
    
    if has_portfolio == 'yes':
        query = query.filter(User.portfolio_url.isnot(None))
    elif has_portfolio == 'no':
        query = query.filter(User.portfolio_url.is_(None))
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(User.created_at >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            query = query.filter(User.created_at <= date_to_obj)
        except ValueError:
            pass
    
    users = query.order_by(User.created_at.desc()).all()
    
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
    
    # Données pour les filtres
    all_talents = Talent.query.order_by(Talent.category, Talent.name).all()
    all_countries = Country.query.order_by(Country.name).all()
    all_cities = City.query.order_by(City.name).all()
    
    stats = {
        'total_users': total_users,
        'with_cv': User.query.filter(User.cv_filename.isnot(None)).count(),
        'with_portfolio': User.query.filter(User.portfolio_url.isnot(None)).count(),
        'filtered_count': len(users)
    }
    
    return render_template('index.html',
                         users=users,
                         talents=all_talents,
                         countries=all_countries,
                         cities=all_cities,
                         stats=stats,
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

@bp.route('/about')
def about():
    return render_template('about.html')
