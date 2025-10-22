#!/usr/bin/env python3
"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""


"""
Script de migration pour ajouter TikTok et Snapchat au modèle CinemaTalent
"""
from app import create_app, db
from sqlalchemy import text

def migrate_cinema_social():
    """Ajoute les colonnes TikTok et Snapchat au modèle CinemaTalent"""
    app = create_app()
    
    with app.app_context():
        print("🎬 Migration des réseaux sociaux CINEMA...")
        
        try:
            inspector = db.inspect(db.engine)
            
            if 'cinema_talents' not in inspector.get_table_names():
                print("❌ Table cinema_talents n'existe pas")
                return
            
            existing_columns = [col['name'] for col in inspector.get_columns('cinema_talents')]
            
            new_columns = {
                'tiktok_encrypted': 'TEXT',
                'snapchat_encrypted': 'TEXT',
            }
            
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
            
            print(f"\n✅ Migration terminée: {added_count} colonnes ajoutées")
            
        except Exception as e:
            print(f"❌ Erreur lors de la migration: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    migrate_cinema_social()
