"""
Migration: Ajout des champs nationality, residence_country_id et residence_city_id
Date: 2025-10-28
Description: Ajoute les nouveaux champs de localisation au modèle User
"""

from app import create_app, db
from sqlalchemy import text

app = create_app()

def migrate():
    with app.app_context():
        try:
            print("🔄 Début de la migration des champs de localisation...")
            
            # Vérifier si les colonnes existent déjà
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' 
                AND column_name IN ('nationality', 'residence_country_id', 'residence_city_id')
            """))
            existing_columns = [row[0] for row in result]
            
            if 'nationality' not in existing_columns:
                print("  ➕ Ajout de la colonne 'nationality'...")
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN nationality VARCHAR(100)
                """))
                print("  ✅ Colonne 'nationality' ajoutée")
            else:
                print("  ⏭️  Colonne 'nationality' existe déjà")
            
            if 'residence_country_id' not in existing_columns:
                print("  ➕ Ajout de la colonne 'residence_country_id'...")
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN residence_country_id INTEGER REFERENCES countries(id)
                """))
                print("  ✅ Colonne 'residence_country_id' ajoutée")
            else:
                print("  ⏭️  Colonne 'residence_country_id' existe déjà")
            
            if 'residence_city_id' not in existing_columns:
                print("  ➕ Ajout de la colonne 'residence_city_id'...")
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN residence_city_id INTEGER REFERENCES cities(id)
                """))
                print("  ✅ Colonne 'residence_city_id' ajoutée")
            else:
                print("  ⏭️  Colonne 'residence_city_id' existe déjà")
            
            # Migrer les données existantes
            print("  🔄 Migration des données existantes...")
            db.session.execute(text("""
                UPDATE users 
                SET residence_country_id = country_id,
                    residence_city_id = city_id
                WHERE residence_country_id IS NULL OR residence_city_id IS NULL
            """))
            print("  ✅ Données migrées")
            
            db.session.commit()
            print("✅ Migration terminée avec succès!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de la migration: {e}")
            raise

if __name__ == '__main__':
    migrate()
