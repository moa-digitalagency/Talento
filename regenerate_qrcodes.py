"""
taalentio.com
Script to regenerate all QR codes with the correct base URL

This script regenerates QR codes for:
1. All regular users
2. All CINEMA talents

Usage:
    python regenerate_qrcodes.py
"""

import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.cinema_talent import CinemaTalent
from app.utils.qr_generator import generate_qr_code, generate_cinema_qr_code
from config import Config

def regenerate_all_qrcodes():
    """Regenerate all QR codes with the correct base URL"""
    app = create_app()
    
    with app.app_context():
        # Get the current base URL
        base_url = Config.get_base_url()
        print(f"\n{'='*60}")
        print(f"🔄 RÉGÉNÉRATION DES QR CODES")
        print(f"{'='*60}")
        print(f"📍 Base URL utilisée: {base_url}")
        print(f"{'='*60}\n")
        
        # Regenerate QR codes for regular users
        print("👤 Régénération des QR codes pour les utilisateurs réguliers...")
        users = User.query.filter(User.unique_code.isnot(None)).all()
        users_count = 0
        users_errors = 0
        
        for user in users:
            try:
                qr_path = os.path.join('app', 'static', 'uploads', 'qrcodes')
                filename = generate_qr_code(user.unique_code, qr_path, profile_type='user')
                user.qr_code_filename = filename
                users_count += 1
                print(f"  ✅ {user.unique_code} - {user.full_name}")
            except Exception as e:
                users_errors += 1
                print(f"  ❌ Erreur pour {user.unique_code}: {str(e)}")
        
        # Commit user QR codes
        try:
            db.session.commit()
            print(f"\n✅ {users_count} QR codes utilisateurs régénérés avec succès!")
            if users_errors > 0:
                print(f"⚠️  {users_errors} erreur(s) rencontrée(s)")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Erreur lors de la sauvegarde: {str(e)}")
        
        # Regenerate QR codes for CINEMA talents
        print(f"\n{'='*60}")
        print("🎬 Régénération des QR codes pour les talents CINEMA...")
        cinema_talents = CinemaTalent.query.filter(CinemaTalent.unique_code.isnot(None)).all()
        cinema_count = 0
        cinema_errors = 0
        
        for talent in cinema_talents:
            try:
                qr_path = os.path.join('app', 'static', 'uploads', 'qrcodes')
                filename = generate_cinema_qr_code(talent.unique_code, qr_path)
                talent.qr_code_filename = filename
                cinema_count += 1
                print(f"  ✅ {talent.unique_code} - {talent.full_name}")
            except Exception as e:
                cinema_errors += 1
                print(f"  ❌ Erreur pour {talent.unique_code}: {str(e)}")
        
        # Commit cinema talent QR codes
        try:
            db.session.commit()
            print(f"\n✅ {cinema_count} QR codes CINEMA régénérés avec succès!")
            if cinema_errors > 0:
                print(f"⚠️  {cinema_errors} erreur(s) rencontrée(s)")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Erreur lors de la sauvegarde: {str(e)}")
        
        # Summary
        print(f"\n{'='*60}")
        print("📊 RÉSUMÉ")
        print(f"{'='*60}")
        print(f"✅ Utilisateurs réguliers: {users_count}/{len(users)}")
        print(f"✅ Talents CINEMA: {cinema_count}/{len(cinema_talents)}")
        print(f"🔗 Base URL: {base_url}")
        print(f"{'='*60}\n")

if __name__ == '__main__':
    regenerate_all_qrcodes()
