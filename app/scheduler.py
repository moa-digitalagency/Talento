"""
Scheduler pour les tâches automatisées de taalentio.com
Utilise APScheduler pour planifier les emails récapitulatifs et autres tâches périodiques
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit

scheduler = None

def send_weekly_recap():
    """
    Envoie le récapitulatif hebdomadaire à l'admin
    Appelé tous les dimanches à 12:59 PM
    """
    from app import db
    from app.models.user import User
    from app.services.email_service import email_service
    from app.models.settings import AppSettings
    from flask import current_app
    
    try:
        with current_app.app_context():
            # Récupérer l'email de l'admin depuis les paramètres
            admin_email = AppSettings.get('admin_notification_email')
            
            # Si pas configuré, chercher l'admin dans la base
            if not admin_email:
                admin = User.query.filter_by(role='admin').first()
                if admin:
                    admin_email = admin.email
                else:
                    current_app.logger.warning("⚠️ Aucun admin trouvé pour l'envoi du récapitulatif")
                    return
            
            current_app.logger.info(f"📊 Envoi du récapitulatif hebdomadaire à {admin_email}")
            
            # Envoyer le récapitulatif
            results = email_service.send_weekly_admin_recap(admin_email)
            
            if 'error' in results:
                current_app.logger.error(f"❌ Erreur lors de l'envoi du récapitulatif: {results['error']}")
            else:
                current_app.logger.info(
                    f"✅ Récapitulatif envoyé - "
                    f"Talents: {'✓' if results['talents_sent'] else '✗'} ({results['talents_count']}), "
                    f"Talents Cinéma: {'✓' if results['cinema_talents_sent'] else '✗'} ({results['cinema_talents_count']})"
                )
                
    except Exception as e:
        current_app.logger.error(f"❌ Erreur dans send_weekly_recap: {str(e)}")
        import traceback
        current_app.logger.error(traceback.format_exc())

def init_scheduler(app):
    """
    Initialise le scheduler avec toutes les tâches planifiées
    
    Args:
        app: Instance Flask
    """
    global scheduler
    
    # Éviter de créer plusieurs instances du scheduler
    if scheduler is not None:
        app.logger.info("⚠️ Scheduler déjà initialisé")
        return scheduler
    
    app.logger.info("🕐 Initialisation du scheduler...")
    
    scheduler = BackgroundScheduler({
        'apscheduler.timezone': 'Africa/Casablanca'  # Timezone Maroc
    })
    
    # Ajouter la tâche de récapitulatif hebdomadaire
    # Tous les dimanches à 12:59 PM
    scheduler.add_job(
        func=send_weekly_recap,
        trigger=CronTrigger(day_of_week='sun', hour=12, minute=59),
        id='weekly_recap',
        name='Récapitulatif Hebdomadaire Admin',
        replace_existing=True
    )
    
    app.logger.info("✅ Tâche planifiée: Récapitulatif hebdomadaire (Dimanche 12:59)")
    
    # Démarrer le scheduler
    scheduler.start()
    app.logger.info("🚀 Scheduler démarré")
    
    # Arrêter proprement le scheduler quand l'app se ferme
    atexit.register(lambda: scheduler.shutdown() if scheduler else None)
    
    return scheduler

def get_scheduler_status():
    """
    Retourne le statut du scheduler et ses tâches
    
    Returns:
        dict avec le statut et la liste des tâches
    """
    global scheduler
    
    if scheduler is None:
        return {
            'running': False,
            'jobs': []
        }
    
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            'id': job.id,
            'name': job.name,
            'next_run': job.next_run_time.strftime('%d/%m/%Y %H:%M:%S') if job.next_run_time else 'N/A',
            'trigger': str(job.trigger)
        })
    
    return {
        'running': scheduler.running,
        'jobs': jobs
    }

def trigger_weekly_recap_now():
    """
    Déclenche manuellement le récapitulatif hebdomadaire (pour test)
    
    Returns:
        dict avec les résultats
    """
    from flask import current_app
    
    current_app.logger.info("🔄 Déclenchement manuel du récapitulatif hebdomadaire")
    send_weekly_recap()
    return {'success': True, 'message': 'Récapitulatif déclenché'}
