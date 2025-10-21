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
from app.utils.qr_generator import generate_qr_code
from app.data.world_countries import WORLD_COUNTRIES
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
        'cv_analyzed_at': 'TIMESTAMP',
        'languages': 'VARCHAR(255)',
        'education': 'TEXT',
        'passport_number_encrypted': 'TEXT',
        'residence_card_encrypted': 'TEXT'
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
    """Remplir la table avec tous les pays du monde (195 pays reconnus)"""
    print("\n🌍 Initialisation de tous les pays du monde...")
    
    # Utiliser la liste complète des pays du monde
    countries_data = [{'name': c['name'], 'code': c['code']} for c in WORLD_COUNTRIES]
    
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
    """Remplir la table des villes marocaines - Liste complète triée alphabétiquement"""
    print("\n🏙️  Initialisation des villes marocaines...")
    
    cities_data = [
        {'name': 'Agadir', 'code': 'AGA'},
        {'name': 'Aïn Harrouda', 'code': 'AHR'},
        {'name': 'Al Hoceïma', 'code': 'HOC'},
        {'name': 'Asilah', 'code': 'ASI'},
        {'name': 'Azemmour', 'code': 'AZE'},
        {'name': 'Azrou', 'code': 'AZR'},
        {'name': 'Ben Guerir', 'code': 'BGU'},
        {'name': 'Béni Mellal', 'code': 'BEM'},
        {'name': 'Benslimane', 'code': 'BSL'},
        {'name': 'Berkane', 'code': 'BRK'},
        {'name': 'Berrechid', 'code': 'BER'},
        {'name': 'Boujdour', 'code': 'BJD'},
        {'name': 'Bouskoura', 'code': 'BOU'},
        {'name': 'Casablanca', 'code': 'CAS'},
        {'name': 'Chefchaouen', 'code': 'CHF'},
        {'name': 'Dakhla', 'code': 'DAK'},
        {'name': 'El Hajeb', 'code': 'EHJ'},
        {'name': 'El Jadida', 'code': 'ELJ'},
        {'name': 'El Kelaa des Sraghna', 'code': 'EKS'},
        {'name': 'Errachidia', 'code': 'ERR'},
        {'name': 'Essaouira', 'code': 'ESS'},
        {'name': 'Fès', 'code': 'FES'},
        {'name': 'Figuig', 'code': 'FIG'},
        {'name': 'Fnideq', 'code': 'FNI'},
        {'name': 'Guelmim', 'code': 'GUE'},
        {'name': 'Guercif', 'code': 'GCF'},
        {'name': 'Ifrane', 'code': 'IFR'},
        {'name': 'Imouzzer Kandar', 'code': 'IMK'},
        {'name': 'Inezgane', 'code': 'INE'},
        {'name': 'Jerada', 'code': 'JER'},
        {'name': 'Kelaat MGouna', 'code': 'KMG'},
        {'name': 'Kenitra', 'code': 'KEN'},
        {'name': 'Khémisset', 'code': 'KHE'},
        {'name': 'Khenifra', 'code': 'KHN'},
        {'name': 'Khouribga', 'code': 'KHO'},
        {'name': 'Ksar El Kébir', 'code': 'KSA'},
        {'name': 'Laâyoune', 'code': 'LAA'},
        {'name': 'Larache', 'code': 'LAR'},
        {'name': 'Marrakech', 'code': 'MAR'},
        {'name': 'Martil', 'code': 'MRT'},
        {'name': 'Mdiq', 'code': 'MDQ'},
        {'name': 'Meknès', 'code': 'MEK'},
        {'name': 'Midelt', 'code': 'MID'},
        {'name': 'Mohammedia', 'code': 'MOH'},
        {'name': 'Nador', 'code': 'NAD'},
        {'name': 'Nouaceur', 'code': 'NOU'},
        {'name': 'Oualidia', 'code': 'OAL'},
        {'name': 'Ouarzazate', 'code': 'OZZ'},
        {'name': 'Oued Zem', 'code': 'OZM'},
        {'name': 'Ouezzane', 'code': 'OUZ'},
        {'name': 'Oujda', 'code': 'OUJ'},
        {'name': 'Rabat', 'code': 'RAB'},
        {'name': 'Safi', 'code': 'SAF'},
        {'name': 'Salé', 'code': 'SAL'},
        {'name': 'Sefrou', 'code': 'SEF'},
        {'name': 'Settat', 'code': 'SET'},
        {'name': 'Sidi Bennour', 'code': 'SBN'},
        {'name': 'Sidi Ifni', 'code': 'SIF'},
        {'name': 'Sidi Kacem', 'code': 'SKC'},
        {'name': 'Sidi Slimane', 'code': 'SSL'},
        {'name': 'Skhirat', 'code': 'SKH'},
        {'name': 'Smara', 'code': 'SMA'},
        {'name': 'Tafraout', 'code': 'TAF'},
        {'name': 'Taghazout', 'code': 'TAG'},
        {'name': 'Tan-Tan', 'code': 'TAN'},
        {'name': 'Tanger', 'code': 'TNG'},
        {'name': 'Taourirt', 'code': 'TAO'},
        {'name': 'Tarfaya', 'code': 'TRF'},
        {'name': 'Taroudant', 'code': 'TRD'},
        {'name': 'Tata', 'code': 'TAT'},
        {'name': 'Taza', 'code': 'TAZ'},
        {'name': 'Témara', 'code': 'TEM'},
        {'name': 'Tétouan', 'code': 'TET'},
        {'name': 'Tiflet', 'code': 'TIF'},
        {'name': 'Tinghir', 'code': 'TGH'},
        {'name': 'Tiznit', 'code': 'TIZ'},
        {'name': 'Youssoufia', 'code': 'YOU'},
        {'name': 'Zagora', 'code': 'ZAG'},
        {'name': 'Zaïo', 'code': 'ZAI'},
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

def create_demo_users():
    """Créer 5 utilisateurs de démonstration (idempotent)"""
    print("\n👥 Vérification des utilisateurs de démonstration...")
    
    morocco = Country.query.filter_by(code='MA').first()
    casablanca = City.query.filter_by(code='CAS').first()
    rabat = City.query.filter_by(code='RAB').first()
    marrakech = City.query.filter_by(code='MAR').first()
    tanger = City.query.filter_by(code='TNG').first()
    
    if not morocco or not casablanca or not rabat:
        print("⚠️  Pays ou villes manquants, impossible de créer les démos")
        return False
    
    talent_dev_web = Talent.query.filter_by(name='Développement Web').first()
    talent_dev_mobile = Talent.query.filter_by(name='Développement Mobile').first()
    talent_graphisme = Talent.query.filter_by(name='Graphisme').first()
    talent_uiux = Talent.query.filter_by(name='UI/UX Design').first()
    talent_plomberie = Talent.query.filter_by(name='Plomberie').first()
    talent_electricite = Talent.query.filter_by(name='Électricité').first()
    talent_cuisine = Talent.query.filter_by(name='Cuisine').first()
    talent_patisserie = Talent.query.filter_by(name='Pâtisserie').first()
    talent_marketing = Talent.query.filter_by(name='Marketing digital').first()
    talent_seo = Talent.query.filter_by(name='SEO/SEA').first()
    
    demo_users = [
        {
            'email': 'demo1@talento.com',
            'unique_code': 'MACAS0002M',
            'first_name': 'Ahmed',
            'last_name': 'Bennani',
            'gender': 'M',
            'country_id': morocco.id,
            'city_id': casablanca.id,
            'date_of_birth': datetime(1990, 3, 15).date(),
            'phone': '+212661234567',
            'whatsapp': '+212661234567',
            'address': '15 Boulevard Zerktouni, Casablanca',
            'passport_number': 'ab123456',
            'residence_card': 'ma2024001234',
            'bio': 'Développeur web full-stack passionné avec 5 ans d\'expérience dans la création d\'applications web modernes. Spécialisé en React, Node.js et Python. J\'ai travaillé sur plus de 30 projets pour des clients internationaux.',
            'years_experience': 5,
            'availability': 'Temps plein',
            'work_mode': 'Hybride',
            'rate_range': '400-600 MAD/heure',
            'languages': 'Français,Anglais,Arabe,Darija',
            'education': 'Master en Informatique - ENSIAS',
            'linkedin': 'https://linkedin.com/in/ahmed-bennani-dev',
            'github': 'https://github.com/ahmedbennani',
            'twitter': 'https://twitter.com/ahmed_codes',
            'portfolio_url': 'https://ahmed-bennani.dev',
            'talents': [t.id for t in [talent_dev_web, talent_dev_mobile] if t]
        },
        {
            'email': 'demo2@talento.com',
            'unique_code': 'MARAB0002F',
            'first_name': 'Fatima',
            'last_name': 'El Amrani',
            'gender': 'F',
            'country_id': morocco.id,
            'city_id': rabat.id,
            'date_of_birth': datetime(1993, 7, 22).date(),
            'phone': '+212662345678',
            'whatsapp': '+212662345678',
            'address': '28 Avenue Mohammed V, Rabat',
            'passport_number': 'cd789012',
            'residence_card': 'ma2024005678',
            'bio': 'Designer graphique créative spécialisée en branding et identité visuelle. Portfolio comprenant des marques nationales et internationales. Passionnée par le design minimaliste et l\'impact visuel fort.',
            'years_experience': 3,
            'availability': 'Temps plein',
            'work_mode': 'À distance',
            'rate_range': '300-500 MAD/heure',
            'languages': 'Français,Anglais,Arabe,Darija',
            'education': 'École Supérieure des Beaux-Arts',
            'linkedin': 'https://linkedin.com/in/fatima-elamrani',
            'behance': 'https://behance.net/fatimaelamrani',
            'dribbble': 'https://dribbble.com/fatima_design',
            'instagram': 'https://instagram.com/fatima.design',
            'portfolio_url': 'https://fatima-elamrani.com',
            'talents': [t.id for t in [talent_graphisme, talent_uiux] if t]
        },
        {
            'email': 'demo3@talento.com',
            'unique_code': 'MACAS0003M',
            'first_name': 'Youssef',
            'last_name': 'Tazi',
            'gender': 'M',
            'country_id': morocco.id,
            'city_id': casablanca.id,
            'date_of_birth': datetime(1985, 11, 8).date(),
            'phone': '+212663456789',
            'whatsapp': '+212663456789',
            'address': '42 Rue des Oudayas, Casablanca',
            'passport_number': 'ef345678',
            'residence_card': 'ma2023009876',
            'bio': 'Plombier professionnel certifié avec 10 ans d\'expérience. Interventions rapides 24/7, spécialiste en installation sanitaire moderne, détection de fuites et rénovation complète. Plus de 500 chantiers réussis.',
            'years_experience': 10,
            'availability': 'Flexible',
            'work_mode': 'Sur site',
            'rate_range': '200-350 MAD/heure',
            'languages': 'Français,Arabe,Darija',
            'education': 'Formation professionnelle OFPPT',
            'facebook': 'https://facebook.com/youssef.tazi.plomberie',
            'whatsapp': '+212663456789',
            'talents': [t.id for t in [talent_plomberie, talent_electricite] if t]
        },
        {
            'email': 'demo4@talento.com',
            'unique_code': 'MARAB0003F',
            'first_name': 'Samira',
            'last_name': 'Chraibi',
            'gender': 'F',
            'country_id': morocco.id,
            'city_id': marrakech.id if marrakech else rabat.id,
            'date_of_birth': datetime(1988, 5, 30).date(),
            'phone': '+212664567890',
            'whatsapp': '+212664567890',
            'address': '7 Rue de la Kasbah, Marrakech',
            'passport_number': 'gh901234',
            'residence_card': 'ma2024011222',
            'bio': 'Chef de cuisine passionnée avec 7 ans d\'expérience en gastronomie française et marocaine. Spécialiste en pâtisserie fine et cuisine fusion. Diplômée Le Cordon Bleu Paris. Organisatrice d\'événements culinaires.',
            'years_experience': 7,
            'availability': 'Temps partiel',
            'work_mode': 'Sur site',
            'rate_range': '250-400 MAD/heure',
            'languages': 'Français,Anglais,Arabe,Darija',
            'education': 'Le Cordon Bleu Paris',
            'instagram': 'https://instagram.com/chef.samira',
            'facebook': 'https://facebook.com/chefsamirachraibi',
            'youtube': 'https://youtube.com/@ChefSamira',
            'tiktok': 'https://tiktok.com/@chef.samira',
            'talents': [t.id for t in [talent_cuisine, talent_patisserie] if t]
        },
        {
            'email': 'demo5@talento.com',
            'unique_code': 'MACAS0004M',
            'first_name': 'Omar',
            'last_name': 'Alaoui',
            'gender': 'M',
            'country_id': morocco.id,
            'city_id': tanger.id if tanger else casablanca.id,
            'date_of_birth': datetime(1992, 9, 12).date(),
            'phone': '+212665678901',
            'whatsapp': '+212665678901',
            'address': '33 Boulevard Pasteur, Tanger',
            'passport_number': 'ij567890',
            'residence_card': 'ma2024015544',
            'bio': 'Expert en marketing digital et SEO avec 4 ans d\'expérience. Spécialiste en croissance organique, publicité Google/Facebook, et stratégie de contenu. Résultats prouvés : +250% de trafic pour mes clients.',
            'years_experience': 4,
            'availability': 'Temps plein',
            'work_mode': 'À distance',
            'rate_range': '350-550 MAD/heure',
            'languages': 'Français,Anglais,Espagnol,Arabe,Darija',
            'education': 'MBA Digital Marketing',
            'linkedin': 'https://linkedin.com/in/omar-alaoui-seo',
            'twitter': 'https://twitter.com/omar_seo',
            'facebook': 'https://facebook.com/omar.alaoui.marketing',
            'instagram': 'https://instagram.com/omar.marketing',
            'portfolio_url': 'https://omar-alaoui-seo.com',
            'talents': [t.id for t in [talent_marketing, talent_seo] if t]
        }
    ]
    
    count = 0
    for demo_data in demo_users:
        existing = User.query.filter_by(email=demo_data['email']).first()
        if not existing:
            talents = demo_data.pop('talents')
            phone_val = demo_data.pop('phone', None)
            whatsapp_val = demo_data.pop('whatsapp', None)
            address_val = demo_data.pop('address', None)
            passport_val = demo_data.pop('passport_number', None)
            residence_val = demo_data.pop('residence_card', None)
            
            user = User(**demo_data)
            user.set_password('demo123')
            user.account_active = True
            
            if phone_val:
                user.phone = phone_val
            if whatsapp_val:
                user.whatsapp = whatsapp_val
            if address_val:
                user.address = address_val
            if passport_val:
                user.passport_number = passport_val
            if residence_val:
                user.residence_card = residence_val
            
            db.session.add(user)
            db.session.flush()
            
            for talent_id in talents:
                user_talent = UserTalent(user_id=user.id, talent_id=talent_id)
                db.session.add(user_talent)
            
            count += 1
    
    if count > 0:
        db.session.commit()
        print(f"✅ {count} nouveaux utilisateurs de démonstration créés")
    else:
        print("✅ Les utilisateurs de démonstration existent déjà")
    
    return True

def generate_qr_codes_for_users():
    """Générer les QR codes pour tous les utilisateurs qui n'en ont pas"""
    print("\n🔲 Génération des QR codes pour les utilisateurs...")
    
    users_without_qr = User.query.filter(User.qr_code_filename == None).all()
    
    if not users_without_qr:
        print("✅ Tous les utilisateurs ont déjà des QR codes")
        return True
    
    count = 0
    for user in users_without_qr:
        try:
            from flask import current_app
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
            qr_save_path = os.path.join(upload_folder, 'qrcodes')
            
            qr_filename = generate_qr_code(user.unique_code, qr_save_path)
            user.qr_code_filename = qr_filename
            count += 1
        except Exception as e:
            print(f"⚠️  Erreur lors de la génération du QR code pour {user.unique_code}: {e}")
    
    if count > 0:
        db.session.commit()
        print(f"✅ {count} QR codes générés avec succès")
    
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
            create_demo_users()
            generate_qr_codes_for_users()
            
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
