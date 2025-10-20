from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, jsonify
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime
from sqlalchemy import or_, and_, func
from app import db
from app.models.user import User
from app.models.talent import Talent, UserTalent
from app.models.location import Country, City
from app.services.export_service import ExportService
from app.services.cv_analyzer import CVAnalyzerService
import io

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Accès réservé aux administrateurs.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
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
    
    query = User.query.filter(User.is_admin == False)
    
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
    
    all_talents = Talent.query.order_by(Talent.category, Talent.name).all()
    all_countries = Country.query.order_by(Country.name).all()
    all_cities = City.query.order_by(City.name).all()
    
    stats = {
        'total_users': User.query.filter(User.is_admin == False).count(),
        'with_cv': User.query.filter(User.cv_filename.isnot(None)).count(),
        'with_portfolio': User.query.filter(User.portfolio_url.isnot(None)).count(),
        'filtered_count': len(users)
    }
    
    return render_template('admin/dashboard.html', 
                         users=users,
                         talents=all_talents,
                         countries=all_countries,
                         cities=all_cities,
                         stats=stats)

@bp.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.filter(User.is_admin == False).order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=all_users)

@bp.route('/user/<int:user_id>')
@login_required
@admin_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_detail.html', user=user)

@bp.route('/export/excel')
@login_required
@admin_required
def export_excel():
    users = User.query.filter(User.is_admin == False).all()
    
    excel_data = ExportService.export_to_excel(users)
    
    return send_file(
        io.BytesIO(excel_data),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'talents_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    )

@bp.route('/export/csv')
@login_required
@admin_required
def export_csv():
    users = User.query.filter(User.is_admin == False).all()
    
    csv_data = ExportService.export_to_csv(users)
    
    return send_file(
        io.BytesIO(csv_data.encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'talents_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@bp.route('/export/pdf')
@login_required
@admin_required
def export_pdf():
    users = User.query.filter(User.is_admin == False).all()
    
    pdf_data = ExportService.export_list_to_pdf(users)
    
    return send_file(
        io.BytesIO(pdf_data),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'talents_list_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )

@bp.route('/user/<int:user_id>/export_pdf')
@login_required
@admin_required
def export_user_pdf(user_id):
    user = User.query.get_or_404(user_id)
    
    pdf_data = ExportService.export_talent_card_pdf(user)
    
    return send_file(
        io.BytesIO(pdf_data),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'fiche_talent_{user.unique_code}_{datetime.now().strftime("%Y%m%d")}.pdf'
    )

@bp.route('/user/<int:user_id>/analyze_cv', methods=['POST'])
@login_required
@admin_required
def analyze_cv(user_id):
    user = User.query.get_or_404(user_id)
    
    if not user.cv_filename:
        return jsonify({'success': False, 'error': 'Aucun CV trouvé pour cet utilisateur'}), 400
    
    user_data = {
        'name': user.full_name,
        'talents': [ut.talent.name for ut in user.talents],
        'location': f"{user.city.name if user.city else ''}, {user.country.name if user.country else ''}"
    }
    
    analysis = CVAnalyzerService.analyze_cv(user.cv_filename, user_data)
    
    if analysis['success']:
        import json
        user.cv_analysis = json.dumps(analysis, ensure_ascii=False)
        user.cv_analyzed_at = datetime.utcnow()
        user.profile_score = max(user.profile_score or 0, analysis['score'])
        db.session.commit()
        
        flash(f'CV analysé avec succès. Score: {analysis["score"]}/100', 'success')
        return jsonify({'success': True, 'analysis': analysis})
    else:
        flash(f'Erreur lors de l\'analyse: {analysis["error"]}', 'error')
        return jsonify(analysis), 500

@bp.route('/search_by_qr')
@login_required
@admin_required
def search_by_qr():
    qr_code = request.args.get('qr', '').strip()
    
    if not qr_code:
        flash('Veuillez scanner un QR code', 'warning')
        return redirect(url_for('admin.dashboard'))
    
    user = User.query.filter(
        or_(
            User.unique_code == qr_code.replace('-', '').upper(),
            User.qr_code_filename.contains(qr_code)
        )
    ).first()
    
    if user:
        return redirect(url_for('admin.user_detail', user_id=user.id))
    else:
        flash('Aucun talent trouvé avec ce QR code', 'error')
        return redirect(url_for('admin.dashboard'))

# ========== CRUD TALENTS ==========

@bp.route('/talents')
@login_required
@admin_required
def talents_list():
    """Liste tous les talents avec statistiques"""
    talents = db.session.query(
        Talent,
        func.count(UserTalent.user_id).label('user_count')
    ).outerjoin(UserTalent).group_by(Talent.id).order_by(Talent.category, Talent.name).all()
    
    return render_template('admin/talents_list.html', talents=talents)

@bp.route('/talents/add', methods=['GET', 'POST'])
@login_required
@admin_required
def talent_add():
    """Ajouter un nouveau talent"""
    if request.method == 'POST':
        name = request.form.get('name')
        emoji = request.form.get('emoji')
        category = request.form.get('category')
        
        if not name or not category:
            flash('Le nom et la catégorie sont obligatoires', 'error')
            return redirect(url_for('admin.talent_add'))
        
        existing = Talent.query.filter_by(name=name).first()
        if existing:
            flash('Un talent avec ce nom existe déjà', 'error')
            return redirect(url_for('admin.talent_add'))
        
        talent = Talent(name=name, emoji=emoji or '⭐', category=category)
        db.session.add(talent)
        db.session.commit()
        
        flash(f'Talent "{name}" créé avec succès', 'success')
        return redirect(url_for('admin.talents_list'))
    
    categories = db.session.query(Talent.category).distinct().order_by(Talent.category).all()
    categories = [c[0] for c in categories]
    return render_template('admin/talent_form.html', talent=None, categories=categories)

@bp.route('/talents/edit/<int:talent_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def talent_edit(talent_id):
    """Modifier un talent existant"""
    talent = Talent.query.get_or_404(talent_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        emoji = request.form.get('emoji')
        category = request.form.get('category')
        
        if not name or not category:
            flash('Le nom et la catégorie sont obligatoires', 'error')
            return redirect(url_for('admin.talent_edit', talent_id=talent_id))
        
        # Vérifier les noms dupliqués (sauf le talent actuel)
        existing = Talent.query.filter(Talent.name == name, Talent.id != talent_id).first()
        if existing:
            flash('Un talent avec ce nom existe déjà', 'error')
            return redirect(url_for('admin.talent_edit', talent_id=talent_id))
        
        talent.name = name
        talent.emoji = emoji or '⭐'
        talent.category = category
        db.session.commit()
        
        flash(f'Talent "{name}" modifié avec succès', 'success')
        return redirect(url_for('admin.talents_list'))
    
    categories = db.session.query(Talent.category).distinct().order_by(Talent.category).all()
    categories = [c[0] for c in categories]
    return render_template('admin/talent_form.html', talent=talent, categories=categories)

@bp.route('/talents/delete/<int:talent_id>', methods=['POST'])
@login_required
@admin_required
def talent_delete(talent_id):
    """Supprimer un talent"""
    talent = Talent.query.get_or_404(talent_id)
    
    user_count = UserTalent.query.filter_by(talent_id=talent_id).count()
    if user_count > 0:
        flash(f'Impossible de supprimer "{talent.name}" car {user_count} utilisateur(s) l\'utilisent', 'error')
        return redirect(url_for('admin.talents_list'))
    
    name = talent.name
    db.session.delete(talent)
    db.session.commit()
    
    flash(f'Talent "{name}" supprimé avec succès', 'success')
    return redirect(url_for('admin.talents_list'))
