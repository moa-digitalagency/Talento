#!/usr/bin/env python3
"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""


"""
Script pour garantir que le compte admin existe toujours
Exécuté automatiquement au démarrage de l'application
"""
import os
from app import create_app, db
from app.models.user import User
from app.models.location import Country, City

def ensure_admin_exists():
    """
    Garantit que le compte admin existe avec les bonnes informations
    Idempotent - peut être exécuté plusieurs fois sans problème
    """
    app = create_app()
    
    with app.app_context():
        admin_email = 'admin@talento.com'
        admin_code = 'MARAB0001N'
        admin_password = os.environ.get('ADMIN_PASSWORD', '@4dm1n')
        
        # Chercher si l'admin existe
        admin = User.query.filter(
            (User.email == admin_email) | (User.unique_code == admin_code)
        ).first()
        
        if not admin:
            print("👤 Création du compte admin...")
            
            # Chercher Morocco et Rabat
            morocco = Country.query.filter_by(code='MA').first()
            rabat = City.query.filter_by(code='RAB').first()
            
            if not morocco or not rabat:
                print("⚠️  Impossible de créer l'admin - Morocco/Rabat introuvables")
                print("⚠️  Exécutez d'abord: python3 migrations_init.py")
                return False
            
            # Créer l'admin
            admin = User(
                email=admin_email,
                first_name='Admin',
                last_name='Talento',
                unique_code=admin_code,
                is_admin=True,
                account_active=True,
                country_id=morocco.id,
                city_id=rabat.id,
                gender='N'
            )
            admin.set_password(admin_password)
            admin.phone = '+212600000000'
            
            db.session.add(admin)
            
            try:
                db.session.commit()
                print(f"✅ Compte admin créé: {admin_email}")
                print(f"   Code unique: {admin_code}")
                print(f"   Mot de passe: {admin_password}")
                return True
            except Exception as e:
                db.session.rollback()
                print(f"⚠️  Erreur lors de la création de l'admin: {e}")
                return False
        else:
            # Vérifier que le mot de passe est correct
            if not admin.check_password(admin_password):
                print(f"🔐 Mise à jour du mot de passe admin...")
                admin.set_password(admin_password)
                try:
                    db.session.commit()
                    print(f"✅ Mot de passe admin mis à jour")
                except Exception as e:
                    db.session.rollback()
                    print(f"⚠️  Erreur lors de la mise à jour: {e}")
            
            # Vérifier que c'est bien un admin
            if not admin.is_admin:
                print(f"👑 Activation des droits admin...")
                admin.is_admin = True
                try:
                    db.session.commit()
                    print(f"✅ Droits admin activés")
                except Exception as e:
                    db.session.rollback()
                    print(f"⚠️  Erreur lors de l'activation: {e}")
            
            print(f"✅ Compte admin existe: {admin.email} ({admin.unique_code})")
            return True

if __name__ == '__main__':
    ensure_admin_exists()
