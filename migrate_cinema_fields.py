#!/usr/bin/env python3
"""
Script de migration pour ajouter les nouveaux champs au modèle CinemaTalent
"""
from app import create_app, db
from sqlalchemy import text

def migrate_cinema_fields():
    """Ajoute les nouveaux champs au modèle CinemaTalent"""
    app = create_app()
    
    with app.app_context():
        print("🎬 Migration des champs CINEMA...")
        
        try:
            # Check if table exists
            inspector = db.inspect(db.engine)
            if 'cinema_talents' not in inspector.get_table_names():
                print("✅ Table cinema_talents n'existe pas encore, elle sera créée automatiquement")
                db.create_all()
                print("✅ Table cinema_talents créée avec succès")
                return
            
            # Get existing columns
            existing_columns = [col['name'] for col in inspector.get_columns('cinema_talents')]
            print(f"📋 Colonnes existantes: {len(existing_columns)}")
            
            # Define new columns to add
            new_columns = {
                'country_of_origin': 'VARCHAR(100)',
                'ethnicities': 'TEXT',
            }
            
            # Add missing columns
            added_count = 0
            for column_name, column_type in new_columns.items():
                if column_name not in existing_columns:
                    try:
                        sql = f'ALTER TABLE cinema_talents ADD COLUMN {column_name} {column_type}'
                        db.session.execute(text(sql))
                        db.session.commit()
                        print(f"✅ Colonne '{column_name}' ajoutée")
                        added_count += 1
                    except Exception as e:
                        print(f"⚠️  Erreur lors de l'ajout de '{column_name}': {str(e)}")
                        db.session.rollback()
                else:
                    print(f"ℹ️  Colonne '{column_name}' existe déjà")
            
            # Rename ethnicity to ethnicities if needed
            if 'ethnicity' in existing_columns and 'ethnicities' not in existing_columns:
                try:
                    # SQLite doesn't support RENAME COLUMN easily, so we'll just add the new column
                    # and copy data later if needed
                    print("ℹ️  Ancienne colonne 'ethnicity' détectée - les données seront migrées manuellement si nécessaire")
                except Exception as e:
                    print(f"⚠️  Note: {str(e)}")
            
            print(f"\n✅ Migration terminée: {added_count} colonnes ajoutées")
            
        except Exception as e:
            print(f"❌ Erreur lors de la migration: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    migrate_cinema_fields()
