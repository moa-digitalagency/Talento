#!/usr/bin/env python
"""
Migration pour ajouter les nouveaux champs CINEMA
- talent_types (types de talents)
- website (site web)
- telegram_encrypted (nouveau réseau social)
"""
from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("🔄 Migration des améliorations CINEMA...")
    
    # Ajouter la colonne talent_types
    try:
        db.session.execute(text("ALTER TABLE cinema_talents ADD COLUMN talent_types TEXT"))
        print("✅ Colonne 'talent_types' ajoutée")
    except Exception as e:
        if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
            print("ℹ️  Colonne 'talent_types' existe déjà")
        else:
            print(f"⚠️  Erreur lors de l'ajout de 'talent_types': {e}")
    
    # Ajouter la colonne website
    try:
        db.session.execute(text("ALTER TABLE cinema_talents ADD COLUMN website VARCHAR(500)"))
        print("✅ Colonne 'website' ajoutée")
    except Exception as e:
        if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
            print("ℹ️  Colonne 'website' existe déjà")
        else:
            print(f"⚠️  Erreur lors de l'ajout de 'website': {e}")
    
    # Ajouter la colonne telegram_encrypted
    try:
        db.session.execute(text("ALTER TABLE cinema_talents ADD COLUMN telegram_encrypted TEXT"))
        print("✅ Colonne 'telegram_encrypted' ajoutée")
    except Exception as e:
        if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
            print("ℹ️  Colonne 'telegram_encrypted' existe déjà")
        else:
            print(f"⚠️  Erreur lors de l'ajout de 'telegram_encrypted': {e}")
    
    db.session.commit()
    print("✅ Migration terminée avec succès!")
