"""
Script pour supprimer toutes les données de démonstration et tous les talents
- Utilisateurs de démo
- Tous les utilisateurs normaux (sauf admin)
- Tous les talents CINEMA
- Toutes les productions
- Tous les projets
- Toutes les données de présence
- Fichiers uploads associés

GARDE:
- Compte admin
- Compétences/talents (table talents)
- Pays et villes
- Paramètres système
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, CinemaTalent, Production, Project, ProjectTalent
from app.models.attendance import Attendance
from sqlalchemy import text

def delete_file_if_exists(filepath):
    """Supprime un fichier s'il existe"""
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
            return True
    except Exception as e:
        print(f"⚠️  Erreur suppression fichier {filepath}: {e}")
    return False

def clean_all_data():
    """Supprime toutes les données de démonstration et tous les talents"""
    app = create_app()
    
    with app.app_context():
        print("🗑️  NETTOYAGE COMPLET DE TOUTES LES DONNÉES")
        print("=" * 60)
        
        # Confirmation de sécurité
        confirm = input("\n⚠️  ATTENTION: Cette opération va supprimer TOUTES les données (sauf admin, compétences, pays/villes).\n"
                       "Voulez-vous continuer? (tapez 'OUI SUPPRIMER TOUT' pour confirmer): ")
        
        if confirm != "OUI SUPPRIMER TOUT":
            print("❌ Opération annulée")
            return
        
        try:
            # 1. SUPPRIMER LES DONNÉES DE PRÉSENCE
            print("\n📋 Suppression des données de présence...")
            attendance_count = Attendance.query.count()
            if attendance_count > 0:
                Attendance.query.delete()
                db.session.commit()
                print(f"✅ {attendance_count} enregistrements de présence supprimés")
            else:
                print("✅ Aucune donnée de présence à supprimer")
            
            # 2. SUPPRIMER LES ASSIGNATIONS DE TALENTS AUX PROJETS
            print("\n🎬 Suppression des assignations de talents aux projets...")
            project_talent_count = ProjectTalent.query.count()
            if project_talent_count > 0:
                ProjectTalent.query.delete()
                db.session.commit()
                print(f"✅ {project_talent_count} assignations supprimées")
            else:
                print("✅ Aucune assignation à supprimer")
            
            # 3. SUPPRIMER TOUS LES PROJETS
            print("\n📽️  Suppression de tous les projets...")
            projects = Project.query.all()
            project_count = len(projects)
            if project_count > 0:
                Project.query.delete()
                db.session.commit()
                print(f"✅ {project_count} projets supprimés")
            else:
                print("✅ Aucun projet à supprimer")
            
            # 4. SUPPRIMER TOUTES LES PRODUCTIONS
            print("\n🏢 Suppression de toutes les productions...")
            productions = Production.query.all()
            production_count = len(productions)
            if production_count > 0:
                Production.query.delete()
                db.session.commit()
                print(f"✅ {production_count} productions supprimées")
            else:
                print("✅ Aucune production à supprimer")
            
            # 5. SUPPRIMER TOUS LES TALENTS CINEMA + LEURS FICHIERS
            print("\n🎭 Suppression de tous les talents CINEMA...")
            cinema_talents = CinemaTalent.query.all()
            cinema_count = len(cinema_talents)
            
            if cinema_count > 0:
                files_deleted = 0
                for talent in cinema_talents:
                    # Supprimer les photos
                    if talent.profile_photo_filename:
                        filepath = os.path.join('app', 'static', 'uploads', 'photos', talent.profile_photo_filename)
                        if delete_file_if_exists(filepath):
                            files_deleted += 1
                    
                    if talent.id_photo_filename:
                        filepath = os.path.join('app', 'static', 'uploads', 'photos', talent.id_photo_filename)
                        if delete_file_if_exists(filepath):
                            files_deleted += 1
                    
                    # Supprimer le QR code
                    if talent.unique_code:
                        qr_filepath = os.path.join('app', 'static', 'uploads', 'qrcodes', f'{talent.unique_code}.png')
                        if delete_file_if_exists(qr_filepath):
                            files_deleted += 1
                
                CinemaTalent.query.delete()
                db.session.commit()
                print(f"✅ {cinema_count} talents CINEMA supprimés")
                print(f"✅ {files_deleted} fichiers supprimés")
            else:
                print("✅ Aucun talent CINEMA à supprimer")
            
            # 6. SUPPRIMER TOUS LES UTILISATEURS (SAUF ADMIN)
            print("\n👥 Suppression de tous les utilisateurs (sauf admin)...")
            
            # Supprimer les relations user_talents d'abord
            db.session.execute(text("DELETE FROM user_talents WHERE user_id IN (SELECT id FROM users WHERE is_admin = FALSE)"))
            
            # Récupérer tous les utilisateurs non-admin
            users = User.query.filter_by(is_admin=False).all()
            user_count = len(users)
            
            if user_count > 0:
                files_deleted = 0
                for user in users:
                    # Supprimer la photo de profil
                    if user.photo_filename:
                        filepath = os.path.join('app', 'static', 'uploads', 'photos', user.photo_filename)
                        if delete_file_if_exists(filepath):
                            files_deleted += 1
                    
                    # Supprimer le CV
                    if user.cv_filename:
                        filepath = os.path.join('app', 'static', 'uploads', 'cvs', user.cv_filename)
                        if delete_file_if_exists(filepath):
                            files_deleted += 1
                    
                    # Supprimer le QR code
                    if user.unique_code:
                        qr_filepath = os.path.join('app', 'static', 'uploads', 'qrcodes', f'{user.unique_code}.png')
                        if delete_file_if_exists(qr_filepath):
                            files_deleted += 1
                
                User.query.filter_by(is_admin=False).delete()
                db.session.commit()
                print(f"✅ {user_count} utilisateurs supprimés")
                print(f"✅ {files_deleted} fichiers supprimés")
            else:
                print("✅ Aucun utilisateur à supprimer")
            
            # 7. RÉINITIALISER LES COMPTEURS DE CODES UNIQUES (si la table existe)
            print("\n🔢 Réinitialisation des compteurs de codes uniques...")
            try:
                db.session.execute(text("DELETE FROM id_counters"))
                db.session.commit()
                print("✅ Compteurs réinitialisés")
            except Exception as e:
                db.session.rollback()  # IMPORTANT: Réinitialiser la transaction en échec
                if "does not exist" in str(e):
                    print("✅ Table id_counters n'existe pas (normal)")
                else:
                    print(f"⚠️  Erreur lors de la réinitialisation: {e}")
            
            print("\n" + "=" * 60)
            print("✅ NETTOYAGE COMPLET TERMINÉ")
            print("\n📊 RÉSUMÉ:")
            print(f"   - {attendance_count} enregistrements de présence supprimés")
            print(f"   - {project_talent_count} assignations de talents supprimées")
            print(f"   - {project_count} projets supprimés")
            print(f"   - {production_count} productions supprimées")
            print(f"   - {cinema_count} talents CINEMA supprimés")
            print(f"   - {user_count} utilisateurs supprimés")
            print("\n💾 DONNÉES CONSERVÉES:")
            print("   - Compte(s) admin")
            print("   - Compétences/talents (table talents)")
            print("   - Pays et villes")
            print("   - Paramètres système")
            print("\n🎉 La base de données est maintenant propre!")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Erreur lors du nettoyage: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    clean_all_data()
