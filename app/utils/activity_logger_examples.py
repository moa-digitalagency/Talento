"""
Exemples d'utilisation du middleware de logging automatique
Ce fichier montre comment utiliser les différentes fonctionnalités du module activity_logger
"""

from flask import Blueprint
from flask_login import current_user
from app.utils.activity_logger import log_activity, log_page_view, log_action, log_settings_change

# Exemple d'utilisation du Blueprint (à titre d'exemple, pas utilisé en production)
example_bp = Blueprint('example', __name__)


# EXEMPLE 1: Utilisation du decorator @log_activity
@example_bp.route('/production/create', methods=['POST'])
@log_activity('create', 'cinema', 'Production')
def create_production():
    """
    Le decorator loggera automatiquement:
    - Action type: create
    - Category: cinema
    - Resource type: Production
    - User, IP, browser, device, etc.
    - Status: success ou error selon le résultat
    """
    # Votre code de création de production ici
    pass


@example_bp.route('/settings/update', methods=['POST'])
@log_activity('update', 'settings', 'AppSettings')
def update_settings():
    """
    Le decorator capture automatiquement toute erreur et la loggue
    """
    # Votre code de mise à jour des paramètres
    pass


# EXEMPLE 2: Utilisation de log_page_view() pour des consultations personnalisées
@example_bp.route('/profile/view/<int:user_id>')
def view_profile(user_id):
    """
    Logger manuellement une consultation de page
    Utile pour des pages spéciales ou des actions de consultation
    """
    # Logger la consultation du profil
    log_page_view(
        url=f'/profile/view/{user_id}',
        user=current_user  # Optionnel, utilise current_user par défaut
    )
    
    # Votre code de visualisation du profil
    pass


# EXEMPLE 3: Utilisation de log_action() pour des actions personnalisées
def export_talents_to_excel():
    """
    Logger une action personnalisée avec tous les détails
    """
    try:
        # Votre code d'export ici
        file_path = '/path/to/export.xlsx'
        
        # Logger l'action d'export avec succès
        log_action(
            action_type='export',
            description='Export des talents vers Excel',
            resource_type='Talent',
            resource_id=None,  # Pas d'ID spécifique pour un export groupé
            status='success',
            user=current_user,
            extra_data={
                'file_path': file_path,
                'format': 'xlsx',
                'count': 150
            }
        )
    except Exception as e:
        # Logger l'erreur
        log_action(
            action_type='export',
            description='Export des talents vers Excel (échec)',
            resource_type='Talent',
            status='error',
            error_message=str(e),
            user=current_user
        )
        raise


def delete_production(production_id):
    """
    Logger une suppression avec l'ID de la ressource
    """
    log_action(
        action_type='delete',
        description=f'Suppression de la production #{production_id}',
        resource_type='Production',
        resource_id=production_id,
        status='success',
        user=current_user
    )
    
    # Votre code de suppression
    pass


# EXEMPLE 4: Utilisation de log_settings_change() pour les modifications de paramètres
def update_app_setting(setting_name, new_value):
    """
    Logger spécifiquement les changements de paramètres
    Capture l'ancienne et la nouvelle valeur automatiquement
    """
    from app.models.settings import AppSettings
    
    # Récupérer l'ancienne valeur
    old_value = AppSettings.get(setting_name)
    
    # Mettre à jour le paramètre
    AppSettings.set(setting_name, new_value)
    
    # Logger le changement
    log_settings_change(
        setting_name=setting_name,
        old_value=old_value,
        new_value=new_value,
        user=current_user  # Optionnel
    )


# EXEMPLE 5: Logger dans un contexte sans utilisateur authentifié
def public_action():
    """
    Le système peut logger même sans utilisateur connecté
    """
    log_action(
        action_type='view',
        description='Consultation de la page publique',
        resource_type='PublicPage',
        status='success',
        user=None  # Sera enregistré comme "Anonyme"
    )


# EXEMPLE 6: Combinaison du decorator avec du logging manuel
@example_bp.route('/project/<int:project_id>/assign', methods=['POST'])
@log_activity('update', 'project', 'Project')
def assign_talent_to_project(project_id):
    """
    Le decorator loggue l'action globale,
    mais vous pouvez ajouter des logs supplémentaires pour plus de détails
    """
    talent_id = request.form.get('talent_id')
    
    # Le decorator loggue déjà l'action principale
    # Mais vous pouvez ajouter un log détaillé supplémentaire
    log_action(
        action_type='assign',
        description=f'Assignation du talent #{talent_id} au projet #{project_id}',
        resource_type='TalentAssignment',
        resource_id=project_id,
        status='success',
        extra_data={
            'talent_id': talent_id,
            'project_id': project_id
        }
    )
    
    # Votre code d'assignation
    pass


"""
NOTES IMPORTANTES:

1. Le middleware loggue automatiquement:
   - Toutes les requêtes GET (consultations de pages)
   - Toutes les requêtes POST/PUT/DELETE (actions)
   - NE loggue PAS les fichiers statiques (.css, .js, .png, etc.)

2. Le decorator @log_activity:
   - Capture automatiquement les erreurs et les loggue
   - Ne bloque jamais l'exécution même en cas d'erreur de logging
   - Enregistre le statut (success/error) automatiquement

3. Les helper functions:
   - log_page_view(): Pour les consultations de pages personnalisées
   - log_action(): Pour les actions personnalisées avec tous les détails
   - log_settings_change(): Spécialisé pour les changements de paramètres

4. Gestion des erreurs:
   - Toutes les fonctions de logging sont "gracieuses"
   - Une erreur de logging n'affectera jamais l'application
   - Les erreurs sont affichées dans les logs mais n'arrêtent pas l'exécution

5. Performance:
   - Le logging est asynchrone et n'impacte pas les performances
   - Les requêtes statiques sont automatiquement exclues
   - La base de données peut être indisponible sans impacter l'application
"""
