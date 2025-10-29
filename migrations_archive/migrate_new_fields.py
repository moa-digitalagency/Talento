#!/usr/bin/env python3
"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""


"""
Script de migration pour ajouter les nouveaux champs aux modèles User et CinemaTalent
- website (User)
- imdb_url_encrypted (User et CinemaTalent)
- threads_encrypted (User et CinemaTalent)
"""
from app import create_app, db
from sqlalchemy import text

def migrate_new_fields():
    """Ajoute les nouveaux champs aux modèles User et CinemaTalent"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Migration des nouveaux champs...")
        
        try:
            inspector = db.inspect(db.engine)
            
            # Migration pour la table users
            print("\n📋 Table: users")
            if 'users' in inspector.get_table_names():
                existing_columns = [col['name'] for col in inspector.get_columns('users')]
                print(f"   Colonnes existantes: {len(existing_columns)}")
                
                # Define new columns for users table
                new_user_columns = {
                    'website': 'VARCHAR(500)',
                    'imdb_url_encrypted': 'TEXT',
                    'threads_encrypted': 'TEXT',
                }
                
                # Add missing columns
                added_count = 0
                for column_name, column_type in new_user_columns.items():
                    if column_name not in existing_columns:
                        try:
                            sql = f'ALTER TABLE users ADD COLUMN {column_name} {column_type}'
                            db.session.execute(text(sql))
                            db.session.commit()
                            print(f"   ✅ Colonne '{column_name}' ajoutée")
                            added_count += 1
                        except Exception as e:
                            print(f"   ⚠️  Erreur lors de l'ajout de '{column_name}': {str(e)}")
                            db.session.rollback()
                    else:
                        print(f"   ℹ️  Colonne '{column_name}' existe déjà")
                
                print(f"   ✅ {added_count} colonnes ajoutées à users")
            else:
                print("   ℹ️  Table users n'existe pas encore")
            
            # Migration pour la table cinema_talents
            print("\n📋 Table: cinema_talents")
            if 'cinema_talents' in inspector.get_table_names():
                existing_columns = [col['name'] for col in inspector.get_columns('cinema_talents')]
                print(f"   Colonnes existantes: {len(existing_columns)}")
                
                # Define new columns for cinema_talents table
                new_cinema_columns = {
                    'imdb_url_encrypted': 'TEXT',
                    'threads_encrypted': 'TEXT',
                }
                
                # Add missing columns
                added_count = 0
                for column_name, column_type in new_cinema_columns.items():
                    if column_name not in existing_columns:
                        try:
                            sql = f'ALTER TABLE cinema_talents ADD COLUMN {column_name} {column_type}'
                            db.session.execute(text(sql))
                            db.session.commit()
                            print(f"   ✅ Colonne '{column_name}' ajoutée")
                            added_count += 1
                        except Exception as e:
                            print(f"   ⚠️  Erreur lors de l'ajout de '{column_name}': {str(e)}")
                            db.session.rollback()
                    else:
                        print(f"   ℹ️  Colonne '{column_name}' existe déjà")
                
                print(f"   ✅ {added_count} colonnes ajoutées à cinema_talents")
            else:
                print("   ℹ️  Table cinema_talents n'existe pas encore")
            
            print(f"\n✅ Migration terminée avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors de la migration: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    migrate_new_fields()
