"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from app import db
from datetime import datetime, timedelta, date

class Attendance(db.Model):
    """Modèle pour gérer les présences des talents cinéma sur les projets"""
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Lien avec le projet
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    # Code du talent cinéma
    cinema_talent_code = db.Column(db.String(11), nullable=False)
    
    # Date de la présence
    date = db.Column(db.Date, nullable=False, default=date.today)
    
    # Heures d'arrivée et de départ
    check_in_time = db.Column(db.DateTime, nullable=True)
    check_out_time = db.Column(db.DateTime, nullable=True)
    
    # Utilisateur qui a enregistré la présence
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    project = db.relationship('Project', backref=db.backref('attendances', lazy='dynamic'))
    recorder = db.relationship('User', backref=db.backref('recorded_attendances', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Attendance {self.cinema_talent_code} - Project {self.project_id} - {self.date}>'
    
    def get_duration_minutes(self):
        """Calcule la durée en minutes entre arrivée et départ"""
        if self.check_in_time and self.check_out_time:
            delta = self.check_out_time - self.check_in_time
            return int(delta.total_seconds() / 60)
        return 0
    
    def get_duration_formatted(self):
        """Retourne la durée formatée en heures et minutes"""
        minutes = self.get_duration_minutes()
        if minutes == 0:
            return "En cours..."
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h {mins:02d}min"
    
    def is_checked_out(self):
        """Vérifie si le talent a quitté"""
        return self.check_out_time is not None
    
    @staticmethod
    def get_or_create_today(project_id, cinema_talent_code, recorded_by):
        """
        Récupère ou crée une présence pour aujourd'hui
        Premier appel = check-in, deuxième appel = check-out
        """
        today = datetime.utcnow().date()
        
        # Chercher une présence existante pour aujourd'hui
        attendance = Attendance.query.filter_by(
            project_id=project_id,
            cinema_talent_code=cinema_talent_code,
            date=today
        ).first()
        
        if attendance:
            # Si déjà enregistré, c'est le départ
            if attendance.check_out_time is None:
                attendance.check_out_time = datetime.utcnow()
                attendance.updated_at = datetime.utcnow()
                db.session.commit()
                return attendance, 'checkout'
            else:
                return attendance, 'already_complete'
        else:
            # Nouvelle présence = arrivée
            attendance = Attendance(
                project_id=project_id,
                cinema_talent_code=cinema_talent_code,
                date=today,
                check_in_time=datetime.utcnow(),
                recorded_by=recorded_by
            )
            db.session.add(attendance)
            db.session.commit()
            return attendance, 'checkin'
    
    @staticmethod
    def get_project_attendance_summary(project_id, start_date=None, end_date=None):
        """
        Obtient un résumé des présences pour un projet
        """
        query = Attendance.query.filter_by(project_id=project_id)
        
        if start_date:
            query = query.filter(Attendance.date >= start_date)
        if end_date:
            query = query.filter(Attendance.date <= end_date)
        
        return query.order_by(Attendance.date.desc(), Attendance.check_in_time.desc()).all()
    
    @staticmethod
    def get_talent_total_hours(cinema_talent_code, project_id):
        """
        Calcule le total d'heures travaillées par un talent sur un projet
        """
        attendances = Attendance.query.filter_by(
            cinema_talent_code=cinema_talent_code,
            project_id=project_id
        ).filter(Attendance.check_out_time.isnot(None)).all()
        
        total_minutes = sum(att.get_duration_minutes() for att in attendances)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        return {
            'total_minutes': total_minutes,
            'formatted': f"{hours}h {minutes:02d}min",
            'hours': hours,
            'minutes': minutes,
            'days_worked': len(attendances)
        }
