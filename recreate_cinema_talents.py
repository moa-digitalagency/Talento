#!/usr/bin/env python3
"""
Script pour supprimer et recréer les profils CINEMA de démonstration
avec les vraies valeurs d'ethnicités et types de talent
"""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.cinema_talent import CinemaTalent
from migrations_init import create_demo_cinema_talents

def main():
    app = create_app()
    
    with app.app_context():
        print("🗑️  Suppression de tous les profils CINEMA existants...")
        
        # Supprimer tous les talents CINEMA
        deleted_count = CinemaTalent.query.delete()
        db.session.commit()
        
        print(f"✅ {deleted_count} profils CINEMA supprimés")
        
        print("\n🎬 Recréation des profils CINEMA avec les vraies données...")
        
        # Recréer les profils de démonstration
        create_demo_cinema_talents()
        
        print("\n✅ Profils CINEMA recréés avec succès!")
        
        # Afficher les codes uniques créés
        talents = CinemaTalent.query.all()
        print(f"\n📋 {len(talents)} profils CINEMA créés:")
        for talent in talents:
            print(f"   - {talent.full_name}: {talent.unique_code}")

if __name__ == '__main__':
    main()
