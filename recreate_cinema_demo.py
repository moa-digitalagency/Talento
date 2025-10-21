#!/usr/bin/env python
"""
Script pour supprimer et recréer les profils CINEMA de démonstration
"""
import os
import json
from datetime import date
from app import create_app, db
from app.models.cinema_talent import CinemaTalent
from app.utils.encryption import encrypt_sensitive_data
from app.utils.cinema_code_generator import generate_cinema_unique_code
from app.utils.qr_generator import generate_cinema_qr_code

def delete_cinema_demo_profiles():
    """Supprimer les profils CINEMA de démonstration"""
    print("\n🗑️  Suppression des profils CINEMA de démonstration...")
    
    demo_emails = [
        'amina.elfassi@demo.cinema',
        'julien.moreau@demo.cinema',
        'chukwudi.okonkwo@demo.cinema'
    ]
    
    count = 0
    for email in demo_emails:
        talent = CinemaTalent.query.filter_by(email=email).first()
        if talent:
            db.session.delete(talent)
            count += 1
            print(f"  ✓ Supprimé: {talent.full_name}")
    
    db.session.commit()
    print(f"✅ {count} profils CINEMA supprimés")
    return True

def create_cinema_demo_profiles():
    """Créer les profils CINEMA de démonstration avec toutes les informations"""
    print("\n✨ Création des nouveaux profils CINEMA de démonstration...")
    
    demo_cinema_talents = [
        {
            # Profile 1: Actrice marocaine
            'first_name': 'Amina',
            'last_name': 'El Fassi',
            'gender': 'F',
            'date_of_birth': date(1995, 3, 15),
            'id_document_type': 'national_id',
            'id_document_number': 'AB123456',
            'ethnicities': json.dumps(['Arabe', 'Amazigh']),
            'country_of_origin': 'Maroc',
            'nationality': 'Marocaine',
            'country_of_residence': 'Maroc',
            'city_of_residence': 'Casablanca',
            'languages_spoken': json.dumps(['Arabe', 'Français', 'Anglais', 'Amazigh (Tamazight)']),
            'eye_color': 'Marron',
            'hair_color': 'Noir',
            'hair_type': 'Ondulé',
            'height': 168,
            'skin_tone': 'Olive',
            'build': 'Athlétique',
            'talent_types': json.dumps(['Acteur/Actrice', 'Mannequin', 'Danseur/euse']),
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
                {'title': 'Racines du Désert', 'year': '2021', 'type': 'Série TV'},
                {'title': 'Sous le Soleil Marocain', 'year': '2020', 'type': 'Film'}
            ])
        },
        {
            # Profile 2: Acteur français
            'first_name': 'Julien',
            'last_name': 'Moreau',
            'gender': 'M',
            'date_of_birth': date(1988, 7, 22),
            'id_document_type': 'passport',
            'id_document_number': 'FR987654',
            'ethnicities': json.dumps(['Européen']),
            'country_of_origin': 'France',
            'nationality': 'Française',
            'country_of_residence': 'France',
            'city_of_residence': 'Paris',
            'languages_spoken': json.dumps(['Français', 'Anglais', 'Espagnol', 'Italien']),
            'eye_color': 'Bleu',
            'hair_color': 'Châtain',
            'hair_type': 'Droit',
            'height': 182,
            'skin_tone': 'Claire',
            'build': 'Musclé',
            'talent_types': json.dumps(['Acteur/Actrice', 'Cascadeur/euse', 'Chanteur/euse']),
            'other_talents': json.dumps(['Arts martiaux', 'Chant lyrique', 'Escrime']),
            'email': 'julien.moreau@demo.cinema',
            'phone': '+33612345678',
            'whatsapp': '+33612345678',
            'website': 'https://julienmoreau-actor.fr',
            'facebook': 'julien.moreau.actor',
            'instagram': '@julien_moreau_films',
            'twitter': '@JulienMoreauFR',
            'linkedin': 'julien-moreau-actor',
            'youtube': 'Julien Moreau Channel',
            'telegram': '@julien_moreau',
            'imdb_url': 'https://imdb.com/name/nm7654321',
            'threads': '@julien.moreau',
            'previous_productions': json.dumps([
                {'title': 'Les Ombres de Paris', 'year': '2023', 'type': 'Film'},
                {'title': 'Brigade Criminelle', 'year': '2020-2022', 'type': 'Série TV'},
                {'title': 'Le Dernier Voyage', 'year': '2019', 'type': 'Film'}
            ])
        },
        {
            # Profile 3: Acteur nigérian
            'first_name': 'Chukwudi',
            'last_name': 'Okonkwo',
            'gender': 'M',
            'date_of_birth': date(1992, 11, 5),
            'id_document_type': 'passport',
            'id_document_number': 'NG456789',
            'ethnicities': json.dumps(['Igbo', 'Yoruba']),
            'country_of_origin': 'Nigéria',
            'nationality': 'Nigériane',
            'country_of_residence': 'Nigéria',
            'city_of_residence': 'Lagos',
            'languages_spoken': json.dumps(['Anglais', 'Igbo', 'Yoruba', 'Haoussa', 'Français']),
            'eye_color': 'Marron foncé',
            'hair_color': 'Noir',
            'hair_type': 'Crépu',
            'height': 178,
            'skin_tone': 'Foncée',
            'build': 'Athlétique',
            'talent_types': json.dumps(['Acteur/Actrice', 'Musicien(ne)', 'Metteur en scène']),
            'other_talents': json.dumps(['Comédie stand-up', 'Guitare', 'Production audiovisuelle']),
            'email': 'chukwudi.okonkwo@demo.cinema',
            'phone': '+2348012345678',
            'whatsapp': '+2348012345678',
            'website': 'https://chukwudiokonkwo.ng',
            'facebook': 'chukwudi.okonkwo.nollywood',
            'instagram': '@chukwudi_nollywood',
            'tiktok': '@chukwudi_movies',
            'snapchat': 'chukwudi_cinema',
            'twitter': '@ChukwudiActor',
            'youtube': 'Chukwudi Okonkwo',
            'telegram': '@chukwudi_nollywood',
            'imdb_url': 'https://imdb.com/name/nm9876543',
            'threads': '@chukwudi_official',
            'previous_productions': json.dumps([
                {'title': 'Lagos Love Story', 'year': '2023', 'type': 'Film'},
                {'title': 'The King\'s Return', 'year': '2022', 'type': 'Film'},
                {'title': 'Family Ties', 'year': '2021-2023', 'type': 'Série TV'}
            ])
        }
    ]
    
    count = 0
    for talent_data in demo_cinema_talents:
        # Extraire les champs à crypter
        id_document_number = talent_data.pop('id_document_number')
        phone = talent_data.pop('phone')
        whatsapp = talent_data.pop('whatsapp', None)
        facebook = talent_data.pop('facebook', None)
        instagram = talent_data.pop('instagram', None)
        twitter = talent_data.pop('twitter', None)
        linkedin = talent_data.pop('linkedin', None)
        youtube = talent_data.pop('youtube', None)
        tiktok = talent_data.pop('tiktok', None)
        snapchat = talent_data.pop('snapchat', None)
        telegram = talent_data.pop('telegram', None)
        imdb_url = talent_data.pop('imdb_url', None)
        threads = talent_data.pop('threads', None)
        
        # Créer le profil
        talent = CinemaTalent(**talent_data)
        
        # Générer le code unique
        unique_code = generate_cinema_unique_code(
            talent.country_of_residence,
            talent.city_of_residence,
            talent.gender
        )
        talent.unique_code = unique_code
        
        # Crypter les données sensibles
        talent.id_document_number_encrypted = encrypt_sensitive_data(id_document_number)
        talent.phone_encrypted = encrypt_sensitive_data(phone)
        if whatsapp:
            talent.whatsapp_encrypted = encrypt_sensitive_data(whatsapp)
        if facebook:
            talent.facebook_encrypted = encrypt_sensitive_data(facebook)
        if instagram:
            talent.instagram_encrypted = encrypt_sensitive_data(instagram)
        if twitter:
            talent.twitter_encrypted = encrypt_sensitive_data(twitter)
        if linkedin:
            talent.linkedin_encrypted = encrypt_sensitive_data(linkedin)
        if youtube:
            talent.youtube_encrypted = encrypt_sensitive_data(youtube)
        if tiktok:
            talent.tiktok_encrypted = encrypt_sensitive_data(tiktok)
        if snapchat:
            talent.snapchat_encrypted = encrypt_sensitive_data(snapchat)
        if telegram:
            talent.telegram_encrypted = encrypt_sensitive_data(telegram)
        if imdb_url:
            talent.imdb_url_encrypted = encrypt_sensitive_data(imdb_url)
        if threads:
            talent.threads_encrypted = encrypt_sensitive_data(threads)
        
        # Générer le QR code
        from flask import current_app
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
        qr_save_path = os.path.join(upload_folder, 'qrcodes')
        os.makedirs(qr_save_path, exist_ok=True)
        
        qr_filename = generate_cinema_qr_code(unique_code, qr_save_path)
        talent.qr_code_filename = qr_filename
        
        db.session.add(talent)
        count += 1
        print(f"  ✓ Créé: {talent.full_name} ({unique_code})")
    
    db.session.commit()
    print(f"✅ {count} profils CINEMA de démonstration créés avec succès")
    return True

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🎬 RECRÉATION DES PROFILS CINEMA DE DÉMONSTRATION")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        try:
            delete_cinema_demo_profiles()
            create_cinema_demo_profiles()
            
            print("\n" + "=" * 60)
            print("✅ RECRÉATION TERMINÉE AVEC SUCCÈS")
            print("=" * 60)
            print(f"\n📊 Total profils CINEMA: {CinemaTalent.query.count()}")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()
