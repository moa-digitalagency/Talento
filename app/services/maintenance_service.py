"""
Service de maintenance système pour Talento
Gestion des opérations de maintenance : optimisation DB, nettoyage, analyse, intégrité
"""
import os
import shutil
import psutil
from datetime import datetime
from sqlalchemy import text, inspect
from app import db
from app.models import AppSettings
import logging

logger = logging.getLogger(__name__)


class MaintenanceService:
    """Service de maintenance système"""
    
    @staticmethod
    def optimize_database():
        """Optimise la base de données PostgreSQL"""
        try:
            results = []
            success_count = 0
            error_count = 0
            
            # Récupérer les tables
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            # VACUUM ANALYZE doit être exécuté en dehors d'une transaction
            # Utiliser raw_connection() pour contourner la gestion transactionnelle de SQLAlchemy
            raw_conn = db.engine.raw_connection()
            try:
                raw_conn.set_isolation_level(0)  # AUTOCOMMIT mode
                cursor = raw_conn.cursor()
                
                for table in tables:
                    try:
                        cursor.execute(f"VACUUM ANALYZE {table}")
                        results.append(f"✅ Table {table} optimisée")
                        success_count += 1
                    except Exception as e:
                        results.append(f"⚠️  Table {table}: {str(e)}")
                        error_count += 1
                        logger.warning(f"Erreur lors de l'optimisation de {table}: {e}")
                
                cursor.close()
            finally:
                raw_conn.close()
            
            # Enregistrer la dernière optimisation
            AppSettings.set('last_db_optimization', datetime.now().isoformat())
            
            if success_count > 0:
                return {
                    'success': True,
                    'message': f'{success_count}/{len(tables)} tables optimisées avec succès',
                    'details': results,
                    'tables_count': len(tables),
                    'success_count': success_count,
                    'error_count': error_count
                }
            else:
                return {
                    'success': False,
                    'message': f'Aucune table optimisée. {error_count} erreurs.',
                    'details': results,
                    'tables_count': len(tables)
                }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'optimisation de la base de données: {e}")
            return {
                'success': False,
                'message': f'Erreur: {str(e)}',
                'details': []
            }
    
    @staticmethod
    def clean_temp_files():
        """Nettoie les fichiers temporaires"""
        try:
            cleaned = []
            total_size = 0
            files_removed = 0
            
            # Dossiers temporaires à nettoyer
            temp_dirs = [
                'app/static/temp',
                'app/static/uploads/temp',
                '/tmp/talento_temp'
            ]
            
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for filename in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, filename)
                        try:
                            # Vérifier l'âge du fichier (supprimer si > 24h)
                            file_age = datetime.now().timestamp() - os.path.getmtime(file_path)
                            if file_age > 86400:  # 24 heures
                                file_size = os.path.getsize(file_path)
                                if os.path.isfile(file_path):
                                    os.remove(file_path)
                                elif os.path.isdir(file_path):
                                    shutil.rmtree(file_path)
                                total_size += file_size
                                files_removed += 1
                                cleaned.append(f"✅ {filename} ({file_size / 1024:.1f} KB)")
                        except Exception as e:
                            cleaned.append(f"⚠️  {filename}: {str(e)}")
            
            # Nettoyer les fichiers .pyc et __pycache__
            pyc_removed = 0
            for root, dirs, files in os.walk('.'):
                # Nettoyer __pycache__
                if '__pycache__' in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, '__pycache__'))
                        pyc_removed += 1
                    except:
                        pass
                
                # Nettoyer fichiers .pyc
                for file in files:
                    if file.endswith('.pyc'):
                        try:
                            os.remove(os.path.join(root, file))
                            pyc_removed += 1
                        except:
                            pass
            
            # Enregistrer le dernier nettoyage
            AppSettings.set('last_temp_cleanup', datetime.now().isoformat())
            
            return {
                'success': True,
                'message': f'{files_removed} fichiers temporaires supprimés ({total_size / 1024:.1f} KB libérés)',
                'details': cleaned,
                'files_removed': files_removed,
                'pyc_removed': pyc_removed,
                'size_freed': total_size
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage des fichiers temporaires: {e}")
            return {
                'success': False,
                'message': f'Erreur: {str(e)}',
                'details': []
            }
    
    @staticmethod
    def analyze_performance():
        """Analyse les performances du système"""
        try:
            metrics = []
            
            # Métriques système
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            metrics.append(f"🖥️  CPU: {cpu_percent}%")
            metrics.append(f"💾 RAM: {memory.percent}% utilisée ({memory.used / (1024**3):.1f}GB / {memory.total / (1024**3):.1f}GB)")
            metrics.append(f"💿 Disque: {disk.percent}% utilisé ({disk.used / (1024**3):.1f}GB / {disk.total / (1024**3):.1f}GB)")
            
            # Métriques base de données
            with db.engine.connect() as conn:
                # Taille de la base de données
                result = conn.execute(text("""
                    SELECT pg_size_pretty(pg_database_size(current_database())) as size
                """))
                db_size = result.fetchone()[0]
                metrics.append(f"🗄️  Taille DB: {db_size}")
                
                # Nombre de connexions actives
                result = conn.execute(text("""
                    SELECT count(*) FROM pg_stat_activity WHERE state = 'active'
                """))
                active_connections = result.fetchone()[0]
                metrics.append(f"🔌 Connexions actives: {active_connections}")
                
                # Tables les plus volumineuses
                result = conn.execute(text("""
                    SELECT schemaname, tablename, 
                           pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
                    FROM pg_tables 
                    WHERE schemaname = 'public'
                    ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
                    LIMIT 5
                """))
                top_tables = result.fetchall()
                
                metrics.append("\n📊 Top 5 tables volumineuses:")
                for table in top_tables:
                    metrics.append(f"   - {table[1]}: {table[2]}")
            
            # Enregistrer la dernière analyse
            AppSettings.set('last_performance_analysis', datetime.now().isoformat())
            
            # Évaluation globale
            status = "good"
            if cpu_percent > 80 or memory.percent > 80 or disk.percent > 80:
                status = "warning"
            if cpu_percent > 90 or memory.percent > 90 or disk.percent > 90:
                status = "critical"
            
            return {
                'success': True,
                'message': 'Analyse des performances terminée',
                'status': status,
                'metrics': metrics,
                'cpu': cpu_percent,
                'memory': memory.percent,
                'disk': disk.percent,
                'db_size': db_size
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse des performances: {e}")
            return {
                'success': False,
                'message': f'Erreur: {str(e)}',
                'metrics': []
            }
    
    @staticmethod
    def verify_data_integrity():
        """Vérifie l'intégrité des données"""
        try:
            issues = []
            checks_passed = 0
            checks_total = 0
            
            # Vérifier les contraintes de clés étrangères
            with db.engine.connect() as conn:
                # Vérifier les users sans country ou city valides
                checks_total += 1
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM users 
                    WHERE (country_id IS NOT NULL AND country_id NOT IN (SELECT id FROM countries))
                       OR (city_id IS NOT NULL AND city_id NOT IN (SELECT id FROM cities))
                """))
                invalid_users = result.fetchone()[0]
                if invalid_users > 0:
                    issues.append(f"⚠️  {invalid_users} utilisateurs avec pays/ville invalide")
                else:
                    checks_passed += 1
                
                # Vérifier les talents orphelins (user_talents sans user ou talent)
                checks_total += 1
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM user_talents 
                    WHERE user_id NOT IN (SELECT id FROM users)
                       OR talent_id NOT IN (SELECT id FROM talents)
                """))
                orphan_talents = result.fetchone()[0]
                if orphan_talents > 0:
                    issues.append(f"⚠️  {orphan_talents} associations de talents orphelines")
                else:
                    checks_passed += 1
                
                # Vérifier les project_talents orphelins
                checks_total += 1
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM project_talents 
                    WHERE project_id NOT IN (SELECT id FROM projects)
                """))
                orphan_projects = result.fetchone()[0]
                if orphan_projects > 0:
                    issues.append(f"⚠️  {orphan_projects} associations projet-talent orphelines")
                else:
                    checks_passed += 1
                
                # Vérifier les cinema_talents sans code unique
                checks_total += 1
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM cinema_talents 
                    WHERE unique_code IS NULL OR unique_code = ''
                """))
                invalid_cinema_codes = result.fetchone()[0]
                if invalid_cinema_codes > 0:
                    issues.append(f"⚠️  {invalid_cinema_codes} talents cinéma sans code unique")
                else:
                    checks_passed += 1
                
                # Vérifier les doublons d'email
                checks_total += 1
                result = conn.execute(text("""
                    SELECT email, COUNT(*) as cnt 
                    FROM users 
                    GROUP BY email 
                    HAVING COUNT(*) > 1
                """))
                duplicate_emails = result.fetchall()
                if duplicate_emails:
                    issues.append(f"⚠️  {len(duplicate_emails)} emails en double détectés")
                    for email, count in duplicate_emails:
                        issues.append(f"   - {email}: {count} fois")
                else:
                    checks_passed += 1
                
                # Vérifier les doublons de codes uniques
                checks_total += 1
                result = conn.execute(text("""
                    SELECT unique_code, COUNT(*) as cnt 
                    FROM users 
                    WHERE unique_code IS NOT NULL
                    GROUP BY unique_code 
                    HAVING COUNT(*) > 1
                """))
                duplicate_codes = result.fetchall()
                if duplicate_codes:
                    issues.append(f"⚠️  {len(duplicate_codes)} codes uniques en double")
                    for code, count in duplicate_codes:
                        issues.append(f"   - {code}: {count} fois")
                else:
                    checks_passed += 1
            
            # Enregistrer la dernière vérification
            AppSettings.set('last_integrity_check', datetime.now().isoformat())
            
            status = "healthy" if len(issues) == 0 else ("warning" if checks_passed / checks_total > 0.5 else "critical")
            
            return {
                'success': True,
                'message': f'{checks_passed}/{checks_total} vérifications passées',
                'status': status,
                'issues': issues if issues else ["✅ Aucun problème détecté"],
                'checks_passed': checks_passed,
                'checks_total': checks_total
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification de l'intégrité: {e}")
            return {
                'success': False,
                'message': f'Erreur: {str(e)}',
                'issues': []
            }
    
    @staticmethod
    def get_last_maintenance_dates():
        """Récupère les dates des dernières opérations de maintenance"""
        return {
            'db_optimization': AppSettings.get('last_db_optimization'),
            'temp_cleanup': AppSettings.get('last_temp_cleanup'),
            'performance_analysis': AppSettings.get('last_performance_analysis'),
            'integrity_check': AppSettings.get('last_integrity_check')
        }
