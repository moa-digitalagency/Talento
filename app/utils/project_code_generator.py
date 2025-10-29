"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

"""
Générateur de codes uniques pour les talents assignés aux projets.
Format: CCIII001001 (sans tirets, minimum 10 caractères)
  - CC: Code pays (2 lettres)
  - III: Initiales de la boîte de production (2-3 lettres)
  - 001: ID du projet (3 chiffres)
  - 001: Numéro séquentiel du talent (3 chiffres)
Exemple: MAABC001001 = Maroc, ABC Productions, projet 1, talent 1
"""
from app.models.project import ProjectTalent
from app.data.world_countries import WORLD_COUNTRIES

def get_country_code_from_nationality(nationality):
    """Récupère le code pays ISO depuis la nationalité"""
    if not nationality:
        return "XX"  # Code par défaut si pas de pays
    
    # Chercher dans WORLD_COUNTRIES
    for country in WORLD_COUNTRIES:
        if country['nationality'] == nationality:
            return country['code']
    
    return "XX"  # Code par défaut si non trouvé

def get_production_initials(production_name):
    """Génère des initiales à partir du nom de la boîte de production"""
    if not production_name:
        return "XXX"
    
    # Supprimer les mots communs et articles
    stop_words = ['de', 'la', 'le', 'les', 'des', 'du', 'et', 'production', 'productions', 'studio', 'studios', 'films']
    
    # Nettoyer et splitter
    words = production_name.strip().split()
    meaningful_words = [w for w in words if w.lower() not in stop_words]
    
    if not meaningful_words:
        meaningful_words = words  # Si tous les mots sont filtrés, utiliser tous
    
    # Générer les initiales
    if len(meaningful_words) == 1:
        # Un seul mot: prendre les 3 premières lettres
        initials = meaningful_words[0][:3].upper()
    elif len(meaningful_words) == 2:
        # Deux mots: première lettre de chaque + deuxième lettre du premier
        initials = (meaningful_words[0][0] + meaningful_words[0][1] + meaningful_words[1][0]).upper()
    else:
        # Trois mots ou plus: première lettre des 3 premiers
        initials = ''.join([w[0] for w in meaningful_words[:3]]).upper()
    
    # S'assurer qu'on a au moins 2 lettres et au plus 3
    if len(initials) < 2:
        initials = initials.ljust(2, 'X')
    elif len(initials) > 3:
        initials = initials[:3]
    
    return initials

def generate_project_talent_code(project):
    """
    Génère un code unique pour un talent assigné à un projet
    Format: CCIII001001 (minimum 10 caractères, sans tirets)
      - CC: Code pays (2 lettres)
      - III: Initiales de production (2-3 lettres)
      - 001: ID projet (3 chiffres)
      - 001: Numéro séquentiel (3 chiffres)
    
    Args:
        project: Objet Project avec origin_country et production_company
    
    Returns:
        str: Code unique généré (ex: MAABC001001)
    """
    # 1. Récupérer le code pays (2 lettres)
    country_code = get_country_code_from_nationality(project.origin_country)
    
    # 2. Récupérer les initiales de la production (2-3 lettres)
    production_name = None
    if project.production_company:
        production_name = project.production_company.name
    
    production_initials = get_production_initials(production_name)
    
    # 3. ID du projet (3 chiffres)
    project_id_str = str(project.id).zfill(3)
    
    # 4. Compter le nombre de talents déjà assignés au projet
    existing_count = ProjectTalent.query.filter_by(project_id=project.id).count()
    next_number = existing_count + 1
    talent_number_str = str(next_number).zfill(3)
    
    # 5. Construire le code final (sans tirets)
    code = f"{country_code}{production_initials}{project_id_str}{talent_number_str}"
    
    # 6. Vérifier l'unicité (au cas où il y aurait un doublon)
    while ProjectTalent.query.filter_by(project_code=code).first():
        next_number += 1
        talent_number_str = str(next_number).zfill(3)
        code = f"{country_code}{production_initials}{project_id_str}{talent_number_str}"
    
    return code
