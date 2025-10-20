import os
import subprocess
import json
from datetime import datetime
from flask import current_app
from app.models.settings import AppSettings


class UpdateService:
    """Service pour gérer les mises à jour de l'application depuis GitHub"""
    
    UPDATE_LOG_FILE = 'logs/update_history.json'
    
    @staticmethod
    def check_git_available():
        """Vérifie si git est disponible"""
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    @staticmethod
    def get_current_branch():
        """Récupère la branche actuelle"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return 'unknown'
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la récupération de la branche: {e}")
            return 'unknown'
    
    @staticmethod
    def get_current_commit():
        """Récupère le hash du commit actuel"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--short', 'HEAD'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return 'unknown'
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la récupération du commit: {e}")
            return 'unknown'
    
    @staticmethod
    def check_updates_available():
        """Vérifie si des mises à jour sont disponibles sur le repo distant"""
        try:
            subprocess.run(['git', 'fetch'], capture_output=True, cwd=os.getcwd())
            
            result = subprocess.run(
                ['git', 'rev-list', 'HEAD...origin/' + UpdateService.get_current_branch(), '--count'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                count = int(result.stdout.strip())
                return count > 0, count
            return False, 0
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la vérification des mises à jour: {e}")
            return False, 0
    
    @staticmethod
    def get_remote_url():
        """Récupère l'URL du repo distant"""
        try:
            result = subprocess.run(
                ['git', 'config', '--get', 'remote.origin.url'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return 'N/A'
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la récupération de l'URL distante: {e}")
            return 'N/A'
    
    @staticmethod
    def get_commit_logs(count=5):
        """Récupère les derniers commits"""
        try:
            result = subprocess.run(
                ['git', 'log', f'-{count}', '--pretty=format:%h|%an|%ar|%s'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                logs = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('|')
                        if len(parts) == 4:
                            logs.append({
                                'hash': parts[0],
                                'author': parts[1],
                                'date': parts[2],
                                'message': parts[3]
                            })
                return logs
            return []
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la récupération des logs de commit: {e}")
            return []
    
    @staticmethod
    def pull_updates():
        """Pull les mises à jour depuis GitHub"""
        try:
            result = subprocess.run(
                ['git', 'pull', 'origin', UpdateService.get_current_branch()],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            return success, output
        except Exception as e:
            current_app.logger.error(f"Erreur lors du pull des mises à jour: {e}")
            return False, str(e)
    
    @staticmethod
    def install_dependencies():
        """Installe les dépendances depuis requirements.txt"""
        try:
            result = subprocess.run(
                ['pip', 'install', '-r', 'requirements.txt'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            return success, output
        except Exception as e:
            current_app.logger.error(f"Erreur lors de l'installation des dépendances: {e}")
            return False, str(e)
    
    @staticmethod
    def run_migrations():
        """Exécute les migrations de base de données"""
        try:
            result = subprocess.run(
                ['flask', 'db', 'upgrade'],
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
                env={**os.environ, 'FLASK_APP': 'app.py'}
            )
            
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            return success, output
        except Exception as e:
            current_app.logger.error(f"Erreur lors de l'exécution des migrations: {e}")
            return False, str(e)
    
    @staticmethod
    def create_rollback_point():
        """Crée un point de restauration avant la mise à jour"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la création du point de restauration: {e}")
            return None
    
    @staticmethod
    def rollback_to_commit(commit_hash):
        """Restaure le code à un commit précédent"""
        try:
            result = subprocess.run(
                ['git', 'reset', '--hard', commit_hash],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            return result.returncode == 0
        except Exception as e:
            current_app.logger.error(f"Erreur lors du rollback: {e}")
            return False
    
    @staticmethod
    def perform_full_update():
        """Effectue une mise à jour complète de l'application avec rollback automatique en cas d'échec"""
        if not UpdateService._ensure_logs_directory():
            return False, {'error': 'Impossible de créer le répertoire de logs'}
        
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'steps': [],
            'success': False
        }
        
        rollback_point = UpdateService.create_rollback_point()
        if not rollback_point:
            log_entry['error'] = 'Impossible de créer un point de restauration'
            UpdateService._save_update_log(log_entry)
            return False, log_entry
        
        log_entry['rollback_point'] = rollback_point
        
        # Étape 1: Pull des mises à jour
        success_pull, output_pull = UpdateService.pull_updates()
        log_entry['steps'].append({
            'name': 'Git Pull',
            'success': success_pull,
            'output': output_pull
        })
        
        if not success_pull:
            UpdateService._save_update_log(log_entry)
            return False, log_entry
        
        # Étape 2: Installation des dépendances
        success_deps, output_deps = UpdateService.install_dependencies()
        log_entry['steps'].append({
            'name': 'Install Dependencies',
            'success': success_deps,
            'output': output_deps
        })
        
        if not success_deps:
            current_app.logger.warning(f"Échec de l'installation des dépendances, rollback vers {rollback_point}")
            UpdateService.rollback_to_commit(rollback_point)
            log_entry['rolled_back'] = True
            UpdateService._save_update_log(log_entry)
            return False, log_entry
        
        # Étape 3: Migrations de la base de données
        success_migrate, output_migrate = UpdateService.run_migrations()
        log_entry['steps'].append({
            'name': 'Database Migration',
            'success': success_migrate,
            'output': output_migrate
        })
        
        if not success_migrate:
            current_app.logger.warning(f"Échec des migrations, rollback vers {rollback_point}")
            UpdateService.rollback_to_commit(rollback_point)
            log_entry['rolled_back'] = True
            UpdateService._save_update_log(log_entry)
            return False, log_entry
        
        log_entry['success'] = True
        UpdateService._save_update_log(log_entry)
        
        return True, log_entry
    
    @staticmethod
    def _ensure_logs_directory():
        """S'assure que le répertoire logs existe"""
        try:
            os.makedirs('logs', exist_ok=True)
            return True
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la création du répertoire logs: {e}")
            return False
    
    @staticmethod
    def _save_update_log(log_entry):
        """Sauvegarde le log de mise à jour"""
        try:
            if not UpdateService._ensure_logs_directory():
                return
            
            logs = []
            if os.path.exists(UpdateService.UPDATE_LOG_FILE):
                with open(UpdateService.UPDATE_LOG_FILE, 'r') as f:
                    logs = json.load(f)
            
            logs.append(log_entry)
            
            logs = logs[-20:]
            
            with open(UpdateService.UPDATE_LOG_FILE, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la sauvegarde du log de mise à jour: {e}")
    
    @staticmethod
    def get_update_history(count=10):
        """Récupère l'historique des mises à jour"""
        try:
            if not os.path.exists(UpdateService.UPDATE_LOG_FILE):
                return []
            
            with open(UpdateService.UPDATE_LOG_FILE, 'r') as f:
                logs = json.load(f)
            
            return logs[-count:]
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la récupération de l'historique des mises à jour: {e}")
            return []
    
    @staticmethod
    def get_git_info():
        """Récupère toutes les informations Git"""
        has_updates, update_count = UpdateService.check_updates_available()
        
        return {
            'git_available': UpdateService.check_git_available(),
            'current_branch': UpdateService.get_current_branch(),
            'current_commit': UpdateService.get_current_commit(),
            'remote_url': UpdateService.get_remote_url(),
            'has_updates': has_updates,
            'update_count': update_count,
            'recent_commits': UpdateService.get_commit_logs(5)
        }
