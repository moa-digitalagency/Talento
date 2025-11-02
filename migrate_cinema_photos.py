"""
Script de migration pour copier les photos de profil des talents cinéma
depuis cinema_photos vers photos pour affichage dans le tableau principal

Usage: Assurez-vous que les variables d'environnement SECRET_KEY et ENCRYPTION_KEY sont définies
"""

import os
import sys

# Vérifier que les variables d'environnement requises sont définies
required_env_vars = ['SECRET_KEY', 'ENCRYPTION_KEY']
missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
if missing_vars:
    print(f"❌ Erreur: Les variables d'environnement suivantes doivent être définies: {', '.join(missing_vars)}")
    print("   Exécutez ce script avec les variables d'environnement requises.")
    sys.exit(1)

os.environ.setdefault('SKIP_AUTO_MIGRATION', '1')

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, CinemaTalent
from app.utils.file_handler import copy_file_between_folders

def migrate_cinema_photos():
    """Copier les photos de profil des talents cinéma existants"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Migration des photos de profil des talents cinéma...")
        
        # Récupérer tous les talents cinéma avec une photo de profil
        cinema_talents = CinemaTalent.query.filter(
            CinemaTalent.profile_photo_filename.isnot(None)
        ).all()
        
        print(f"📊 {len(cinema_talents)} talents cinéma avec photo de profil trouvés")
        
        success_count = 0
        error_count = 0
        
        for talent in cinema_talents:
            try:
                # Trouver l'utilisateur associé
                user = User.query.filter_by(unique_code=talent.unique_code).first()
                
                if not user:
                    print(f"⚠️  Utilisateur non trouvé pour {talent.unique_code}")
                    error_count += 1
                    continue
                
                # Copier le fichier en utilisant la fonction helper
                copy_success = copy_file_between_folders(
                    talent.profile_photo_filename,
                    'cinema_photos',
                    'photo'
                )
                
                if copy_success:
                    # Mettre à jour l'utilisateur
                    user.photo_filename = talent.profile_photo_filename
                    db.session.add(user)
                    
                    print(f"✅ Photo copiée pour {talent.first_name} {talent.last_name} ({talent.unique_code})")
                    success_count += 1
                else:
                    print(f"⚠️  Impossible de copier la photo pour {talent.unique_code}")
                    error_count += 1
                    
            except Exception as e:
                print(f"❌ Erreur pour {talent.unique_code}: {str(e)}")
                error_count += 1
        
        # Commit les changements
        try:
            db.session.commit()
            print(f"\n✅ Migration terminée!")
            print(f"   - {success_count} photos copiées avec succès")
            print(f"   - {error_count} erreurs")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Erreur lors du commit: {str(e)}")

if __name__ == '__main__':
    migrate_cinema_photos()
