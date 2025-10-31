"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

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
            # Utilise python -m pip pour garantir qu'on utilise le bon pip
            result = subprocess.run(
                ['python', '-m', 'pip', 'install', '--upgrade', '-r', 'requirements.txt'],
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
                timeout=300  # 5 minutes timeout
            )
            
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            if not success:
                current_app.logger.error(f"Échec de l'installation pip. Code de retour: {result.returncode}")
                current_app.logger.error(f"Sortie: {output}")
            
            return success, output
        except subprocess.TimeoutExpired:
            current_app.logger.error("Timeout lors de l'installation des dépendances (>5min)")
            return False, "Timeout: L'installation a pris plus de 5 minutes"
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
        current_app.logger.info(f"Point de restauration créé: {rollback_point}")
        
        # Étape 1: Pull des mises à jour
        current_app.logger.info("Début du pull des mises à jour...")
        success_pull, output_pull = UpdateService.pull_updates()
        log_entry['steps'].append({
            'name': 'Git Pull',
            'success': success_pull,
            'output': output_pull[:500] if len(output_pull) > 500 else output_pull  # Limiter la taille
        })
        
        if not success_pull:
            current_app.logger.error("Échec du pull Git")
            UpdateService._save_update_log(log_entry)
            return False, log_entry
        
        current_app.logger.info("Pull Git réussi")
        
        # Étape 2: Installation des dépendances
        current_app.logger.info("Début de l'installation des dépendances...")
        success_deps, output_deps = UpdateService.install_dependencies()
        log_entry['steps'].append({
            'name': 'Install Dependencies',
            'success': success_deps,
            'output': output_deps[:1000] if len(output_deps) > 1000 else output_deps  # Limiter la taille
        })
        
        if not success_deps:
            current_app.logger.warning(f"Échec de l'installation des dépendances, rollback vers {rollback_point}")
            UpdateService.rollback_to_commit(rollback_point)
            log_entry['rolled_back'] = True
            UpdateService._save_update_log(log_entry)
            return False, log_entry
        
        current_app.logger.info("Installation des dépendances réussie")
        
        # Étape 3: Migrations de la base de données
        current_app.logger.info("Début des migrations de la base de données...")
        success_migrate, output_migrate = UpdateService.run_migrations()
        log_entry['steps'].append({
            'name': 'Database Migration',
            'success': success_migrate,
            'output': output_migrate[:500] if len(output_migrate) > 500 else output_migrate  # Limiter la taille
        })
        
        if not success_migrate:
            current_app.logger.warning(f"Échec des migrations, rollback vers {rollback_point}")
            UpdateService.rollback_to_commit(rollback_point)
            log_entry['rolled_back'] = True
            UpdateService._save_update_log(log_entry)
            return False, log_entry
        
        current_app.logger.info("Migrations de la base de données réussies")
        
        log_entry['success'] = True
        UpdateService._save_update_log(log_entry)
        current_app.logger.info("Mise à jour complète réussie!")
        
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
                try:
                    with open(UpdateService.UPDATE_LOG_FILE, 'r') as f:
                        content = f.read().strip()
                        if content and not content.startswith('<!doctype') and not content.startswith('<html'):
                            logs = json.loads(content)
                except json.JSONDecodeError:
                    current_app.logger.warning("Log file corrupted, starting fresh")
                    logs = []
            
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
                content = f.read().strip()
                if not content or content.startswith('<!doctype') or content.startswith('<html'):
                    current_app.logger.warning("Log file contains HTML instead of JSON, resetting it")
                    return []
                logs = json.loads(content)
            
            return logs[-count:]
        except json.JSONDecodeError as e:
            current_app.logger.error(f"Erreur de décodage JSON dans l'historique des mises à jour: {e}")
            try:
                os.remove(UpdateService.UPDATE_LOG_FILE)
                current_app.logger.info("Fichier de log corrompu supprimé")
            except:
                pass
            return []
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la récupération de l'historique des mises à jour: {e}")
            return []
    
    @staticmethod
    def has_local_changes():
        """Vérifie s'il y a des modifications locales non committées"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            return bool(result.stdout.strip())
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la vérification des modifications: {e}")
            return False
    
    @staticmethod
    def git_pull():
        """Wrapper pour pull_updates avec format de réponse standard"""
        success, output = UpdateService.pull_updates()
        return {
            'success': success,
            'message': output if output else ('Mise à jour réussie' if success else 'Échec de la mise à jour')
        }
    
    @staticmethod
    def git_status():
        """Récupère le statut Git"""
        try:
            result = subprocess.run(
                ['git', 'status', '--short'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            if result.returncode == 0:
                status = result.stdout.strip()
                return {
                    'success': True,
                    'message': status if status else 'Aucune modification en cours'
                }
            return {
                'success': False,
                'message': 'Erreur lors de la récupération du statut'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def get_git_info():
        """Récupère toutes les informations Git"""
        has_updates, update_count = UpdateService.check_updates_available()
        
        return {
            'git_available': UpdateService.check_git_available(),
            'branch': UpdateService.get_current_branch(),
            'commit_hash': UpdateService.get_current_commit(),
            'remote_url': UpdateService.get_remote_url(),
            'has_updates': has_updates,
            'update_count': update_count,
            'has_changes': UpdateService.has_local_changes(),
            'recent_commits': UpdateService.get_commit_logs(5)
        }
    
    @staticmethod
    def configure_git_remote(repo_url, branch='main'):
        """Configure le remote Git avec l'URL fournie"""
        try:
            # Vérifier si un remote origin existe déjà
            check_remote = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if check_remote.returncode == 0:
                # Remote existe, le mettre à jour
                result = subprocess.run(
                    ['git', 'remote', 'set-url', 'origin', repo_url],
                    capture_output=True,
                    text=True,
                    cwd=os.getcwd()
                )
            else:
                # Aucun remote, en ajouter un
                result = subprocess.run(
                    ['git', 'remote', 'add', 'origin', repo_url],
                    capture_output=True,
                    text=True,
                    cwd=os.getcwd()
                )
            
            if result.returncode != 0:
                return False, result.stderr
            
            # Vérifier la connexion
            fetch_result = subprocess.run(
                ['git', 'fetch', 'origin'],
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
                timeout=30
            )
            
            if fetch_result.returncode == 0:
                current_app.logger.info(f"Remote Git configuré avec succès: {repo_url}")
                return True, "Remote configuré et connexion vérifiée avec succès"
            else:
                current_app.logger.warning(f"Remote configuré mais impossible de fetch: {fetch_result.stderr}")
                return True, f"Remote configuré mais connexion non vérifiée: {fetch_result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout lors de la vérification de la connexion au repository"
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la configuration du remote Git: {e}")
            return False, str(e)
    
    @staticmethod
    def git_pull_with_migration(auto_migrate=True):
        """
        Pull les mises à jour GitHub avec gestion intelligente des migrations
        Cette méthode ajoute automatiquement les nouvelles tables sans toucher aux données existantes
        """
        try:
            # Créer un point de restauration
            rollback_point = UpdateService.create_rollback_point()
            if not rollback_point:
                return {
                    'success': False,
                    'message': 'Impossible de créer un point de restauration'
                }
            
            current_app.logger.info(f"Point de restauration créé: {rollback_point}")
            
            # Étape 1: Pull des mises à jour
            success_pull, output_pull = UpdateService.pull_updates()
            if not success_pull:
                return {
                    'success': False,
                    'message': f'Erreur lors du pull Git: {output_pull}'
                }
            
            current_app.logger.info("Pull Git réussi")
            message_parts = ["Code mis à jour depuis GitHub"]
            
            # Étape 2: Installer les nouvelles dépendances si requirements.txt a changé
            if 'requirements.txt' in output_pull:
                current_app.logger.info("requirements.txt modifié, installation des dépendances...")
                success_deps, output_deps = UpdateService.install_dependencies()
                if success_deps:
                    message_parts.append("Dépendances installées")
                else:
                    current_app.logger.warning(f"Échec de l'installation des dépendances: {output_deps}")
                    message_parts.append(f"Avertissement: Échec installation dépendances")
            
            # Étape 3: Migration de base de données intelligente si activée
            if auto_migrate:
                current_app.logger.info("Exécution des migrations de base de données...")
                
                # Utiliser le script d'init pour gérer intelligemment les nouvelles tables
                try:
                    import sys
                    result = subprocess.run(
                        [sys.executable, 'migrations_init.py'],
                        capture_output=True,
                        text=True,
                        cwd=os.getcwd(),
                        timeout=120
                    )
                    
                    if result.returncode == 0:
                        current_app.logger.info("Migrations exécutées avec succès")
                        message_parts.append("Base de données mise à jour (nouvelles tables ajoutées)")
                    else:
                        # Essayer avec flask db upgrade en fallback
                        success_migrate, output_migrate = UpdateService.run_migrations()
                        if success_migrate:
                            message_parts.append("Migrations Flask appliquées")
                        else:
                            current_app.logger.warning(f"Avertissement migrations: {output_migrate}")
                            message_parts.append("Avertissement: Migrations non appliquées")
                
                except subprocess.TimeoutExpired:
                    current_app.logger.warning("Timeout lors des migrations (>2min)")
                    message_parts.append("Avertissement: Timeout migrations")
                except Exception as e:
                    current_app.logger.error(f"Erreur lors des migrations: {e}")
                    message_parts.append(f"Avertissement migrations: {str(e)}")
            
            # Sauvegarder dans l'historique
            UpdateService._save_update_log({
                'timestamp': datetime.utcnow().isoformat(),
                'type': 'git_pull',
                'success': True,
                'message': ' | '.join(message_parts),
                'details': output_pull[:200] if len(output_pull) > 200 else output_pull
            })
            
            return {
                'success': True,
                'message': ' | '.join(message_parts)
            }
            
        except Exception as e:
            current_app.logger.error(f"Erreur lors de la mise à jour: {e}")
            return {
                'success': False,
                'message': f'Erreur: {str(e)}'
            }
