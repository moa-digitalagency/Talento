#!/usr/bin/env python
"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""


"""
Script pour régénérer les données CINEMA avec la nouvelle clé de chiffrement
"""
import os
os.environ.setdefault('FLASK_ENV', 'development')

from app import create_app, db
from app.models.cinema_talent import CinemaTalent
from app.utils.encryption import encrypt_sensitive_data
import json
from datetime import date

def fix_cinema_encryption():
    """Supprimer et recréer les profils CINEMA avec la nouvelle clé"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Suppression des anciens profils CINEMA...")
        CinemaTalent.query.delete()
        db.session.commit()
        print("✅ Anciens profils supprimés")
        
        print("\n🎬 Création de nouveaux profils CINEMA avec la nouvelle clé de chiffrement...")
        
        demo_cinema_talents = [
            {
                'first_name': 'Amina',
                'last_name': 'El Fassi',
                'gender': 'F',
                'date_of_birth': date(1995, 3, 15),
                'id_document_type': 'national_id',
                'id_document_number': 'AB123456',
                'ethnicities': json.dumps(['Arabe', 'Berbère']),
                'country_of_origin': 'Maroc',
                'nationality': 'Marocaine',
                'country_of_residence': 'Maroc',
                'city_of_residence': 'Casablanca',
                'languages_spoken': json.dumps(['Arabe', 'Français', 'Anglais', 'Amazigh (Tamazight)']),
                'eye_color': 'Marron',
                'hair_color': 'Noir',
                'hair_type': 'Ondulés',
                'height': 168,
                'skin_tone': 'Olive',
                'build': 'Athlétique',
                'talent_types': json.dumps(['Acteur/Actrice Principal(e)', 'Mannequin', 'Danseur/Danseuse de fond']),
                'other_talents': json.dumps(['Danse contemporaine', 'Yoga', 'Équitation']),
                'email': 'amina.elfassi@demo.cinema',
                'phone': '+212612345678',
                'whatsapp': '+212612345678',
                'website': 'https://aminaelfassi.com',
                'facebook': 'amina.elfassi.cinema',
                'instagram': '@amina_elfassi_official',
                'tiktok': '@amina_cinema',
                'youtube': 'Amina El Fassi',
                'telegram': '@amina_cinema',
                'imdb_url': 'https://imdb.com/name/nm1234567',
                'threads': '@amina_elfassi',
                'previous_productions': json.dumps([
                    {'title': 'Le Cœur de Casablanca', 'year': '2022', 'type': 'Film'},
                    {'title': 'Racines du Désert', 'year': '2021', 'type': 'Série TV'}
                ])
            },
            {
                'first_name': 'Julien',
                'last_name': 'Moreau',
                'gender': 'M',
                'date_of_birth': date(1988, 7, 22),
                'id_document_type': 'passport',
                'id_document_number': 'FR987654',
                'ethnicities': json.dumps(['Caucasienne/Blanche']),
                'country_of_origin': 'France',
                'nationality': 'Française',
                'country_of_residence': 'France',
                'city_of_residence': 'Paris',
                'languages_spoken': json.dumps(['Français', 'Anglais', 'Espagnol', 'Italien']),
                'eye_color': 'Bleu',
                'hair_color': 'Châtain',
                'hair_type': 'Raides',
                'height': 182,
                'skin_tone': 'Claire',
                'build': 'Mince',
                'talent_types': json.dumps(['Acteur/Actrice Principal(e)', 'Chanteur/Chanteuse']),
                'other_talents': json.dumps(['Piano', 'Escrime', 'Natation']),
                'email': 'julien.moreau@demo.cinema',
                'phone': '+33612345678',
                'whatsapp': '+33612345678',
                'linkedin': 'julien-moreau-cinema',
                'twitter': '@julien_moreau',
                'previous_productions': json.dumps([
                    {'title': 'Paris sous la pluie', 'year': '2023', 'type': 'Film'},
                    {'title': "L'Art de vivre", 'year': '2020-2022', 'type': 'Série TV'}
                ])
            },
            {
                'first_name': 'Chukwudi',
                'last_name': 'Okonkwo',
                'gender': 'M',
                'date_of_birth': date(1992, 11, 8),
                'id_document_type': 'passport',
                'id_document_number': 'NG456789',
                'ethnicities': json.dumps(['Africaine']),
                'country_of_origin': 'Nigeria',
                'nationality': 'Nigériane',
                'country_of_residence': 'Nigeria',
                'city_of_residence': 'Lagos',
                'languages_spoken': json.dumps(['Anglais', 'Igbo', 'Yoruba', 'Français']),
                'eye_color': 'Marron foncé',
                'hair_color': 'Noir',
                'hair_type': 'Très Crépus',
                'height': 185,
                'skin_tone': 'Foncée',
                'build': 'Musclé',
                'talent_types': json.dumps(['Acteur/Actrice Secondaire', 'Cascadeur/Cascadeuse']),
                'other_talents': json.dumps(['Arts Martiaux', 'Parkour', 'Basketball']),
                'email': 'chukwudi.okonkwo@demo.cinema',
                'phone': '+2348012345678',
                'whatsapp': '+2348012345678',
                'instagram': '@chukwudi_action',
                'tiktok': '@chukwudi_stunts',
                'youtube': 'Chukwudi Action',
                'previous_productions': json.dumps([
                    {'title': 'Nollywood Heroes', 'year': '2023', 'type': 'Film'},
                    {'title': 'Lagos Action', 'year': '2021', 'type': 'Série Web'}
                ])
            }
        ]
        
        created_count = 0
        for talent_data in demo_cinema_talents:
            # Vérifier si ce talent existe déjà
            existing = CinemaTalent.query.filter_by(email=talent_data['email']).first()
            if existing:
                print(f"⏭️  Profil déjà existant: {talent_data['first_name']} {talent_data['last_name']}")
                continue
            
            talent = CinemaTalent()
            
            # Données non chiffrées
            talent.first_name = talent_data['first_name']
            talent.last_name = talent_data['last_name']
            talent.gender = talent_data['gender']
            talent.date_of_birth = talent_data['date_of_birth']
            talent.id_document_type = talent_data['id_document_type']
            talent.ethnicities = talent_data['ethnicities']
            talent.country_of_origin = talent_data['country_of_origin']
            talent.nationality = talent_data['nationality']
            talent.country_of_residence = talent_data['country_of_residence']
            talent.city_of_residence = talent_data['city_of_residence']
            talent.languages_spoken = talent_data['languages_spoken']
            talent.eye_color = talent_data['eye_color']
            talent.hair_color = talent_data['hair_color']
            talent.hair_type = talent_data['hair_type']
            talent.height = talent_data['height']
            talent.skin_tone = talent_data['skin_tone']
            talent.build = talent_data['build']
            talent.talent_types = talent_data['talent_types']
            talent.other_talents = talent_data['other_talents']
            talent.email = talent_data['email']
            talent.website = talent_data.get('website')
            talent.previous_productions = talent_data['previous_productions']
            
            # Données chiffrées avec la NOUVELLE clé
            talent.id_document_number_encrypted = encrypt_sensitive_data(talent_data['id_document_number'])
            talent.phone_encrypted = encrypt_sensitive_data(talent_data['phone'])
            talent.whatsapp_encrypted = encrypt_sensitive_data(talent_data['whatsapp'])
            
            # Réseaux sociaux chiffrés
            if 'facebook' in talent_data:
                talent.facebook_encrypted = encrypt_sensitive_data(talent_data['facebook'])
            if 'instagram' in talent_data:
                talent.instagram_encrypted = encrypt_sensitive_data(talent_data['instagram'])
            if 'linkedin' in talent_data:
                talent.linkedin_encrypted = encrypt_sensitive_data(talent_data['linkedin'])
            if 'twitter' in talent_data:
                talent.twitter_encrypted = encrypt_sensitive_data(talent_data['twitter'])
            if 'youtube' in talent_data:
                talent.youtube_encrypted = encrypt_sensitive_data(talent_data['youtube'])
            if 'tiktok' in talent_data:
                talent.tiktok_encrypted = encrypt_sensitive_data(talent_data['tiktok'])
            if 'telegram' in talent_data:
                talent.telegram_encrypted = encrypt_sensitive_data(talent_data['telegram'])
            if 'imdb_url' in talent_data:
                talent.imdb_url_encrypted = encrypt_sensitive_data(talent_data['imdb_url'])
            if 'threads' in talent_data:
                talent.threads_encrypted = encrypt_sensitive_data(talent_data['threads'])
            
            db.session.add(talent)
            created_count += 1
            print(f"✅ Créé: {talent.first_name} {talent.last_name}")
        
        db.session.commit()
        
        print(f"\n✅ {created_count} profils CINEMA créés avec la nouvelle clé de chiffrement!")
        
        # Vérifier le total
        total = CinemaTalent.query.count()
        print(f"📊 Total de profils CINEMA dans la base: {total}")

if __name__ == '__main__':
    fix_cinema_encryption()
