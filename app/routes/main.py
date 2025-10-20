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
    work_mode_filter = request.args.get('work_mode')
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
    
    if work_mode_filter:
        query = query.filter(User.work_mode == work_mode_filter)
    
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
    
    # Statistiques générales basées sur les utilisateurs actifs
    total_users = User.query.filter_by(account_active=True, is_admin=False).count()
    
    # Nombre de compétences sélectionnées par les talents (pas le total disponible)
    total_talents_selected = db.session.query(func.count(func.distinct(UserTalent.talent_id))).filter(
        UserTalent.user_id.in_(
            db.session.query(User.id).filter_by(account_active=True, is_admin=False)
        )
    ).scalar() or 0
    
    # Nombre de villes où il y a des utilisateurs inscrits
    total_cities_with_users = db.session.query(func.count(func.distinct(User.city_id))).filter(
        User.account_active == True,
        User.is_admin == False,
        User.city_id.isnot(None)
    ).scalar() or 0
    
    # Nombre de pays où il y a des utilisateurs inscrits
    total_countries_with_users = db.session.query(func.count(func.distinct(User.country_id))).filter(
        User.account_active == True,
        User.is_admin == False,
        User.country_id.isnot(None)
    ).scalar() or 0
    
    # Utilisateurs récents (derniers 6)
    recent_users = User.query.filter_by(account_active=True, is_admin=False).order_by(desc(User.created_at)).limit(6).all()
    
    # Top 10 compétences les plus sélectionnées par les utilisateurs
    top_talents = db.session.query(
        Talent.name,
        Talent.emoji,
        Talent.category,
        func.count(UserTalent.talent_id).label('count')
    ).join(UserTalent).join(User).filter(
        User.account_active == True,
        User.is_admin == False
    ).group_by(Talent.id, Talent.name, Talent.emoji, Talent.category).order_by(desc('count')).limit(10).all()
    
    # Top 10 villes marocaines avec le plus de talents
    top_morocco_cities = db.session.query(
        City.name,
        func.count(User.id).label('user_count')
    ).join(User).join(Country).filter(
        User.account_active == True,
        User.is_admin == False,
        Country.code == 'MA'
    ).group_by(City.id, City.name).order_by(desc('user_count')).limit(10).all()
    
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
                         total_talents_selected=total_talents_selected,
                         total_countries_with_users=total_countries_with_users,
                         total_cities_with_users=total_cities_with_users,
                         recent_users=recent_users,
                         top_talents=top_talents,
                         top_morocco_cities=top_morocco_cities)

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/talents')
@login_required
def talents():
    """Page de recherche et visualisation des talents"""
    search_query = request.args.get('search', '').strip()
    talent_search = request.args.get('talent_search', '').strip()
    availability_filter = request.args.get('availability')
    work_mode_filter = request.args.get('work_mode')
    city_filter = request.args.get('city')
    
    # Obtenir uniquement les talents qui ont au moins un utilisateur
    talents_with_users = db.session.query(
        Talent.id,
        Talent.name,
        Talent.emoji,
        Talent.category,
        func.count(UserTalent.user_id).label('user_count')
    ).join(UserTalent).join(User).filter(
        User.account_active == True,
        User.is_admin == False
    ).group_by(Talent.id, Talent.name, Talent.emoji, Talent.category)
    
    # Appliquer le filtre de recherche de talent si présent
    if talent_search:
        talents_with_users = talents_with_users.filter(Talent.name.ilike(f'%{talent_search}%'))
    
    talent_stats = talents_with_users.order_by(Talent.category, Talent.name).all()
    
    # Obtenir tous les utilisateurs avec filtres
    user_query = User.query.filter(
        User.account_active == True,
        User.is_admin == False
    )
    
    # Filtrer par talent si spécifié
    if talent_search:
        user_query = user_query.join(UserTalent).join(Talent).filter(
            Talent.name.ilike(f'%{talent_search}%')
        )
    
    # Appliquer les filtres de recherche
    if search_query:
        search_pattern = f'%{search_query}%'
        user_query = user_query.filter(
            or_(
                User.first_name.ilike(search_pattern),
                User.last_name.ilike(search_pattern),
                User.email.ilike(search_pattern)
            )
        )
    
    if availability_filter:
        user_query = user_query.filter(User.availability == availability_filter)
    
    if work_mode_filter:
        user_query = user_query.filter(User.work_mode == work_mode_filter)
    
    if city_filter:
        user_query = user_query.filter(User.city_id == int(city_filter))
    
    users = user_query.distinct().order_by(User.created_at.desc()).all()
    
    # Données pour les filtres
    all_cities = City.query.order_by(City.name).all()
    
    return render_template('talents.html', 
                         talent_stats=talent_stats,
                         total_talents=len(talent_stats),
                         users=users,
                         total_users=len(users),
                         cities=all_cities)

@bp.route('/talents/users/<int:talent_id>')
@login_required
def talent_users(talent_id):
    """Page affichant les utilisateurs qui ont un talent spécifique"""
    talent = Talent.query.get_or_404(talent_id)
    
    # Filtres de recherche
    search_query = request.args.get('search', '').strip()
    availability_filter = request.args.get('availability')
    work_mode_filter = request.args.get('work_mode')
    city_filter = request.args.get('city')
    gender_filter = request.args.get('gender')
    
    # Base query: utilisateurs qui ont ce talent
    query = User.query.join(UserTalent).filter(
        UserTalent.talent_id == talent_id,
        User.account_active == True,
        User.is_admin == False
    )
    
    # Appliquer les filtres
    if search_query:
        search_pattern = f'%{search_query}%'
        query = query.filter(
            or_(
                User.first_name.ilike(search_pattern),
                User.last_name.ilike(search_pattern),
                User.email.ilike(search_pattern)
            )
        )
    
    if availability_filter:
        query = query.filter(User.availability == availability_filter)
    
    if work_mode_filter:
        query = query.filter(User.work_mode == work_mode_filter)
    
    if city_filter:
        query = query.filter(User.city_id == int(city_filter))
    
    if gender_filter:
        query = query.filter(User.gender == gender_filter)
    
    users = query.order_by(User.created_at.desc()).all()
    
    # Données pour les filtres
    all_cities = City.query.order_by(City.name).all()
    
    return render_template('talent_users.html',
                         talent=talent,
                         users=users,
                         cities=all_cities,
                         total_users=len(users))
