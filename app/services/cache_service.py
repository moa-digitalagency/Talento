"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class CacheService:
    """Service pour gérer le cache de l'application"""
    
    @staticmethod
    def get_directory_size(path):
        """Calculer la taille d'un répertoire en MB"""
        total = 0
        try:
            for entry in os.scandir(path):
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += CacheService.get_directory_size(entry.path)
        except (PermissionError, FileNotFoundError):
            pass
        return round(total / (1024 * 1024), 2)  # Convertir en MB
    
    @staticmethod
    def get_cache_stats():
        """Obtenir les statistiques du cache"""
        app_root = Path(__file__).parent.parent
        
        # Cache système (fichiers .pyc)
        system_size = 0
        for root, dirs, files in os.walk(app_root):
            for file in files:
                if file.endswith('.pyc') or '__pycache__' in root:
                    try:
                        system_size += os.path.getsize(os.path.join(root, file))
                    except:
                        pass
        
        # Cache Flask (si existant)
        flask_cache_path = app_root / 'flask_cache'
        flask_size = CacheService.get_directory_size(flask_cache_path) if flask_cache_path.exists() else 0
        
        # Fichiers temporaires
        temp_path = app_root / 'static' / 'uploads' / 'temp'
        temp_size = CacheService.get_directory_size(temp_path) if temp_path.exists() else 0
        
        return {
            'system_size': f"{round(system_size / (1024 * 1024), 2)} MB",
            'flask_size': f"{flask_size} MB",
            'temp_size': f"{temp_size} MB"
        }
    
    @staticmethod
    def clear_system_cache():
        """Nettoyer le cache système (.pyc files)"""
        app_root = Path(__file__).parent.parent
        removed = 0
        
        for root, dirs, files in os.walk(app_root):
            # Supprimer les fichiers .pyc
            for file in files:
                if file.endswith('.pyc'):
                    try:
                        os.remove(os.path.join(root, file))
                        removed += 1
                    except:
                        pass
            
            # Supprimer les dossiers __pycache__
            for dir_name in dirs:
                if dir_name == '__pycache__':
                    try:
                        shutil.rmtree(os.path.join(root, dir_name))
                        removed += 1
                    except:
                        pass
        
        return {'success': True, 'removed': removed}
    
    @staticmethod
    def clear_flask_cache():
        """Nettoyer le cache Flask"""
        app_root = Path(__file__).parent.parent
        flask_cache_path = app_root / 'flask_cache'
        
        if flask_cache_path.exists():
            try:
                shutil.rmtree(flask_cache_path)
                return {'success': True, 'message': 'Cache Flask nettoyé'}
            except Exception as e:
                return {'success': False, 'message': str(e)}
        
        return {'success': True, 'message': 'Aucun cache Flask trouvé'}
    
    @staticmethod
    def clear_temp_files():
        """Nettoyer les fichiers temporaires"""
        app_root = Path(__file__).parent.parent
        temp_path = app_root / 'static' / 'uploads' / 'temp'
        
        if temp_path.exists():
            try:
                removed = 0
                for file in temp_path.iterdir():
                    if file.is_file():
                        file.unlink()
                        removed += 1
                return {'success': True, 'removed': removed}
            except Exception as e:
                return {'success': False, 'message': str(e)}
        
        return {'success': True, 'removed': 0}
    
    @staticmethod
    def clear_all():
        """Nettoyer tous les caches"""
        results = []
        
        system_result = CacheService.clear_system_cache()
        results.append(f"Cache système: {system_result.get('removed', 0)} éléments supprimés")
        
        flask_result = CacheService.clear_flask_cache()
        results.append(f"Cache Flask: {flask_result.get('message', 'nettoyé')}")
        
        temp_result = CacheService.clear_temp_files()
        results.append(f"Fichiers temporaires: {temp_result.get('removed', 0)} fichiers supprimés")
        
        return {'success': True, 'results': results}
