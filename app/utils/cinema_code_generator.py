"""
Générateur de code unique pour les talents CINEMA
Format: PPVVVNNNNNG (10 caractères)
- PP: Code pays ISO-2 (2 lettres)
- VVV: 3 premières lettres de la ville (en majuscules)
- NNNN: Numéro séquentiel (4 chiffres)
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
        str: Code unique de 10 caractères (PPVVVNNNNNG)
    
    Note:
        Le numéro séquentiel est incrémenté par PAYS uniquement, 
        pas par combinaison pays+ville. Ainsi:
        - SNCAS0001M (Sénégal, Casablanca)
        - CDCAS0001M (Tchad, Casablanca) 
        Et non SNCAS0001M puis SNCAS0002M pour deux personnes de la même ville.
    """
    # Obtenir le code pays (2 lettres)
    country_code = get_country_code(country_name)
    
    # Obtenir le code ville (3 lettres)
    city_code = clean_city_code(city_name)
    
    # Trouver le prochain numéro séquentiel pour ce PAYS uniquement
    # On cherche tous les codes qui commencent par le code pays (2 lettres)
    # et on trouve le numéro séquentiel maximum (pas de tri lexicographique!)
    all_talents = CinemaTalent.query.filter(
        CinemaTalent.unique_code.like(f"{country_code}%")
    ).all()
    
    max_sequence = 0
    if all_talents:
        for talent in all_talents:
            if talent.unique_code:
                try:
                    # Gérer les anciens codes (12 chars: PPVVVNNNNNNNG) et nouveaux (10 chars: PPVVVNNNNNG)
                    # Extraire tous les chiffres entre la position 5 et le dernier caractère (genre)
                    if len(talent.unique_code) >= 10:
                        # Extraire la partie numérique (entre ville et genre)
                        # Pour ancien format (12 chars): position 5-11 (6 chiffres)
                        # Pour nouveau format (10 chars): position 5-9 (4 chiffres)
                        numeric_part = talent.unique_code[5:-1]  # Tout sauf le genre à la fin
                        # Ne garder que les chiffres
                        sequence_num = int(''.join(c for c in numeric_part if c.isdigit()))
                        max_sequence = max(max_sequence, sequence_num)
                except (ValueError, IndexError):
                    continue
    
    next_number = max_sequence + 1
    
    # Formatter le numéro sur 4 chiffres
    sequence = str(next_number).zfill(4)
    
    # Construire le code final: PPVVVNNNNNG
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
