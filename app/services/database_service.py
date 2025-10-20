import os
import sqlite3
from datetime import datetime
from flask import current_app
from sqlalchemy import text, inspect
from app import db
from app.models import User, Talent, Country, City, UserTalent


class DatabaseService:
    """Service pour gérer les diagnostics et statistiques de la base de données"""
    
    @staticmethod
    def get_connection_info():
        """Récupère les informations de connexion à la base de données"""
        db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI', '')
        
        is_postgresql = 'postgresql' in db_uri.lower()
        is_sqlite = 'sqlite' in db_uri.lower()
        
        masked_uri = DatabaseService._mask_db_uri(db_uri)
        
        return {
            'type': 'PostgreSQL' if is_postgresql else 'SQLite',
            'uri_masked': masked_uri,
            'is_postgresql': is_postgresql,
            'is_sqlite': is_sqlite
        }
    
    @staticmethod
    def _mask_db_uri(uri):
        """Masque les informations sensibles dans l'URI de la base de données"""
        if not uri:
            return ''
        
        if 'postgresql' in uri.lower():
            if '@' in uri:
                parts = uri.split('@')
                if '://' in parts[0]:
                    protocol_user = parts[0].split('://')
                    return f"{protocol_user[0]}://****:****@{parts[1]}"
            return uri
        
        if 'sqlite:///' in uri.lower():
            return uri.replace(os.getcwd(), '<project_root>')
        
        return uri
    
    @staticmethod
    def get_table_stats():
        """Récupère les statistiques des tables principales"""
        try:
            stats = {
                'users': User.query.count(),
                'users_active': User.query.filter_by(account_active=True).count(),
                'users_admin': User.query.filter_by(is_admin=True).count(),
                'talents': Talent.query.count(),
                'countries': Country.query.count(),
                'cities': City.query.count(),
                'user_talents': UserTalent.query.count()
            }
            return stats
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la récupération des statistiques: {e}")
            return {}
    
    @staticmethod
    def get_database_size():
        """Récupère la taille de la base de données"""
        try:
            conn_info = DatabaseService.get_connection_info()
            
            if conn_info['is_sqlite']:
                db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI', '')
                db_path = db_uri.replace('sqlite:///', '')
                
                if os.path.exists(db_path):
                    size_bytes = os.path.getsize(db_path)
                    return DatabaseService._format_size(size_bytes)
                return '0 B'
            
            elif conn_info['is_postgresql']:
                result = db.session.execute(text(
                    "SELECT pg_size_pretty(pg_database_size(current_database()))"
                ))
                return result.scalar()
            
            return 'N/A'
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la récupération de la taille de la DB: {e}")
            return 'N/A'
    
    @staticmethod
    def _format_size(bytes_size):
        """Formate une taille en bytes en format lisible"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} TB"
    
    @staticmethod
    def get_last_migration():
        """Récupère la dernière migration appliquée"""
        try:
            result = db.session.execute(text(
                "SELECT version_num FROM alembic_version ORDER BY version_num DESC LIMIT 1"
            ))
            version = result.scalar()
            return version if version else 'Aucune'
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la récupération de la version de migration: {e}")
            return 'N/A'
    
    @staticmethod
    def test_connection():
        """Teste la connexion à la base de données"""
        try:
            db.session.execute(text('SELECT 1'))
            return True
        except Exception as e:
            current_app.logger.error(f"Erreur de connexion à la DB: {e}")
            return False
    
    @staticmethod
    def get_all_tables():
        """Liste toutes les tables de la base de données"""
        try:
            inspector = inspect(db.engine)
            return inspector.get_table_names()
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la récupération des tables: {e}")
            return []
    
    @staticmethod
    def get_full_diagnostics():
        """Récupère tous les diagnostics de la base de données"""
        return {
            'connection': DatabaseService.get_connection_info(),
            'connection_status': DatabaseService.test_connection(),
            'size': DatabaseService.get_database_size(),
            'tables': DatabaseService.get_all_tables(),
            'table_stats': DatabaseService.get_table_stats(),
            'last_migration': DatabaseService.get_last_migration(),
            'timestamp': datetime.utcnow().isoformat()
        }
