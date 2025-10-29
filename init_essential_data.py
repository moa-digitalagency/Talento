#!/usr/bin/env python
"""
Script d'initialisation rapide des données essentielles
Charge tous les pays, villes et talents dans la base de données

Usage:
    python init_essential_data.py
    
Ce script peut être lancé à tout moment pour corriger les données manquantes.
"""

import os
import sys

os.environ['SKIP_AUTO_MIGRATION'] = '1'

from app import create_app, db
from app.models.location import Country, City
from app.models.talent import Talent
from app.data.world_countries import WORLD_COUNTRIES

def init_countries():
    """Initialiser tous les pays du monde (195 pays)"""
    print("\n🌍 Chargement de tous les pays du monde...")
    
    countries_data = [{'name': c['name'], 'code': c['code']} for c in WORLD_COUNTRIES]
    
    added = 0
    for data in countries_data:
        if not Country.query.filter_by(code=data['code']).first():
            country = Country(**data)
            db.session.add(country)
            added += 1
    
    db.session.commit()
    total = Country.query.count()
    print(f"✅ {added} nouveaux pays ajoutés (Total: {total} pays)")
    return total

def init_cities():
    """Initialiser les villes principales du monde"""
    from app.data.world_cities import WORLD_CITIES
    
    print("\n🏙️  Chargement des villes du monde...")
    
    added = 0
    total_cities = 0
    
    for country_code, cities_list in WORLD_CITIES.items():
        country = Country.query.filter_by(code=country_code).first()
        
        if not country:
            continue
        
        for city_name in cities_list:
            total_cities += 1
            city_code = f"{country_code}-{total_cities:03d}"
            
            existing = City.query.filter_by(name=city_name, country_id=country.id).first()
            
            if not existing:
                city = City(
                    name=city_name,
                    code=city_code,
                    country_id=country.id
                )
                db.session.add(city)
                added += 1
    
    db.session.commit()
    total = City.query.count()
    print(f"✅ {added} nouvelles villes ajoutées (Total: {total} villes)")
    return total

def init_talents():
    """Initialiser la liste complète des talents"""
    print("\n⭐ Chargement de tous les talents...")
    
    talents_data = [
        {'name': 'Acteur/Actrice', 'emoji': '🎭', 'category': 'Cinéma'},
        {'name': 'Cascadeur/Cascadeuse', 'emoji': '🤸', 'category': 'Cinéma'},
        {'name': 'Chorégraphe', 'emoji': '💃', 'category': 'Cinéma'},
        {'name': 'Chanteur/Chanteuse', 'emoji': '🎤', 'category': 'Cinéma'},
        {'name': 'Danseur/Danseuse', 'emoji': '🕺', 'category': 'Cinéma'},
        {'name': 'Musicien/Musicienne', 'emoji': '🎸', 'category': 'Cinéma'},
        {'name': 'Mannequin', 'emoji': '👗', 'category': 'Cinéma'},
        {'name': 'Figurant/Figurante', 'emoji': '👥', 'category': 'Cinéma'},
        {'name': 'Doublure', 'emoji': '🎬', 'category': 'Cinéma'},
        {'name': 'Comédien de voix', 'emoji': '🗣️', 'category': 'Cinéma'},
        
        {'name': 'Réalisateur/Réalisatrice', 'emoji': '🎬', 'category': 'Production'},
        {'name': 'Assistant réalisateur', 'emoji': '📋', 'category': 'Production'},
        {'name': 'Scénariste', 'emoji': '✍️', 'category': 'Production'},
        {'name': 'Producteur/Productrice', 'emoji': '💼', 'category': 'Production'},
        {'name': 'Directeur de production', 'emoji': '📊', 'category': 'Production'},
        {'name': 'Régisseur général', 'emoji': '🏗️', 'category': 'Production'},
        {'name': 'Scripte', 'emoji': '📝', 'category': 'Production'},
        {'name': 'Directeur de casting', 'emoji': '🎯', 'category': 'Production'},
        
        {'name': 'Directeur de la photographie', 'emoji': '📸', 'category': 'Image'},
        {'name': 'Cadreur/Cadreuse', 'emoji': '📹', 'category': 'Image'},
        {'name': 'Chef opérateur', 'emoji': '🎥', 'category': 'Image'},
        {'name': 'Assistant caméra', 'emoji': '🎬', 'category': 'Image'},
        {'name': 'Steadicam', 'emoji': '🎦', 'category': 'Image'},
        {'name': 'Opérateur drone', 'emoji': '🚁', 'category': 'Image'},
        {'name': 'Photographe de plateau', 'emoji': '📷', 'category': 'Image'},
        {'name': 'Étalonnage coloriste', 'emoji': '🎨', 'category': 'Image'},
        
        {'name': 'Chef électricien', 'emoji': '💡', 'category': 'Lumière'},
        {'name': 'Électricien', 'emoji': '⚡', 'category': 'Lumière'},
        {'name': 'Machiniste', 'emoji': '🔧', 'category': 'Lumière'},
        {'name': 'Grutier', 'emoji': '🏗️', 'category': 'Lumière'},
        
        {'name': 'Ingénieur du son', 'emoji': '🎙️', 'category': 'Son'},
        {'name': 'Perchman', 'emoji': '🎤', 'category': 'Son'},
        {'name': 'Mixeur son', 'emoji': '🎛️', 'category': 'Son'},
        {'name': 'Bruiteur', 'emoji': '🔊', 'category': 'Son'},
        {'name': 'Compositeur musique', 'emoji': '🎵', 'category': 'Son'},
        
        {'name': 'Monteur/Monteuse', 'emoji': '✂️', 'category': 'Post-production'},
        {'name': 'Assistant monteur', 'emoji': '🎞️', 'category': 'Post-production'},
        {'name': 'Monteur son', 'emoji': '🔉', 'category': 'Post-production'},
        {'name': 'Superviseur VFX', 'emoji': '🌟', 'category': 'Post-production'},
        {'name': 'Infographiste 3D', 'emoji': '🖥️', 'category': 'Post-production'},
        {'name': 'Animateur 2D/3D', 'emoji': '🎨', 'category': 'Post-production'},
        
        {'name': 'Chef décorateur', 'emoji': '🎨', 'category': 'Décors'},
        {'name': 'Accessoiriste', 'emoji': '🛠️', 'category': 'Décors'},
        {'name': 'Ensemblier', 'emoji': '🪑', 'category': 'Décors'},
        {'name': 'Constructeur décors', 'emoji': '🔨', 'category': 'Décors'},
        {'name': 'Peintre décorateur', 'emoji': '🖌️', 'category': 'Décors'},
        
        {'name': 'Chef costumier', 'emoji': '👔', 'category': 'Costumes'},
        {'name': 'Costumier/Costumière', 'emoji': '👗', 'category': 'Costumes'},
        {'name': 'Couturier/Couturière', 'emoji': '🧵', 'category': 'Costumes'},
        {'name': 'Habilleur/Habilleuse', 'emoji': '👕', 'category': 'Costumes'},
        
        {'name': 'Chef maquilleur', 'emoji': '💄', 'category': 'Maquillage/Coiffure'},
        {'name': 'Maquilleur/Maquilleuse', 'emoji': '💅', 'category': 'Maquillage/Coiffure'},
        {'name': 'Maquilleur effets spéciaux', 'emoji': '🎭', 'category': 'Maquillage/Coiffure'},
        {'name': 'Coiffeur/Coiffeuse', 'emoji': '💇', 'category': 'Maquillage/Coiffure'},
        
        {'name': 'Régisseur général', 'emoji': '📋', 'category': 'Régie'},
        {'name': 'Régisseur extérieur', 'emoji': '🌍', 'category': 'Régie'},
        {'name': 'Responsable des repérages', 'emoji': '🗺️', 'category': 'Régie'},
        {'name': 'Chef de plateau', 'emoji': '🎬', 'category': 'Régie'},
        
        {'name': 'Chauffeur', 'emoji': '🚗', 'category': 'Transport/Logistique'},
        {'name': 'Coordinateur transport', 'emoji': '🚚', 'category': 'Transport/Logistique'},
        {'name': 'Responsable logistique', 'emoji': '📦', 'category': 'Transport/Logistique'},
        
        {'name': 'Traiteur', 'emoji': '🍽️', 'category': 'Restauration'},
        {'name': 'Chef cuisinier', 'emoji': '👨‍🍳', 'category': 'Restauration'},
        
        {'name': 'Agent de sécurité', 'emoji': '🛡️', 'category': 'Sécurité'},
        {'name': 'Coordinateur sécurité', 'emoji': '👮', 'category': 'Sécurité'},
        {'name': 'Coordinateur cascades', 'emoji': '🎯', 'category': 'Sécurité'},
        
        {'name': 'Dresseur animalier', 'emoji': '🐕', 'category': 'Spécialités'},
        {'name': 'Coordinateur animalier', 'emoji': '🦁', 'category': 'Spécialités'},
        {'name': 'Coach dialogue', 'emoji': '💬', 'category': 'Spécialités'},
        {'name': 'Consultant technique', 'emoji': '🎓', 'category': 'Spécialités'},
        {'name': 'Traducteur/Interprète', 'emoji': '🌐', 'category': 'Spécialités'},
    ]
    
    added = 0
    for data in talents_data:
        if not Talent.query.filter_by(name=data['name']).first():
            talent = Talent(**data)
            db.session.add(talent)
            added += 1
    
    db.session.commit()
    total = Talent.query.count()
    print(f"✅ {added} nouveaux talents ajoutés (Total: {total} talents)")
    return total

def main():
    """Fonction principale"""
    try:
        app = create_app()
    except Exception as e:
        print(f"\n❌ ERREUR lors de la création de l'application: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    with app.app_context():
        print("="*70)
        print("🚀 INITIALISATION DES DONNÉES ESSENTIELLES")
        print("="*70)
        
        try:
            db.create_all()
            print("✅ Tables de base de données vérifiées")
            
            countries_count = init_countries()
            cities_count = init_cities()
            talents_count = init_talents()
            
            print("\n" + "="*70)
            print("✅ INITIALISATION TERMINÉE AVEC SUCCÈS!")
            print("="*70)
            print(f"📊 Résumé:")
            print(f"   • Pays: {countries_count}")
            print(f"   • Villes: {cities_count}")
            print(f"   • Talents: {talents_count}")
            print("="*70)
            
            return 0
            
        except Exception as e:
            print(f"\n❌ ERREUR lors de l'initialisation: {e}")
            import traceback
            traceback.print_exc()
            return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
