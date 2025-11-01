"""
Système de migration automatique robuste pour taalentio.com
Gère les nouvelles tables et colonnes sans faire crasher l'application
"""
import os
import logging
from sqlalchemy import inspect, text
from flask import current_app

logger = logging.getLogger(__name__)

def safe_auto_migrate(db):
    """
    Exécute les migrations automatiques de manière sécurisée
    Ne fait jamais crasher l'application, même en cas d'erreur
    """
    try:
        logger.info("🔄 Démarrage de la migration automatique...")
        
        with current_app.app_context():
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            logger.info(f"📊 Tables existantes: {len(existing_tables)}")
            
            if not _ensure_tables_exist(db, existing_tables):
                logger.warning("⚠️ Création de tables échouée, mais application continue")
            
            if not _ensure_columns_exist(db, inspector):
                logger.warning("⚠️ Ajout de colonnes échoué, mais application continue")
            
            logger.info("✅ Migration automatique terminée")
            return True
            
    except Exception as e:
        logger.error(f"❌ Erreur lors de la migration automatique: {e}")
        logger.error("ℹ️ L'application continue malgré l'erreur de migration")
        return False

def _ensure_tables_exist(db, existing_tables):
    """
    Vérifie et crée les tables manquantes
    Retourne False en cas d'erreur, mais ne lève pas d'exception
    """
    try:
        required_tables = ['users', 'talents', 'user_talents', 'countries', 
                          'cities', 'cinema_talents', 'app_settings']
        
        missing_tables = [t for t in required_tables if t not in existing_tables]
        
        if missing_tables:
            logger.info(f"➕ Création des tables manquantes: {', '.join(missing_tables)}")
            db.create_all()
            logger.info(f"✅ {len(missing_tables)} tables créées")
        else:
            logger.info("✅ Toutes les tables requises existent")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la création des tables: {e}")
        return False

def _ensure_columns_exist(db, inspector):
    """
    Vérifie et ajoute les colonnes manquantes
    Retourne False en cas d'erreur, mais ne lève pas d'exception
    """
    try:
        columns_added = 0
        
        is_sqlite = str(db.engine.url).startswith('sqlite')
        
        users_columns = {
            'availability': 'VARCHAR(50)',
            'work_mode': 'VARCHAR(50)',
            'rate_range': 'VARCHAR(100)',
            'profile_score': 'INTEGER DEFAULT 0',
            'cv_analysis': 'TEXT',
            'cv_analyzed_at': 'TIMESTAMP',
            'languages': 'VARCHAR(255)',
            'education': 'TEXT',
            'passport_number_encrypted': 'TEXT',
            'residence_card_encrypted': 'TEXT',
            'website': 'VARCHAR(255)',
            'imdb_url_encrypted': 'TEXT',
            'threads_encrypted': 'TEXT'
        }
        
        cinema_columns = {
            'unique_code': 'VARCHAR(12)' if is_sqlite else 'VARCHAR(12) UNIQUE',
            'qr_code_filename': 'VARCHAR(255)',
            'website': 'VARCHAR(255)',
            'imdb_url_encrypted': 'TEXT',
            'threads_encrypted': 'TEXT'
        }
        
        talents_columns = {
            'tag': "VARCHAR(20) DEFAULT 'general'"
        }
        
        columns_added += _add_columns_to_table(db, inspector, 'users', users_columns)
        columns_added += _add_columns_to_table(db, inspector, 'cinema_talents', cinema_columns)
        columns_added += _add_columns_to_table(db, inspector, 'talents', talents_columns)
        
        if columns_added > 0:
            logger.info(f"✅ {columns_added} colonnes ajoutées au total")
        else:
            logger.info("✅ Toutes les colonnes requises existent")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la vérification des colonnes: {e}")
        return False

def _add_columns_to_table(db, inspector, table_name, columns_to_check):
    """
    Ajoute des colonnes manquantes à une table spécifique
    Retourne le nombre de colonnes ajoutées
    """
    columns_added = 0
    
    try:
        if table_name not in inspector.get_table_names():
            logger.warning(f"⚠️ Table {table_name} n'existe pas encore")
            return 0
        
        existing_columns = [col['name'] for col in inspector.get_columns(table_name)]
        
        for col_name, col_type in columns_to_check.items():
            if col_name not in existing_columns:
                try:
                    logger.info(f"➕ Ajout de {table_name}.{col_name}...")
                    
                    with db.engine.begin() as conn:
                        conn.execute(text(f'ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type}'))
                    
                    columns_added += 1
                    logger.info(f"✅ Colonne {table_name}.{col_name} ajoutée")
                    
                except Exception as e:
                    if 'already exists' in str(e).lower() or 'duplicate' in str(e).lower():
                        logger.debug(f"ℹ️ Colonne {table_name}.{col_name} existe déjà")
                    else:
                        logger.warning(f"⚠️ Impossible d'ajouter {table_name}.{col_name}: {e}")
        
        return columns_added
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'ajout de colonnes à {table_name}: {e}")
        return columns_added

def run_initial_seed(db):
    """
    Lance le seeding initial des données (pays, villes, talents, admin)
    Utilisé uniquement lors de la première installation
    """
    import subprocess
    import sys
    
    try:
        if os.environ.get('SKIP_AUTO_SEED') == '1':
            logger.info("⏭️ Seeding automatique désactivé (SKIP_AUTO_SEED=1)")
            return True
        
        logger.info("🌱 Lancement du seeding initial...")
        
        env = os.environ.copy()
        env['SKIP_AUTO_MIGRATION'] = '1'
        
        result = subprocess.run(
            [sys.executable, 'migrations_init.py'],
            env=env,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            logger.info("✅ Seeding initial terminé avec succès")
            logger.debug(result.stdout)
            return True
        else:
            logger.warning(f"⚠️ Seeding initial avec code de retour {result.returncode}")
            logger.warning(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("❌ Seeding initial timeout après 60 secondes")
        return False
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du seeding initial: {e}")
        return False
