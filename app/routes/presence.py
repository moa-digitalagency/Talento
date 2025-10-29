"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.project import Project, ProjectTalent
from app.models.cinema_talent import CinemaTalent
from app.models.attendance import Attendance
from datetime import datetime, timedelta, date
from functools import wraps

bp = Blueprint('presence', __name__, url_prefix='/presence')

def presence_required(f):
    """Décorateur pour vérifier que l'utilisateur a le rôle 'presence' ou est admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Veuillez vous connecter pour accéder à cette page.', 'error')
            return redirect(url_for('auth.login'))
        
        if not (current_user.is_admin or current_user.role == 'presence'):
            flash('Vous n\'avez pas les droits d\'accès à cette section.', 'error')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@presence_required
def index():
    """Liste des projets pour enregistrer les présences"""
    projects = Project.query.filter_by(is_active=True).order_by(Project.name).all()
    return render_template('presence/index.html', projects=projects)

@bp.route('/project/<int:project_id>')
@login_required
@presence_required
def project_attendance(project_id):
    """Vue de gestion des présences pour un projet spécifique"""
    project = Project.query.get_or_404(project_id)
    
    # Obtenir la date sélectionnée (par défaut aujourd'hui)
    selected_date_str = request.args.get('date')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()
    
    # Obtenir les présences du jour
    today_attendances = Attendance.query.filter_by(
        project_id=project_id,
        date=selected_date
    ).all()
    
    # Créer un dictionnaire pour accès rapide
    attendance_by_code = {att.cinema_talent_code: att for att in today_attendances}
    
    # Obtenir tous les talents assignés au projet
    project_talents = ProjectTalent.query.filter_by(project_id=project_id).all()
    
    # Enrichir les données avec les infos des talents
    talents_data = []
    for pt in project_talents:
        talent = CinemaTalent.query.filter_by(unique_code=pt.cinema_talent_code).first()
        if talent:
            attendance = attendance_by_code.get(pt.cinema_talent_code)
            talents_data.append({
                'code': pt.cinema_talent_code,
                'talent': talent,
                'attendance': attendance,
                'status': 'checked_out' if (attendance and attendance.check_out_time) else ('checked_in' if attendance else 'absent')
            })
    
    return render_template('presence/project_attendance.html',
                         project=project,
                         talents_data=talents_data,
                         selected_date=selected_date)

@bp.route('/record', methods=['POST'])
@login_required
@presence_required
def record_attendance():
    """Enregistre une présence (arrivée ou départ)"""
    project_id = request.form.get('project_id', type=int)
    cinema_talent_code = request.form.get('cinema_talent_code', '').strip().upper().replace('-', '')
    
    if not project_id or not cinema_talent_code:
        return jsonify({'success': False, 'message': 'Données manquantes'}), 400
    
    # Vérifier que le projet existe
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'success': False, 'message': 'Projet non trouvé'}), 404
    
    # Vérifier que le talent existe
    talent = CinemaTalent.query.filter_by(unique_code=cinema_talent_code).first()
    if not talent:
        return jsonify({'success': False, 'message': f'Talent {cinema_talent_code} non trouvé'}), 404
    
    # Vérifier que le talent est assigné au projet
    assignment = ProjectTalent.query.filter_by(
        project_id=project_id,
        cinema_talent_code=cinema_talent_code
    ).first()
    
    if not assignment:
        return jsonify({
            'success': False,
            'message': f'{talent.first_name} {talent.last_name} n\'est pas assigné à ce projet'
        }), 400
    
    # Enregistrer la présence
    try:
        attendance, action = Attendance.get_or_create_today(
            project_id=project_id,
            cinema_talent_code=cinema_talent_code,
            recorded_by=current_user.id
        )
        
        if action == 'checkin':
            message = f'✅ Arrivée enregistrée: {talent.first_name} {talent.last_name} à {attendance.check_in_time.strftime("%H:%M")}'
        elif action == 'checkout':
            duration = attendance.get_duration_formatted()
            message = f'👋 Départ enregistré: {talent.first_name} {talent.last_name} à {attendance.check_out_time.strftime("%H:%M")} (Durée: {duration})'
        else:
            message = f'ℹ️ {talent.first_name} {talent.last_name} a déjà un enregistrement complet aujourd\'hui'
        
        return jsonify({
            'success': True,
            'action': action,
            'message': message,
            'attendance': {
                'check_in': attendance.check_in_time.isoformat() if attendance.check_in_time else None,
                'check_out': attendance.check_out_time.isoformat() if attendance.check_out_time else None,
                'duration': attendance.get_duration_formatted()
            }
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erreur: {str(e)}'}), 500

@bp.route('/check_in_all/<int:project_id>', methods=['POST'])
@login_required
@presence_required
def check_in_all(project_id):
    """Marque l'arrivée de tous les talents assignés au projet"""
    project = Project.query.get_or_404(project_id)
    
    # Obtenir tous les talents assignés
    project_talents = ProjectTalent.query.filter_by(project_id=project_id).all()
    
    checked_in = 0
    already_present = 0
    today = date.today()
    
    for pt in project_talents:
        # Vérifier si déjà enregistré aujourd'hui
        existing = Attendance.query.filter_by(
            project_id=project_id,
            cinema_talent_code=pt.cinema_talent_code,
            date=today
        ).first()
        
        if not existing:
            # Créer l'enregistrement d'arrivée
            attendance = Attendance(
                project_id=project_id,
                cinema_talent_code=pt.cinema_talent_code,
                date=today,
                check_in_time=datetime.utcnow(),
                recorded_by=current_user.id
            )
            db.session.add(attendance)
            checked_in += 1
        else:
            already_present += 1
    
    try:
        db.session.commit()
        flash(f'✅ {checked_in} talent(s) marqué(s) présent(s). {already_present} déjà enregistré(s).', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Erreur: {str(e)}', 'error')
    
    return redirect(url_for('presence.project_attendance', project_id=project_id))

@bp.route('/check_out_all/<int:project_id>', methods=['POST'])
@login_required
@presence_required
def check_out_all(project_id):
    """Marque le départ de tous les talents présents aujourd'hui"""
    project = Project.query.get_or_404(project_id)
    today = date.today()
    
    # Obtenir toutes les présences d'aujourd'hui sans heure de départ
    attendances = Attendance.query.filter_by(
        project_id=project_id,
        date=today
    ).filter(Attendance.check_out_time.is_(None)).all()
    
    checked_out = 0
    for attendance in attendances:
        attendance.check_out_time = datetime.utcnow()
        attendance.updated_at = datetime.utcnow()
        checked_out += 1
    
    try:
        db.session.commit()
        flash(f'👋 {checked_out} talent(s) marqué(s) comme partis.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Erreur: {str(e)}', 'error')
    
    return redirect(url_for('presence.project_attendance', project_id=project_id))

@bp.route('/history/<string:cinema_talent_code>')
@login_required
def talent_history(cinema_talent_code):
    """Affiche l'historique de présence d'un talent"""
    talent = CinemaTalent.query.filter_by(unique_code=cinema_talent_code).first_or_404()
    
    # Obtenir toutes les présences du talent
    attendances = Attendance.query.filter_by(
        cinema_talent_code=cinema_talent_code
    ).order_by(Attendance.date.desc()).all()
    
    # Grouper par projet
    by_project = {}
    for att in attendances:
        if att.project_id not in by_project:
            by_project[att.project_id] = {
                'project': att.project,
                'attendances': [],
                'total_minutes': 0
            }
        by_project[att.project_id]['attendances'].append(att)
        by_project[att.project_id]['total_minutes'] += att.get_duration_minutes()
    
    # Formater les totaux
    for proj_data in by_project.values():
        minutes = proj_data['total_minutes']
        hours = minutes // 60
        mins = minutes % 60
        proj_data['total_formatted'] = f"{hours}h {mins:02d}min"
        proj_data['days_worked'] = len([a for a in proj_data['attendances'] if a.check_out_time])
    
    return render_template('presence/talent_history.html',
                         talent=talent,
                         by_project=by_project)

@bp.route('/export/<int:project_id>')
@login_required
@presence_required
def export_attendance(project_id):
    """Exporte les présences d'un projet"""
    from app.services.export_service import export_attendance_to_excel
    
    project = Project.query.get_or_404(project_id)
    
    # Paramètres de date
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    period = request.args.get('period', 'all')
    
    today = date.today()
    
    if period == 'day':
        start_date = end_date = today
    elif period == 'week':
        start_date = today - timedelta(days=today.weekday())
        end_date = today
    elif period == 'month':
        start_date = today.replace(day=1)
        end_date = today
    else:
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Récupérer les données
    attendances = Attendance.get_project_attendance_summary(project_id, start_date, end_date)
    
    # Exporter
    return export_attendance_to_excel(project, attendances, start_date, end_date)
