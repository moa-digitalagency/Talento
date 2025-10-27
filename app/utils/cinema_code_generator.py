"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

"""
Générateur de code unique pour les talents CINEMA
Format: PPVVVNNNNNG (11 caractères)
- PP: Code pays ISO-2 (2 lettres)
- VVV: 3 premières lettres de la ville (en majuscules)
- NNNN: Numéro séquentiel (4 chiffres) - incrémenté par PAYS
- G: Genre (M/F)

Exemple: MACAS0001F (Maroc, Casablanca, 1ère personne au Maroc, Femme)

Important: Le compteur est global par pays, donc:
- MACAS0001F = 1ère personne enregistrée au Maroc (de Casablanca)
- MARAB0002M = 2ème personne enregistrée au Maroc (de Rabat)
- SNDAG0001F = 1ère personne enregistrée au Sénégal (de Dakar)
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
    import unicodedata
    city_clean = unicodedata.normalize('NFD', city_name)
    city_clean = ''.join(c for c in city_clean if unicodedata.category(c) != 'Mn')
    
    city_clean = re.sub(r'[^A-Za-z0-9]', '', city_clean)
    
    return city_clean[:3].upper().ljust(3, 'X')


def generate_cinema_unique_code(country_name, city_name, gender):
    """
    Générer un code unique pour un talent CINEMA
    
    Args:
        country_name (str): Nom du pays de résidence
        city_name (str): Nom de la ville de résidence
        gender (str): Genre (M/F)
    
    Returns:
        str: Code unique de 11 caractères (PPVVVNNNNNG)
    
    Format:
        - PP: Code pays (2 lettres, ex: MA pour Maroc)
        - VVV: Code ville (3 lettres, ex: CAS pour Casablanca)
        - NNNN: Numéro séquentiel (4 chiffres, incrémenté par PAYS)
        - G: Genre (M/F)
    
    Exemple: MACAS0001F
    
    Note:
        Le numéro séquentiel est incrémenté par PAYS uniquement, 
        pas par combinaison pays+ville. Ainsi:
        - MACAS0001F = 1ère personne au Maroc (de Casablanca)
        - MARAB0002M = 2ème personne au Maroc (de Rabat)
        - SNDAG0001F = 1ère personne au Sénégal (de Dakar)
        
        Cela permet de distinguer les talents CINEMA des talents réguliers qui
        utilisent le format PPGNNNNVVV.
    """
    # Obtenir le code pays (2 lettres)
    country_code = get_country_code(country_name)
    
    # Obtenir le code ville (3 lettres)
    city_code = clean_city_code(city_name)
    
    # Trouver le prochain numéro séquentiel pour ce PAYS uniquement
    # On cherche tous les codes qui commencent par le code pays (2 lettres)
    all_talents = CinemaTalent.query.filter(
        CinemaTalent.unique_code.like(f"{country_code}%")
    ).all()
    
    max_sequence = 0
    if all_talents:
        for talent in all_talents:
            if talent.unique_code:
                try:
                    # Format attendu: PPVVVNNNNNG (11 caractères)
                    # La partie numérique se trouve aux positions 5-9 (4 chiffres)
                    if len(talent.unique_code) >= 11:
                        numeric_part = talent.unique_code[5:9]
                        if numeric_part.isdigit():
                            sequence_num = int(numeric_part)
                            max_sequence = max(max_sequence, sequence_num)
                    # Rétrocompatibilité avec l'ancien format à 6 chiffres (PPVVVNNNNNNNG - 13 chars)
                    elif len(talent.unique_code) == 13:
                        numeric_part = talent.unique_code[5:11]
                        if numeric_part.isdigit():
                            sequence_num = int(numeric_part)
                            max_sequence = max(max_sequence, sequence_num)
                except (ValueError, IndexError):
                    continue
    
    next_number = max_sequence + 1
    
    # Formatter le numéro sur 4 chiffres
    sequence = str(next_number).zfill(4)
    
    # Construire le code final: PPVVVNNNNNG (11 caractères)
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
    from flask import current_app
    
    # En production, utiliser le domaine Replit
    base_url = current_app.config.get('BASE_URL', 'http://localhost:5004')
    return f"{base_url}/cinema/profile/{unique_code}"
