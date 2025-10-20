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

# Rediriger l'ancien /admin/dashboard vers /
@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return redirect(url_for('main.index'))

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

@bp.route('/user/<int:user_id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_active(user_id):
    user = User.query.get_or_404(user_id)
    user.account_active = not user.account_active
    db.session.commit()
    flash(f"Compte {'activé' if user.account_active else 'désactivé'} avec succès.", 'success')
    return redirect(url_for('main.index'))

@bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('Impossible de supprimer un compte administrateur.', 'error')
        return redirect(url_for('main.index'))
    
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé avec succès.', 'success')
    return redirect(url_for('main.index'))

@bp.route('/export/excel')
@login_required
@admin_required
def export_excel():
    users = User.query.filter(User.is_admin == False).all()
    excel_bytes = ExportService.export_to_excel(users)
    
    buffer = io.BytesIO(excel_bytes)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'talento_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    )

@bp.route('/export/csv')
@login_required
@admin_required
def export_csv():
    users = User.query.filter(User.is_admin == False).all()
    csv_data = ExportService.export_to_csv(users)
    
    buffer = io.BytesIO()
    buffer.write(csv_data.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'talento_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@bp.route('/export/pdf')
@login_required
@admin_required
def export_pdf():
    users = User.query.filter(User.is_admin == False).all()
    pdf_bytes = ExportService.export_list_to_pdf(users)
    
    buffer = io.BytesIO(pdf_bytes)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'talento_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )

@bp.route('/export/pdf/<int:user_id>')
@login_required
@admin_required
def export_pdf_individual(user_id):
    user = User.query.get_or_404(user_id)
    pdf_bytes = ExportService.export_talent_card_pdf(user)
    
    buffer = io.BytesIO(pdf_bytes)
    buffer.seek(0)
    
    filename = f'talento_{user.unique_code}_{datetime.now().strftime("%Y%m%d")}.pdf'
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

@bp.route('/analyze-cv/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def analyze_cv(user_id):
    user = User.query.get_or_404(user_id)
    
    if not user.cv_filename:
        return jsonify({'error': 'Aucun CV disponible pour cet utilisateur'}), 400
    
    try:
        analysis = CVAnalyzerService.analyze_cv(user)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/talent/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_talent():
    if request.method == 'POST':
        name = request.form.get('name')
        emoji = request.form.get('emoji')
        category = request.form.get('category')
        
        if not all([name, emoji, category]):
            flash('Tous les champs sont requis.', 'error')
            return redirect(url_for('admin.new_talent'))
        
        existing = Talent.query.filter_by(name=name).first()
        if existing:
            flash('Ce talent existe déjà.', 'error')
            return redirect(url_for('admin.new_talent'))
        
        talent = Talent(name=name, emoji=emoji, category=category)
        db.session.add(talent)
        db.session.commit()
        
        flash('Talent ajouté avec succès.', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('admin/talent_form.html')

@bp.route('/talents')
@login_required
@admin_required
def talents_list():
    talents = Talent.query.order_by(Talent.category, Talent.name).all()
    return render_template('admin/talents_list.html', talents=talents)

@bp.route('/talent/<int:talent_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_talent(talent_id):
    talent = Talent.query.get_or_404(talent_id)
    
    usage_count = UserTalent.query.filter_by(talent_id=talent_id).count()
    if usage_count > 0:
        flash(f'Impossible de supprimer ce talent. Il est utilisé par {usage_count} profil(s).', 'error')
        return redirect(url_for('admin.talents_list'))
    
    db.session.delete(talent)
    db.session.commit()
    flash('Talent supprimé avec succès.', 'success')
    return redirect(url_for('admin.talents_list'))

@bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.first_name = request.form.get('first_name', '').strip()
        user.last_name = request.form.get('last_name', '').strip()
        user.email = request.form.get('email', '').strip()
        
        dob_str = request.form.get('date_of_birth')
        if dob_str:
            try:
                from datetime import datetime as dt
                user.date_of_birth = dt.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        user.gender = request.form.get('gender')
        user.phone = request.form.get('phone', '').strip() or None
        user.whatsapp = request.form.get('whatsapp', '').strip() or None
        user.address = request.form.get('address', '').strip() or None
        
        country_id = request.form.get('country_id')
        user.country_id = int(country_id) if country_id else None
        
        city_id = request.form.get('city_id')
        user.city_id = int(city_id) if city_id else None
        
        user.availability = request.form.get('availability')
        user.work_mode = request.form.get('work_mode')
        user.rate_range = request.form.get('rate_range', '').strip() or None
        user.years_experience = request.form.get('years_experience') or None
        
        user.bio = request.form.get('bio', '').strip() or None
        user.portfolio_url = request.form.get('portfolio_url', '').strip() or None
        
        user.linkedin = request.form.get('linkedin', '').strip() or None
        user.instagram = request.form.get('instagram', '').strip() or None
        user.twitter = request.form.get('twitter', '').strip() or None
        user.facebook = request.form.get('facebook', '').strip() or None
        user.github = request.form.get('github', '').strip() or None
        user.behance = request.form.get('behance', '').strip() or None
        user.dribbble = request.form.get('dribbble', '').strip() or None
        user.youtube = request.form.get('youtube', '').strip() or None
        
        talent_ids = request.form.getlist('talents')
        UserTalent.query.filter_by(user_id=user.id).delete()
        for talent_id in talent_ids:
            if talent_id:
                user_talent = UserTalent(user_id=user.id, talent_id=int(talent_id))
                db.session.add(user_talent)
        
        db.session.commit()
        flash('Profil mis à jour avec succès.', 'success')
        return redirect(url_for('admin.user_detail', user_id=user.id))
    
    countries = Country.query.order_by(Country.name).all()
    cities = City.query.order_by(City.name).all()
    all_talents = Talent.query.order_by(Talent.category, Talent.name).all()
    user_talent_ids = [ut.talent_id for ut in user.talents]
    
    return render_template('admin/user_edit.html', 
                         user=user, 
                         countries=countries, 
                         cities=cities,
                         all_talents=all_talents,
                         user_talent_ids=user_talent_ids)
