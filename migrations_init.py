#!/usr/bin/env python
"""
Script de migration et initialisation de la base de données
Ce script vérifie et corrige la structure de la base de données automatiquement
"""
import os
import sys
from app import create_app, db
from app.models.user import User
from app.models.talent import Talent, UserTalent
from app.models.location import Country, City
from sqlalchemy import inspect, text
from datetime import datetime

def check_and_create_tables():
    """Vérifie et crée les tables manquantes"""
    print("🔍 Vérification de la structure de la base de données...")
    
    inspector = inspect(db.engine)
    existing_tables = inspector.get_table_names()
    
    required_tables = ['users', 'talents', 'user_talents', 'countries', 'cities']
    missing_tables = [table for table in required_tables if table not in existing_tables]
    
    if missing_tables:
        print(f"⚠️  Tables manquantes détectées: {', '.join(missing_tables)}")
        print("📝 Création des tables manquantes...")
        db.create_all()
        print("✅ Tables créées avec succès")
    else:
        print("✅ Toutes les tables existent")
    
    return True

def check_and_add_columns():
    """Vérifie et ajoute les colonnes manquantes"""
    print("\n🔍 Vérification des colonnes...")
    
    inspector = inspect(db.engine)
    
    user_columns_to_check = {
        'availability': 'VARCHAR(50)',
        'work_mode': 'VARCHAR(50)', 
        'rate_range': 'VARCHAR(100)',
        'profile_score': 'INTEGER DEFAULT 0',
        'cv_analysis': 'TEXT',
        'cv_analyzed_at': 'TIMESTAMP'
    }
    
    if 'users' in inspector.get_table_names():
        existing_columns = [col['name'] for col in inspector.get_columns('users')]
        
        for col_name, col_type in user_columns_to_check.items():
            if col_name not in existing_columns:
                print(f"➕ Ajout de la colonne users.{col_name}...")
                try:
                    with db.engine.connect() as conn:
                        conn.execute(text(f'ALTER TABLE users ADD COLUMN {col_name} {col_type}'))
                        conn.commit()
                    print(f"✅ Colonne {col_name} ajoutée")
                except Exception as e:
                    print(f"⚠️  Colonne {col_name} existe déjà ou erreur: {e}")
    
    print("✅ Vérification des colonnes terminée")
    return True

def seed_countries():
    """Remplir la table des pays africains"""
    print("\n🌍 Initialisation des pays africains...")
    
    countries_data = [
        {'name': 'Maroc', 'code': 'MA'},
        {'name': 'Algérie', 'code': 'DZ'},
        {'name': 'Tunisie', 'code': 'TN'},
        {'name': 'Libye', 'code': 'LY'},
        {'name': 'Égypte', 'code': 'EG'},
        {'name': 'Mauritanie', 'code': 'MR'},
        {'name': 'Mali', 'code': 'ML'},
        {'name': 'Sénégal', 'code': 'SN'},
        {'name': 'Gambie', 'code': 'GM'},
        {'name': 'Guinée-Bissau', 'code': 'GW'},
        {'name': 'Guinée', 'code': 'GN'},
        {'name': 'Sierra Leone', 'code': 'SL'},
        {'name': 'Liberia', 'code': 'LR'},
        {'name': "Côte d'Ivoire", 'code': 'CI'},
        {'name': 'Ghana', 'code': 'GH'},
        {'name': 'Togo', 'code': 'TG'},
        {'name': 'Bénin', 'code': 'BJ'},
        {'name': 'Nigéria', 'code': 'NG'},
        {'name': 'Niger', 'code': 'NE'},
        {'name': 'Burkina Faso', 'code': 'BF'},
        {'name': 'Cameroun', 'code': 'CM'},
        {'name': 'Tchad', 'code': 'TD'},
        {'name': 'République Centrafricaine', 'code': 'CF'},
        {'name': 'Guinée Équatoriale', 'code': 'GQ'},
        {'name': 'Gabon', 'code': 'GA'},
        {'name': 'Congo', 'code': 'CG'},
        {'name': 'RD Congo', 'code': 'CD'},
        {'name': 'Angola', 'code': 'AO'},
        {'name': 'Soudan', 'code': 'SD'},
        {'name': 'Soudan du Sud', 'code': 'SS'},
        {'name': 'Éthiopie', 'code': 'ET'},
        {'name': 'Érythrée', 'code': 'ER'},
        {'name': 'Djibouti', 'code': 'DJ'},
        {'name': 'Somalie', 'code': 'SO'},
        {'name': 'Kenya', 'code': 'KE'},
        {'name': 'Ouganda', 'code': 'UG'},
        {'name': 'Rwanda', 'code': 'RW'},
        {'name': 'Burundi', 'code': 'BI'},
        {'name': 'Tanzanie', 'code': 'TZ'},
        {'name': 'Malawi', 'code': 'MW'},
        {'name': 'Mozambique', 'code': 'MZ'},
        {'name': 'Zimbabwe', 'code': 'ZW'},
        {'name': 'Zambie', 'code': 'ZM'},
        {'name': 'Botswana', 'code': 'BW'},
        {'name': 'Namibie', 'code': 'NA'},
        {'name': 'Afrique du Sud', 'code': 'ZA'},
        {'name': 'Lesotho', 'code': 'LS'},
        {'name': 'Eswatini', 'code': 'SZ'},
        {'name': 'Madagascar', 'code': 'MG'},
        {'name': 'Maurice', 'code': 'MU'},
        {'name': 'Comores', 'code': 'KM'},
        {'name': 'Seychelles', 'code': 'SC'},
        {'name': 'Cap-Vert', 'code': 'CV'},
        {'name': 'São Tomé-et-Príncipe', 'code': 'ST'},
    ]
    
    count = 0
    for data in countries_data:
        if not Country.query.filter_by(code=data['code']).first():
            country = Country(**data)
            db.session.add(country)
            count += 1
    
    db.session.commit()
    print(f"✅ {count} nouveaux pays ajoutés ({len(countries_data)} total)")
    return True

def seed_cities():
    """Remplir la table des villes marocaines"""
    print("\n🏙️  Initialisation des villes marocaines...")
    
    cities_data = [
        {'name': 'Rabat', 'code': 'RAB'},
        {'name': 'Casablanca', 'code': 'CAS'},
        {'name': 'Tanger', 'code': 'TNG'},
        {'name': 'Marrakech', 'code': 'MAR'},
        {'name': 'Fès', 'code': 'FES'},
        {'name': 'Agadir', 'code': 'AGA'},
        {'name': 'Meknès', 'code': 'MEK'},
        {'name': 'Oujda', 'code': 'OUJ'},
        {'name': 'Tétouan', 'code': 'TET'},
        {'name': 'Salé', 'code': 'SAL'},
        {'name': 'Kenitra', 'code': 'KEN'},
        {'name': 'El Jadida', 'code': 'ELJ'},
    ]
    
    count = 0
    for data in cities_data:
        if not City.query.filter_by(code=data['code']).first():
            city = City(**data)
            db.session.add(city)
            count += 1
    
    db.session.commit()
    print(f"✅ {count} nouvelles villes ajoutées ({len(cities_data)} total)")
    return True

def seed_talents():
    """Remplir la table des talents"""
    print("\n⭐ Initialisation des talents...")
    
    talents_data = [
        {'name': 'Maçonnerie', 'emoji': '🧱', 'category': 'Construction'},
        {'name': 'Carrelage', 'emoji': '⬜', 'category': 'Construction'},
        {'name': 'Plomberie', 'emoji': '🔧', 'category': 'Construction'},
        {'name': 'Électricité', 'emoji': '⚡', 'category': 'Construction'},
        {'name': 'Menuiserie', 'emoji': '🪚', 'category': 'Construction'},
        {'name': 'Peinture', 'emoji': '🎨', 'category': 'Construction'},
        {'name': 'Soudure', 'emoji': '🔥', 'category': 'Construction'},
        {'name': 'Ferronnerie', 'emoji': '⚒️', 'category': 'Construction'},
        {'name': 'Charpenterie', 'emoji': '🪵', 'category': 'Construction'},
        {'name': 'Toiture', 'emoji': '🏠', 'category': 'Construction'},
        {'name': 'Isolation', 'emoji': '🧰', 'category': 'Construction'},
        {'name': 'Climatisation', 'emoji': '❄️', 'category': 'Construction'},
        {'name': 'Cuisine', 'emoji': '🍳', 'category': 'Restauration'},
        {'name': 'Pâtisserie', 'emoji': '🧁', 'category': 'Restauration'},
        {'name': 'Boulangerie', 'emoji': '🥖', 'category': 'Restauration'},
        {'name': 'Serveur', 'emoji': '🍽️', 'category': 'Restauration'},
        {'name': 'Barista', 'emoji': '☕', 'category': 'Restauration'},
        {'name': 'Chef cuisine', 'emoji': '👨\u200d🍳', 'category': 'Restauration'},
        {'name': 'Développement Web', 'emoji': '🖥️', 'category': 'Technologie'},
        {'name': 'Développement Mobile', 'emoji': '📱', 'category': 'Technologie'},
        {'name': 'Data Science', 'emoji': '📊', 'category': 'Technologie'},
        {'name': 'IA/ML', 'emoji': '🤖', 'category': 'Technologie'},
        {'name': 'Cybersécurité', 'emoji': '🔒', 'category': 'Technologie'},
        {'name': 'DevOps', 'emoji': '⚙️', 'category': 'Technologie'},
        {'name': 'Maintenance IT', 'emoji': '🔌', 'category': 'Technologie'},
        {'name': 'Réseaux', 'emoji': '🌐', 'category': 'Technologie'},
        {'name': 'Graphisme', 'emoji': '🎨', 'category': 'Créatif'},
        {'name': 'UI/UX Design', 'emoji': '✏️', 'category': 'Créatif'},
        {'name': 'Illustration', 'emoji': '🖌️', 'category': 'Créatif'},
        {'name': 'Animation 3D', 'emoji': '🎬', 'category': 'Créatif'},
        {'name': 'Motion Design', 'emoji': '🎞️', 'category': 'Créatif'},
        {'name': 'Photographie', 'emoji': '📷', 'category': 'Médias'},
        {'name': 'Vidéographie', 'emoji': '🎥', 'category': 'Médias'},
        {'name': 'Montage vidéo', 'emoji': '✂️', 'category': 'Médias'},
        {'name': 'Rédaction', 'emoji': '✍️', 'category': 'Médias'},
        {'name': 'Journalisme', 'emoji': '📰', 'category': 'Médias'},
        {'name': 'Community Management', 'emoji': '💬', 'category': 'Marketing'},
        {'name': 'SEO/SEA', 'emoji': '🔍', 'category': 'Marketing'},
        {'name': 'Marketing digital', 'emoji': '📈', 'category': 'Marketing'},
        {'name': 'Content Marketing', 'emoji': '📝', 'category': 'Marketing'},
        {'name': 'Email Marketing', 'emoji': '📧', 'category': 'Marketing'},
        {'name': 'Musique', 'emoji': '🎵', 'category': 'Artistique'},
        {'name': 'Chant', 'emoji': '🎤', 'category': 'Artistique'},
        {'name': 'Danse', 'emoji': '💃', 'category': 'Artistique'},
        {'name': 'Théâtre', 'emoji': '🎭', 'category': 'Artistique'},
        {'name': 'Mannequinat', 'emoji': '🕴️', 'category': 'Artistique'},
        {'name': 'Comédie', 'emoji': '😂', 'category': 'Artistique'},
        {'name': 'Ménage', 'emoji': '🧹', 'category': 'Services'},
        {'name': 'Jardinage', 'emoji': '🌱', 'category': 'Services'},
        {'name': "Garde d'enfants", 'emoji': '👶', 'category': 'Services'},
        {'name': 'Aide à domicile', 'emoji': '🏡', 'category': 'Services'},
        {'name': 'Coiffure', 'emoji': '💇', 'category': 'Services'},
        {'name': 'Esthétique', 'emoji': '💅', 'category': 'Services'},
        {'name': 'Chauffeur', 'emoji': '🚗', 'category': 'Transport'},
        {'name': 'Livreur', 'emoji': '📦', 'category': 'Transport'},
        {'name': 'Taxi', 'emoji': '🚕', 'category': 'Transport'},
        {'name': 'Enseignant', 'emoji': '👨\u200d🏫', 'category': 'Éducation'},
        {'name': 'Formation professionnelle', 'emoji': '📚', 'category': 'Éducation'},
        {'name': 'Cours particuliers', 'emoji': '📖', 'category': 'Éducation'},
        {'name': 'Coaching', 'emoji': '🎯', 'category': 'Éducation'},
        {'name': 'Infirmier', 'emoji': '💉', 'category': 'Santé'},
        {'name': 'Aide-soignant', 'emoji': '🩺', 'category': 'Santé'},
        {'name': 'Pharmacien', 'emoji': '💊', 'category': 'Santé'},
        {'name': 'Vente', 'emoji': '🛍️', 'category': 'Commerce'},
        {'name': 'Commerce', 'emoji': '🏪', 'category': 'Commerce'},
        {'name': 'Caissier', 'emoji': '💰', 'category': 'Commerce'},
        {'name': 'Organisation événements', 'emoji': '🎉', 'category': 'Événementiel'},
        {'name': 'Animation', 'emoji': '🎊', 'category': 'Événementiel'},
        {'name': 'DJ', 'emoji': '🎧', 'category': 'Événementiel'},
        {'name': 'Secrétariat', 'emoji': '📋', 'category': 'Bureautique'},
        {'name': 'Comptabilité', 'emoji': '🧮', 'category': 'Bureautique'},
        {'name': 'Ressources Humaines', 'emoji': '👥', 'category': 'Bureautique'},
        {'name': 'Gestion de projet', 'emoji': '📊', 'category': 'Bureautique'},
    ]
    
    count = 0
    for data in talents_data:
        if not Talent.query.filter_by(name=data['name']).first():
            talent = Talent(**data)
            db.session.add(talent)
            count += 1
    
    db.session.commit()
    print(f"✅ {count} nouveaux talents ajoutés ({len(talents_data)} total)")
    return True

def create_admin_user():
    """Créer le compte super admin (idempotent)"""
    print("\n👤 Vérification du compte admin...")
    
    admin_email = 'admin@talento.com'
    admin_code = 'MARAB0001N'
    
    admin = User.query.filter(
        (User.email == admin_email) | (User.unique_code == admin_code)
    ).first()
    
    if not admin:
        print("➕ Création du compte super admin...")
        
        admin_password = os.environ.get('ADMIN_PASSWORD', '@4dm1n')
        
        morocco = Country.query.filter_by(code='MA').first()
        rabat = City.query.filter_by(code='RAB').first()
        
        admin = User(
            email=admin_email,
            first_name='Admin',
            last_name='Talento',
            unique_code=admin_code,
            is_admin=True,
            account_active=True,
            country_id=morocco.id if morocco else None,
            city_id=rabat.id if rabat else None,
            gender='N'
        )
        admin.set_password(admin_password)
        admin.phone = '+212600000000'
        
        db.session.add(admin)
        
        try:
            db.session.commit()
            print(f"✅ Compte admin créé: {admin_email}")
            print(f"   Code unique: {admin_code}")
            print(f"   Mot de passe: {'[Variable ADMIN_PASSWORD]' if os.environ.get('ADMIN_PASSWORD') else '@4dm1n'}")
        except Exception as e:
            db.session.rollback()
            admin = User.query.filter(
                (User.email == admin_email) | (User.unique_code == admin_code)
            ).first()
            if admin:
                print(f"✅ Compte admin existe déjà (détecté après rollback): {admin.email}")
            else:
                print(f"⚠️  Erreur inattendue lors de la création admin: {e}")
                raise
    else:
        print(f"✅ Compte admin existe déjà: {admin.email}")
        if admin.email != admin_email or not admin.is_admin:
            admin.email = admin_email
            admin.is_admin = True
            try:
                db.session.commit()
                print("   ℹ️  Compte admin mis à jour")
            except Exception as e:
                db.session.rollback()
                print(f"   ⚠️  Impossible de mettre à jour: {e}")
    
    return True

def main():
    """Fonction principale d'initialisation"""
    print("=" * 60)
    print("🚀 INITIALISATION DE LA BASE DE DONNÉES TALENTO")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        try:
            check_and_create_tables()
            check_and_add_columns()
            seed_countries()
            seed_cities()
            seed_talents()
            create_admin_user()
            
            print("\n" + "=" * 60)
            print("✅ INITIALISATION TERMINÉE AVEC SUCCÈS")
            print("=" * 60)
            print(f"\n📊 Statistiques:")
            print(f"   - Pays: {Country.query.count()}")
            print(f"   - Villes: {City.query.count()}")
            print(f"   - Talents: {Talent.query.count()}")
            print(f"   - Utilisateurs: {User.query.count()}")
            print(f"\n🔐 Compte admin: admin@talento.com")
            print(f"   Mot de passe: {'[Variable ADMIN_PASSWORD]' if os.environ.get('ADMIN_PASSWORD') else '@4dm1n'}")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    main()
