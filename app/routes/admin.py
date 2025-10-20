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
    buffer = ExportService.export_to_excel(users)
    
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
    buffer = ExportService.export_list_to_pdf(users)
    
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
    buffer = ExportService.export_talent_card_pdf(user)
    
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
