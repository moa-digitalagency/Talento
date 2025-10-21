"""
Générateur de code unique pour les talents CINEMA
Format: PPVVVNNNNNNNG (12 caractères)
- PP: Code pays ISO-2 (2 lettres)
- VVV: 3 premières lettres de la ville (en majuscules)
- NNNNNN: Numéro séquentiel (6 chiffres)
- G: Genre (M/F)
"""
from app import db
from app.models.cinema_talent import CinemaTalent
from app.data.world_countries import WORLD_COUNTRIES
import re


def get_country_code(country_name):
    """Obtenir le code ISO-2 d'un pays à partir de son nom"""
    for country in WORLD_COUNTRIES:
        if country['name'].lower() == country_name.lower():
            return country['code']
    return 'XX'


def clean_city_code(city_name):
    """Extraire les 3 premières lettres d'une ville (en supprimant les caractères spéciaux)"""
    # Supprimer les accents et caractères spéciaux
    import unicodedata
    city_clean = unicodedata.normalize('NFD', city_name)
    city_clean = ''.join(c for c in city_clean if unicodedata.category(c) != 'Mn')
    
    # Garder seulement les lettres et chiffres
    city_clean = re.sub(r'[^A-Za-z0-9]', '', city_clean)
    
    # Prendre les 3 premiers caractères (en majuscules)
    return city_clean[:3].upper().ljust(3, 'X')


def generate_cinema_unique_code(country_name, city_name, gender):
    """
    Générer un code unique pour un talent CINEMA
    
    Args:
        country_name (str): Nom du pays de résidence
        city_name (str): Nom de la ville de résidence
        gender (str): Genre (M/F)
    
    Returns:
        str: Code unique de 12 caractères (PPVVVNNNNNNNG)
    """
    # Obtenir le code pays (2 lettres)
    country_code = get_country_code(country_name)
    
    # Obtenir le code ville (3 lettres)
    city_code = clean_city_code(city_name)
    
    # Trouver le prochain numéro séquentiel pour ce pays/ville
    prefix = f"{country_code}{city_code}"
    
    # Chercher le dernier code avec ce préfixe
    last_talent = CinemaTalent.query.filter(
        CinemaTalent.unique_code.like(f"{prefix}%")
    ).order_by(CinemaTalent.unique_code.desc()).first()
    
    if last_talent and last_talent.unique_code:
        # Extraire le numéro séquentiel du dernier code
        try:
            last_number = int(last_talent.unique_code[5:11])
            next_number = last_number + 1
        except (ValueError, IndexError):
            next_number = 1
    else:
        next_number = 1
    
    # Formatter le numéro sur 6 chiffres
    sequence = str(next_number).zfill(6)
    
    # Construire le code final: PPVVVNNNNNNNG
    unique_code = f"{country_code}{city_code}{sequence}{gender}"
    
    return unique_code


def generate_cinema_qr_url(unique_code):
    """
    Générer l'URL du profil CINEMA pour le QR code
    
    Args:
        unique_code (str): Code unique du talent
    
    Returns:
        str: URL du profil
    """
    from flask import current_app, url_for
    
    # En production, utiliser le domaine Replit
    base_url = current_app.config.get('BASE_URL', 'http://localhost:5000')
    return f"{base_url}/cinema/profile/{unique_code}"
