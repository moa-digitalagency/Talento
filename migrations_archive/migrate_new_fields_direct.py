#!/usr/bin/env python3
"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""


"""
Script de migration directe pour ajouter les nouveaux champs aux modèles User et CinemaTalent
"""
import os
import psycopg2
from urllib.parse import urlparse

def migrate_new_fields_direct():
    """Ajoute les nouveaux champs directement via psycopg2"""
    
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL non trouvée dans les variables d'environnement")
        return
    
    # Parse database URL
    result = urlparse(database_url)
    
    # Connect to database
    try:
        conn = psycopg2.connect(
            host=result.hostname,
            database=result.path[1:],
            user=result.username,
            password=result.password,
            port=result.port
        )
        cur = conn.cursor()
        
        print("🔄 Migration des nouveaux champs...")
        print(f"🔗 Connexion à la base de données: {result.hostname}")
        
        # Check existing columns in users table
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users'
        """)
        existing_user_columns = [row[0] for row in cur.fetchall()]
        print(f"\n📋 Table users: {len(existing_user_columns)} colonnes existantes")
        
        # Add new columns to users table
        user_columns_to_add = [
            ('website', 'VARCHAR(500)'),
            ('imdb_url_encrypted', 'TEXT'),
            ('threads_encrypted', 'TEXT'),
        ]
        
        added_user_count = 0
        for column_name, column_type in user_columns_to_add:
            if column_name not in existing_user_columns:
                try:
                    cur.execute(f'ALTER TABLE users ADD COLUMN {column_name} {column_type}')
                    conn.commit()
                    print(f"   ✅ Colonne '{column_name}' ajoutée à users")
                    added_user_count += 1
                except Exception as e:
                    print(f"   ⚠️  Erreur lors de l'ajout de '{column_name}' à users: {str(e)}")
                    conn.rollback()
            else:
                print(f"   ℹ️  Colonne '{column_name}' existe déjà dans users")
        
        # Check existing columns in cinema_talents table
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'cinema_talents'
        """)
        existing_cinema_columns = [row[0] for row in cur.fetchall()]
        print(f"\n📋 Table cinema_talents: {len(existing_cinema_columns)} colonnes existantes")
        
        # Add new columns to cinema_talents table
        cinema_columns_to_add = [
            ('imdb_url_encrypted', 'TEXT'),
            ('threads_encrypted', 'TEXT'),
        ]
        
        added_cinema_count = 0
        for column_name, column_type in cinema_columns_to_add:
            if column_name not in existing_cinema_columns:
                try:
                    cur.execute(f'ALTER TABLE cinema_talents ADD COLUMN {column_name} {column_type}')
                    conn.commit()
                    print(f"   ✅ Colonne '{column_name}' ajoutée à cinema_talents")
                    added_cinema_count += 1
                except Exception as e:
                    print(f"   ⚠️  Erreur lors de l'ajout de '{column_name}' à cinema_talents: {str(e)}")
                    conn.rollback()
            else:
                print(f"   ℹ️  Colonne '{column_name}' existe déjà dans cinema_talents")
        
        print(f"\n✅ Migration terminée avec succès")
        print(f"   📊 {added_user_count} colonnes ajoutées à users")
        print(f"   📊 {added_cinema_count} colonnes ajoutées à cinema_talents")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la connexion ou de la migration: {str(e)}")
        return

if __name__ == '__main__':
    migrate_new_fields_direct()
