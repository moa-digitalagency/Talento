"""
Script d'initialisation des données essentielles
Charge les pays, villes et catégories de talents dans la base de données
Peut être exécuté après la migration ou manuellement
"""

import os
import sys

os.environ['SKIP_AUTO_MIGRATION'] = '1'

from app import create_app, db
from app.models.location import Country, City
from app.models.talent import Talent
from app.data.world_countries import WORLD_COUNTRIES
from app.data.world_cities import WORLD_CITIES
from app.constants import TALENT_CATEGORIES

def load_countries():
    """Charge tous les pays du monde"""
    print("\n🌍 Chargement des pays...")
    added = 0
    updated = 0
    
    for country_data in WORLD_COUNTRIES:
        country = Country.query.filter_by(code=country_data['code']).first()
        
        if country:
            if country.name != country_data['name']:
                country.name = country_data['name']
                updated += 1
        else:
            country = Country(
                name=country_data['name'],
                code=country_data['code']
            )
            db.session.add(country)
            added += 1
    
    try:
        db.session.commit()
        print(f"✅ Pays: {added} ajoutés, {updated} mis à jour")
        total = Country.query.count()
        print(f"   Total: {total} pays dans la base de données")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur lors du chargement des pays: {e}")
        return False

def load_cities():
    """Charge toutes les villes par pays"""
    print("\n🏙️  Chargement des villes...")
    added = 0
    skipped = 0
    
    for country_code, cities_list in WORLD_CITIES.items():
        country = Country.query.filter_by(code=country_code).first()
        
        if not country:
            print(f"⚠️  Pays {country_code} introuvable, villes ignorées")
            skipped += len(cities_list)
            continue
        
        for city_name in cities_list:
            city_code = city_name[:3].upper().replace(' ', '').replace('-', '')
            
            city = City.query.filter(
                City.name == city_name,
                City.country_id == country.id
            ).first()
            
            if not city:
                city = City(
                    name=city_name,
                    code=f"{country_code}{city_code}",
                    country_id=country.id
                )
                db.session.add(city)
                added += 1
    
    try:
        db.session.commit()
        print(f"✅ Villes: {added} ajoutées, {skipped} ignorées")
        total = City.query.count()
        print(f"   Total: {total} villes dans la base de données")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur lors du chargement des villes: {e}")
        return False

def load_talents():
    """Charge toutes les catégories de talents"""
    print("\n✨ Chargement des catégories de talents...")
    added = 0
    updated = 0
    
    for category in TALENT_CATEGORIES:
        category_name = category['name']
        category_emoji = category['emoji']
        
        for talent_name in category['talents']:
            talent = Talent.query.filter_by(name=talent_name).first()
            
            if talent:
                if talent.category != category_name or talent.emoji != category_emoji:
                    talent.category = category_name
                    talent.emoji = category_emoji
                    updated += 1
            else:
                talent = Talent(
                    name=talent_name,
                    category=category_name,
                    emoji=category_emoji
                )
                db.session.add(talent)
                added += 1
    
    try:
        db.session.commit()
        print(f"✅ Talents: {added} ajoutés, {updated} mis à jour")
        total = Talent.query.count()
        print(f"   Total: {total} talents dans la base de données")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur lors du chargement des talents: {e}")
        return False

def main():
    """Fonction principale"""
    print("="*70)
    print("🚀 INITIALISATION DES DONNÉES ESSENTIELLES")
    print("="*70)
    
    app = create_app()
    
    with app.app_context():
        countries_ok = load_countries()
        cities_ok = load_cities()
        talents_ok = load_talents()
        
        print("\n" + "="*70)
        if countries_ok and cities_ok and talents_ok:
            print("✅ CHARGEMENT TERMINÉ AVEC SUCCÈS!")
            
            countries_count = Country.query.count()
            cities_count = City.query.count()
            talents_count = Talent.query.count()
            
            print(f"\n📊 RÉSUMÉ:")
            print(f"   • {countries_count} pays")
            print(f"   • {cities_count} villes")
            print(f"   • {talents_count} talents")
        else:
            print("⚠️  CHARGEMENT INCOMPLET - Vérifiez les erreurs ci-dessus")
            sys.exit(1)
        
        print("="*70)

if __name__ == '__main__':
    main()
