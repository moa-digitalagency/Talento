"""
Service pour la gestion de la liste de surveillance (watchlist)
Vérifie si les nouvelles inscriptions correspondent à des noms surveillés
"""
import unicodedata
from flask import current_app
from app.models.settings import AppSettings
from app.services.email_service import email_service

def normalize_name(text):
    """
    Normalise un nom en retirant les accents et les caractères spéciaux
    
    Args:
        text: Texte à normaliser
    
    Returns:
        str: Texte normalisé sans accents en minuscules
    """
    if not text:
        return ""
    # Supprimer les accents
    nfkd_form = unicodedata.normalize('NFKD', text.lower())
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def check_watchlist_and_notify(talent_obj, talent_type='talent'):
    """
    Vérifie si une personne est dans la liste de surveillance et envoie une notification
    
    Args:
        talent_obj: Objet User ou CinemaTalent
        talent_type: 'talent' ou 'cinema'
    
    Returns:
        bool: True si une notification a été envoyée, False sinon
    """
    try:
        # Vérifier si la watchlist est activée
        watchlist_enabled = AppSettings.get('watchlist_enabled', False)
        if not watchlist_enabled:
            return False
        
        # Récupérer la liste des noms à surveiller
        watchlist_names_raw = AppSettings.get('watchlist_names', '')
        if not watchlist_names_raw:
            return False
        
        watchlist_names = [name.strip() for name in watchlist_names_raw.split('\n') if name.strip()]
        if not watchlist_names:
            return False
        
        # Normaliser les noms du talent
        full_name_normalized = normalize_name(talent_obj.full_name)
        first_name_normalized = normalize_name(talent_obj.first_name)
        last_name_normalized = normalize_name(talent_obj.last_name)
        
        # Vérifier si le nom est dans la liste
        match_found = False
        for watch_name in watchlist_names:
            watch_name_normalized = normalize_name(watch_name)
            if (watch_name_normalized in full_name_normalized or 
                watch_name_normalized == first_name_normalized or 
                watch_name_normalized == last_name_normalized):
                match_found = True
                current_app.logger.info(f"🔔 Watchlist match trouvé: {talent_obj.full_name} correspond à '{watch_name}'")
                break
        
        if not match_found:
            return False
        
        # Préparer les données du talent
        if talent_type == 'talent':
            talent_data = {
                'full_name': talent_obj.full_name,
                'unique_code': talent_obj.unique_code,
                'city': talent_obj.city.name if talent_obj.city else 'N/A',
                'country': talent_obj.country.name if talent_obj.country else 'N/A'
            }
        else:  # cinema
            talent_data = {
                'full_name': talent_obj.full_name,
                'unique_code': talent_obj.unique_code,
                'city': talent_obj.city or 'N/A',
                'country': talent_obj.country or 'N/A'
            }
        
        # Récupérer l'email de notification
        watchlist_notification_email = AppSettings.get('watchlist_notification_email', '')
        if not watchlist_notification_email:
            current_app.logger.warning("⚠️ Watchlist activée mais pas d'email de notification configuré")
            return False
        
        # Envoyer la notification
        success = email_service.send_watchlist_notification(
            admin_email=watchlist_notification_email,
            talent_data=talent_data,
            talent_type=talent_type
        )
        
        if success:
            current_app.logger.info(f"✅ Notification watchlist envoyée pour {talent_obj.full_name} à {watchlist_notification_email}")
        else:
            current_app.logger.error(f"❌ Échec d'envoi de la notification watchlist pour {talent_obj.full_name}")
        
        return success
        
    except Exception as e:
        current_app.logger.error(f"Erreur dans check_watchlist_and_notify: {str(e)}")
        import traceback
        current_app.logger.error(traceback.format_exc())
        return False
