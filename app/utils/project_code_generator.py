"""
Générateur de codes uniques pour les talents assignés aux projets.
Format: PRJ-[Project ID]-[Sequential Number] (ex: PRJ-001-001)
"""
from app.models.project import ProjectTalent

def generate_project_talent_code(project_id):
    """
    Génère un code unique pour un talent assigné à un projet
    Format: PRJ-XXX-YYY où XXX = ID projet, YYY = numéro séquentiel
    """
    # Compter le nombre de talents déjà assignés au projet
    existing_count = ProjectTalent.query.filter_by(project_id=project_id).count()
    
    # Générer le nouveau numéro séquentiel
    next_number = existing_count + 1
    
    # Formater le code
    code = f"PRJ-{str(project_id).zfill(3)}-{str(next_number).zfill(3)}"
    
    # Vérifier l'unicité (au cas où)
    while ProjectTalent.query.filter_by(project_code=code).first():
        next_number += 1
        code = f"PRJ-{str(project_id).zfill(3)}-{str(next_number).zfill(3)}"
    
    return code
