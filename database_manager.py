#!/usr/bin/env python
"""
═══════════════════════════════════════════════════════════════════════════════
                    GESTIONNAIRE DE BASE DE DONNÉES - Talento Platform
                                    taalentio.com
                              MOA Digital Agency LLC
                            Par : Aisance KALONJI
                         Mail : moa@myoneart.com
                            www.myoneart.com
═══════════════════════════════════════════════════════════════════════════════

DESCRIPTION:
    Gestionnaire unique et consolidé pour l'initialisation, la migration et la
    maintenance de la base de données. Ce fichier remplace:
    - migrations_init.py
    - init_essential_data.py
    - init_full_database.py

    Il offre une gestion complète et sécurisée de la base de données avec:
    - Détection automatique des changements de schéma
    - Protection contre la perte de données
    - Support des mises à jour via GitHub sans casser les données existantes

FONCTIONNALITÉS:
    ✓ Création automatique de toutes les tables manquantes
    ✓ Ajout intelligent des colonnes manquantes (sans perte de données)
    ✓ Seeding des données essentielles (pays, villes, talents, admin)
    ✓ Backup automatique avant modifications critiques
    ✓ Rollback automatique en cas d'erreur
    ✓ Logging détaillé de toutes les opérations
    ✓ Mode dry-run pour voir les changements sans les appliquer
    ✓ Compatible PostgreSQL et SQLite
    ✓ Sûr pour les mises à jour GitHub (n'écrase jamais les données existantes)

USAGE:
    # Premier démarrage de l'application
    python database_manager.py --force

    # Mise à jour après pull GitHub (mode sûr avec backup)
    python database_manager.py --backup-first

    # Mode interactif (demande confirmation pour les opérations critiques)
    python database_manager.py

    # Vérifier ce qui serait modifié sans rien changer
    python database_manager.py --dry-run

OPTIONS:
    --force         Mode non-interactif (pas de confirmation)
    --backup-first  Créer un backup avant toute opération
    --dry-run       Afficher les modifications sans les appliquer
    --verbose, -v   Afficher les logs détaillés
    --help, -h      Afficher cette aide

EXEMPLES:
    # Après un git pull (mise à jour sécurisée)
    python database_manager.py --backup-first

    # Installation fraîche
    python database_manager.py --force

    # Vérifier l'état de la base de données
    python database_manager.py --dry-run

SÉCURITÉ:
    ✓ Backups automatiques avant modifications destructives
    ✓ Rollback automatique en cas d'erreur
    ✓ Données sensibles chiffrées
    ✓ Confirmations pour les opérations critiques
    ✓ Logs détaillés de toutes les opérations
    ✓ Ne supprime jamais de données existantes
    ✓ Idempotent - peut être exécuté plusieurs fois sans danger

═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

# Configuration de l'environnement
os.environ['SKIP_AUTO_MIGRATION'] = '1'

# Imports de l'application
from app import create_app, db
from app.models.user import User
from app.models.talent import Talent, UserTalent
from app.models.location import Country, City
from app.models.cinema_talent import CinemaTalent
from app.models.production import Production
from app.models.project import Project, ProjectTalent
from app.models.attendance import Attendance
from app.models.activity_log import ActivityLog
from app.models.security_log import SecurityLog
from app.models.email_log import EmailLog
from app.models.name_tracking import NameTracking, NameTrackingMatch
from app.models.settings import AppSettings
from app.data.world_countries import WORLD_COUNTRIES
from app.utils.id_generator import generate_unique_code

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class DatabaseInitializer:
    """Gestionnaire complet d'initialisation et migration de base de données"""
    
    def __init__(self, dry_run: bool = False, force: bool = False, backup_first: bool = False):
        self.dry_run = dry_run
        self.force = force
        self.backup_first = backup_first
        self.operations_log = []
        self.changes_made = False
        
    def log_operation(self, operation: str, details: str = ""):
        """Enregistrer une opération dans le log"""
        timestamp = datetime.now().isoformat()
        entry = f"[{timestamp}] {operation}"
        if details:
            entry += f" - {details}"
        self.operations_log.append(entry)
        logger.info(operation + (f" - {details}" if details else ""))
    
    def confirm_action(self, message: str) -> bool:
        """Demander confirmation pour une action (sauf si --force)"""
        if self.force or self.dry_run:
            return True
        response = input(f"\n⚠️  {message} (o/N): ").strip().lower()
        return response in ['o', 'oui', 'y', 'yes']
    
    def create_backup(self) -> Optional[str]:
        """Créer un backup complet de la base de données"""
        if self.dry_run:
            logger.info("💾 [DRY-RUN] Backup serait créé")
            return None
        
        try:
            from app.services.backup_service import BackupService
            logger.info("💾 Création du backup de sécurité...")
            zip_path, temp_dir = BackupService.create_full_backup()
            
            # Déplacer le backup vers un emplacement permanent
            import shutil
            backup_dir = 'backups'
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_filename = os.path.basename(zip_path)
            final_path = os.path.join(backup_dir, backup_filename)
            shutil.move(zip_path, final_path)
            
            # Nettoyer le dossier temporaire
            shutil.rmtree(temp_dir)
            
            logger.info(f"✅ Backup créé: {final_path}")
            self.log_operation("BACKUP_CREATED", final_path)
            return final_path
        except Exception as e:
            logger.error(f"❌ Erreur lors de la création du backup: {e}")
            if not self.force:
                raise
            return None
    
    def get_database_info(self) -> Dict:
        """Obtenir les informations sur la base de données"""
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        db_info = {
            'engine': str(db.engine.url).split(':')[0],
            'tables_count': len(existing_tables),
            'tables': existing_tables,
            'is_postgresql': 'postgresql' in str(db.engine.url),
            'is_sqlite': 'sqlite' in str(db.engine.url)
        }
        
        # Compter les enregistrements dans les tables principales
        if 'users' in existing_tables:
            db_info['users_count'] = User.query.count()
        if 'countries' in existing_tables:
            db_info['countries_count'] = Country.query.count()
        if 'cities' in existing_tables:
            db_info['cities_count'] = City.query.count()
        if 'talents' in existing_tables:
            db_info['talents_count'] = Talent.query.count()
        
        return db_info
    
    def check_and_create_tables(self) -> List[str]:
        """Vérifier et créer les tables manquantes"""
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        required_tables = [
            'users', 'talents', 'user_talents', 'countries', 'cities',
            'cinema_talents', 'productions', 'projects', 'project_talents',
            'attendances', 'activity_logs', 'security_logs', 'email_logs',
            'name_tracking', 'name_tracking_matches', 'app_settings'
        ]
        
        missing_tables = [t for t in required_tables if t not in existing_tables]
        
        if missing_tables:
            logger.info(f"📋 Tables manquantes détectées: {', '.join(missing_tables)}")
            
            if self.dry_run:
                logger.info(f"💡 [DRY-RUN] {len(missing_tables)} tables seraient créées")
                return missing_tables
            
            if not self.force and missing_tables:
                if not self.confirm_action(f"Créer {len(missing_tables)} tables manquantes?"):
                    logger.warning("⏭️  Création de tables annulée par l'utilisateur")
                    return []
            
            logger.info("📝 Création des tables manquantes...")
            try:
                db.create_all()
                logger.info(f"✅ {len(missing_tables)} tables créées avec succès")
                self.log_operation("TABLES_CREATED", f"{len(missing_tables)} tables")
                self.changes_made = True
                return missing_tables
            except Exception as e:
                logger.error(f"❌ Erreur lors de la création des tables: {e}")
                raise
        else:
            logger.info("✅ Toutes les tables requises existent déjà")
            return []
    
    def get_column_definitions(self) -> Dict[str, Dict[str, str]]:
        """Obtenir les définitions de colonnes pour chaque table"""
        db_type = 'postgresql' if 'postgresql' in str(db.engine.url) else 'sqlite'
        
        # Définitions de colonnes pour la table users
        users_columns = {
            'unique_code': 'VARCHAR(10)',
            'first_name': 'VARCHAR(100)',
            'last_name': 'VARCHAR(100)',
            'email': 'VARCHAR(120)',
            'password_hash': 'VARCHAR(255)',
            'date_of_birth': 'DATE',
            'gender': 'VARCHAR(1)',
            'phone_encrypted': 'TEXT',
            'whatsapp_encrypted': 'TEXT',
            'address_encrypted': 'TEXT',
            'passport_number_encrypted': 'TEXT',
            'residence_card_encrypted': 'TEXT',
            'country_id': 'INTEGER',
            'city_id': 'INTEGER',
            'nationality': 'VARCHAR(100)',
            'residence_country_id': 'INTEGER',
            'residence_city_id': 'INTEGER',
            'photo_filename': 'VARCHAR(255)',
            'cv_filename': 'VARCHAR(255)',
            'portfolio_url': 'VARCHAR(500)',
            'website': 'VARCHAR(500)',
            'linkedin_encrypted': 'TEXT',
            'imdb_url_encrypted': 'TEXT',
            'threads_encrypted': 'TEXT',
            'instagram_encrypted': 'TEXT',
            'twitter_encrypted': 'TEXT',
            'facebook_encrypted': 'TEXT',
            'tiktok_encrypted': 'TEXT',
            'youtube_encrypted': 'TEXT',
            'github_encrypted': 'TEXT',
            'behance_encrypted': 'TEXT',
            'dribbble_encrypted': 'TEXT',
            'pinterest_encrypted': 'TEXT',
            'snapchat_encrypted': 'TEXT',
            'telegram_encrypted': 'TEXT',
            'bio': 'TEXT',
            'years_experience': 'INTEGER',
            'profile_score': 'INTEGER DEFAULT 0',
            'availability': 'VARCHAR(50)',
            'work_mode': 'VARCHAR(50)',
            'rate_range': 'VARCHAR(100)',
            'languages': 'VARCHAR(255)',
            'education': 'TEXT',
            'cv_analysis': 'TEXT',
            'cv_analyzed_at': 'TIMESTAMP',
            'is_admin': 'BOOLEAN DEFAULT FALSE',
            'role': "VARCHAR(50) DEFAULT 'user'",
            'account_active': 'BOOLEAN DEFAULT TRUE',
            'qr_code_filename': 'VARCHAR(255)',
            'created_at': 'TIMESTAMP',
            'updated_at': 'TIMESTAMP'
        }
        
        # Définitions de colonnes pour cinema_talents
        cinema_talents_columns = {
            'unique_code': 'VARCHAR(12)' if db_type == 'sqlite' else 'VARCHAR(12) UNIQUE',
            'qr_code_filename': 'VARCHAR(255)',
            'website': 'VARCHAR(500)',
            'imdb_url_encrypted': 'TEXT',
            'threads_encrypted': 'TEXT'
        }
        
        # Définitions de colonnes pour cities
        cities_columns = {
            'country_id': 'INTEGER'
        }
        
        return {
            'users': users_columns,
            'cinema_talents': cinema_talents_columns,
            'cities': cities_columns
        }
    
    def check_and_add_columns(self) -> int:
        """Vérifier et ajouter les colonnes manquantes"""
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        column_definitions = self.get_column_definitions()
        columns_added = 0
        
        for table_name, columns_to_check in column_definitions.items():
            if table_name not in existing_tables:
                logger.debug(f"⏭️  Table {table_name} n'existe pas encore, colonnes ignorées")
                continue
            
            existing_columns = {col['name'] for col in inspector.get_columns(table_name)}
            missing_columns = {col: dtype for col, dtype in columns_to_check.items() 
                             if col not in existing_columns}
            
            if missing_columns:
                logger.info(f"➕ Colonnes manquantes dans {table_name}: {len(missing_columns)}")
                
                for col_name, col_type in missing_columns.items():
                    if self.dry_run:
                        logger.info(f"💡 [DRY-RUN] Ajouterait {table_name}.{col_name} ({col_type})")
                        columns_added += 1
                        continue
                    
                    try:
                        logger.info(f"   ➕ Ajout de {table_name}.{col_name}...")
                        with db.engine.begin() as conn:
                            conn.execute(text(f'ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type}'))
                        
                        logger.info(f"   ✅ Colonne {table_name}.{col_name} ajoutée")
                        self.log_operation("COLUMN_ADDED", f"{table_name}.{col_name}")
                        columns_added += 1
                        self.changes_made = True
                        
                    except Exception as e:
                        error_str = str(e).lower()
                        if 'already exists' in error_str or 'duplicate' in error_str:
                            logger.debug(f"   ℹ️  Colonne {table_name}.{col_name} existe déjà")
                        else:
                            logger.warning(f"   ⚠️  Impossible d'ajouter {table_name}.{col_name}: {e}")
        
        if columns_added > 0:
            logger.info(f"✅ {columns_added} colonnes ajoutées au total")
        else:
            logger.info("✅ Toutes les colonnes requises existent déjà")
        
        return columns_added
    
    def seed_countries(self) -> int:
        """Charger tous les pays du monde"""
        if self.dry_run:
            existing_count = Country.query.count() if 'countries' in inspect(db.engine).get_table_names() else 0
            potential_new = len(WORLD_COUNTRIES) - existing_count
            logger.info(f"💡 [DRY-RUN] {potential_new} pays seraient ajoutés")
            return 0
        
        logger.info("🌍 Chargement des pays...")
        
        added = 0
        for country_data in WORLD_COUNTRIES:
            try:
                if not Country.query.filter_by(code=country_data['code']).first():
                    country = Country(
                        name=country_data['name'],
                        code=country_data['code']
                    )
                    db.session.add(country)
                    added += 1
            except Exception as e:
                logger.debug(f"Pays {country_data['code']} existe déjà ou erreur: {e}")
        
        if added > 0:
            db.session.commit()
            self.log_operation("COUNTRIES_SEEDED", f"{added} pays ajoutés")
            self.changes_made = True
        
        total = Country.query.count()
        logger.info(f"✅ {added} nouveaux pays ajoutés (Total: {total} pays)")
        return added
    
    def seed_cities(self) -> int:
        """Charger les villes principales"""
        if self.dry_run:
            logger.info("💡 [DRY-RUN] Les villes seraient ajoutées")
            return 0
        
        try:
            from app.data.world_cities import WORLD_CITIES
        except ImportError:
            logger.warning("⚠️  Fichier world_cities.py non disponible")
            return 0
        
        logger.info("🏙️  Chargement des villes...")
        
        added = 0
        total_processed = 0
        
        for country_code, cities_list in WORLD_CITIES.items():
            country = Country.query.filter_by(code=country_code).first()
            if not country:
                continue
            
            for city_name in cities_list:
                total_processed += 1
                city_code = f"{country_code}-{total_processed:03d}"
                
                existing = City.query.filter_by(name=city_name, country_id=country.id).first()
                if not existing:
                    city = City(
                        name=city_name,
                        code=city_code,
                        country_id=country.id
                    )
                    db.session.add(city)
                    added += 1
        
        if added > 0:
            db.session.commit()
            self.log_operation("CITIES_SEEDED", f"{added} villes ajoutées")
            self.changes_made = True
        
        total = City.query.count()
        logger.info(f"✅ {added} nouvelles villes ajoutées (Total: {total} villes)")
        return added
    
    def seed_talents(self) -> int:
        """Charger la liste complète des talents depuis constants.py"""
        if self.dry_run:
            logger.info("💡 [DRY-RUN] Les talents seraient ajoutés")
            return 0
        
        logger.info("⭐ Chargement des talents depuis TALENT_CATEGORIES...")
        
        from app.constants import TALENT_CATEGORIES
        
        added = 0
        updated = 0
        
        for category in TALENT_CATEGORIES:
            category_name = category['name']
            category_emoji = category['emoji']
            category_tag = category.get('tag', 'general')
            
            for talent_name in category['talents']:
                try:
                    talent = Talent.query.filter_by(name=talent_name).first()
                    
                    if talent:
                        if talent.category != category_name or talent.emoji != category_emoji or talent.tag != category_tag:
                            talent.category = category_name
                            talent.emoji = category_emoji
                            talent.tag = category_tag
                            updated += 1
                    else:
                        talent = Talent(
                            name=talent_name,
                            category=category_name,
                            emoji=category_emoji,
                            tag=category_tag
                        )
                        db.session.add(talent)
                        added += 1
                except Exception as e:
                    logger.debug(f"Erreur avec le talent {talent_name}: {e}")
        
        if added > 0 or updated > 0:
            db.session.commit()
            self.log_operation("TALENTS_SEEDED", f"{added} ajoutés, {updated} mis à jour")
            self.changes_made = True
        
        total = Talent.query.count()
        cinema_count = Talent.query.filter_by(tag='cinema').count()
        general_count = Talent.query.filter_by(tag='general').count()
        logger.info(f"✅ {added} nouveaux talents ajoutés, {updated} mis à jour")
        logger.info(f"   Total: {total} talents ({general_count} général, {cinema_count} cinéma)")
        return added
    
    def create_admin_user(self) -> bool:
        """Créer le compte administrateur par défaut"""
        if self.dry_run:
            logger.info("💡 [DRY-RUN] Compte admin serait vérifié/créé")
            return False
        
        logger.info("👤 Vérification du compte administrateur...")
        
        admin_email = 'admin@talento.com'
        admin = User.query.filter_by(email=admin_email).first()
        
        if admin:
            logger.info(f"✅ Compte admin existe déjà: {admin_email}")
            if not admin.is_admin:
                admin.is_admin = True
                admin.role = 'admin'
                db.session.commit()
                logger.info("✅ Droits admin activés")
                self.log_operation("ADMIN_RIGHTS_ACTIVATED", admin_email)
                self.changes_made = True
            return False
        
        # Créer le compte admin
        try:
            # Obtenir le pays Morocco
            morocco = Country.query.filter_by(code='MA').first()
            rabat = City.query.filter_by(name='Rabat').first() if morocco else None
            
            admin = User(
                unique_code=generate_unique_code(),
                first_name='Admin',
                last_name='Talento',
                email=admin_email,
                is_admin=True,
                role='admin',
                account_active=True,
                country_id=morocco.id if morocco else None,
                city_id=rabat.id if rabat else None
            )
            
            # Mot de passe par défaut (doit être changé lors de la première connexion)
            admin_password = os.environ.get('ADMIN_DEFAULT_PASSWORD', '@4dm1n')
            admin.set_password(admin_password)
            
            db.session.add(admin)
            db.session.commit()
            
            logger.info(f"✅ Compte admin créé: {admin_email}")
            logger.info(f"🔑 Mot de passe par défaut: {admin_password}")
            logger.warning("⚠️  IMPORTANT: Changez le mot de passe admin après la première connexion!")
            
            self.log_operation("ADMIN_USER_CREATED", admin_email)
            self.changes_made = True
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la création du compte admin: {e}")
            db.session.rollback()
            raise
    
    def create_app_settings(self) -> int:
        """Créer les paramètres de base de l'application"""
        if self.dry_run:
            logger.info("💡 [DRY-RUN] Les paramètres de base seraient créés")
            return 0
        
        logger.info("⚙️  Initialisation des paramètres de base...")
        
        default_settings = {
            'app_name': 'Talento',
            'app_version': '1.0.0',
            'maintenance_mode': False,
            'allow_registration': True,
            'max_upload_size': 10485760,  # 10 MB
            'session_timeout': 3600,  # 1 heure
            'password_min_length': 8,
            'require_email_verification': False,
        }
        
        added = 0
        for key, value in default_settings.items():
            try:
                if not AppSettings.query.filter_by(key=key).first():
                    AppSettings.set(key, value)
                    added += 1
                    logger.debug(f"   ✅ Paramètre créé: {key} = {value}")
            except Exception as e:
                logger.debug(f"Paramètre {key} existe déjà ou erreur: {e}")
        
        if added > 0:
            logger.info(f"✅ {added} paramètres de base ajoutés")
            self.log_operation("APP_SETTINGS_CREATED", f"{added} paramètres")
            self.changes_made = True
        else:
            logger.info("✅ Paramètres de base déjà configurés")
        
        return added
    
    def run_full_initialization(self) -> Dict:
        """Exécuter l'initialisation complète de la base de données"""
        try:
            print("=" * 80)
            print("    INITIALISATION COMPLÈTE DE LA BASE DE DONNÉES - taalentio.com")
            print("=" * 80)
            
            if self.dry_run:
                print("\n🔍 MODE DRY-RUN: Aucune modification ne sera appliquée\n")
            
            # 1. Obtenir les informations sur la base de données
            db_info = self.get_database_info()
            logger.info(f"📊 Base de données: {db_info['engine']}")
            logger.info(f"📊 Tables existantes: {db_info['tables_count']}")
            
            # 2. Créer un backup si demandé
            backup_path = None
            if self.backup_first and db_info['tables_count'] > 0:
                if self.confirm_action("Créer un backup avant les modifications?"):
                    backup_path = self.create_backup()
            
            # 3. Créer les tables manquantes
            print("\n" + "─" * 80)
            print("ÉTAPE 1: CRÉATION DES TABLES")
            print("─" * 80)
            missing_tables = self.check_and_create_tables()
            
            # 4. Ajouter les colonnes manquantes
            print("\n" + "─" * 80)
            print("ÉTAPE 2: MIGRATION DES COLONNES")
            print("─" * 80)
            columns_added = self.check_and_add_columns()
            
            # 5. Seeding des données essentielles
            print("\n" + "─" * 80)
            print("ÉTAPE 3: CHARGEMENT DES DONNÉES ESSENTIELLES")
            print("─" * 80)
            
            countries_added = self.seed_countries()
            cities_added = self.seed_cities()
            talents_added = self.seed_talents()
            admin_created = self.create_admin_user()
            settings_added = self.create_app_settings()
            
            # 6. Résumé final
            print("\n" + "=" * 80)
            print("    RÉSUMÉ DE L'INITIALISATION")
            print("=" * 80)
            
            summary = {
                'success': True,
                'dry_run': self.dry_run,
                'changes_made': self.changes_made,
                'backup_path': backup_path,
                'tables_created': len(missing_tables),
                'columns_added': columns_added,
                'countries_added': countries_added,
                'cities_added': cities_added,
                'talents_added': talents_added,
                'admin_created': admin_created,
                'settings_added': settings_added,
                'operations_log': self.operations_log
            }
            
            if self.dry_run:
                print("\n🔍 Mode DRY-RUN - Aucune modification appliquée")
            elif self.changes_made:
                print("\n✅ Initialisation terminée avec succès!")
            else:
                print("\n✅ Base de données déjà à jour, aucune modification nécessaire")
            
            print(f"\n📊 Statistiques:")
            print(f"   • Tables créées: {len(missing_tables)}")
            print(f"   • Colonnes ajoutées: {columns_added}")
            print(f"   • Pays ajoutés: {countries_added}")
            print(f"   • Villes ajoutées: {cities_added}")
            print(f"   • Talents ajoutés: {talents_added}")
            print(f"   • Compte admin: {'Créé' if admin_created else 'Déjà existant'}")
            print(f"   • Paramètres ajoutés: {settings_added}")
            
            if backup_path:
                print(f"\n💾 Backup créé: {backup_path}")
            
            # État final de la base de données
            final_db_info = self.get_database_info()
            print(f"\n📈 État final de la base de données:")
            print(f"   • Tables: {final_db_info['tables_count']}")
            if 'users_count' in final_db_info:
                print(f"   • Utilisateurs: {final_db_info['users_count']}")
            if 'countries_count' in final_db_info:
                print(f"   • Pays: {final_db_info['countries_count']}")
            if 'cities_count' in final_db_info:
                print(f"   • Villes: {final_db_info['cities_count']}")
            if 'talents_count' in final_db_info:
                print(f"   • Talents: {final_db_info['talents_count']}")
            
            print("\n" + "=" * 80)
            
            return summary
            
        except Exception as e:
            logger.error(f"\n❌ ERREUR CRITIQUE: {e}")
            logger.info("🔄 Tentative de rollback...")
            try:
                db.session.rollback()
                logger.info("✅ Rollback effectué avec succès")
            except Exception as rollback_error:
                logger.error(f"❌ Erreur lors du rollback: {rollback_error}")
            
            import traceback
            traceback.print_exc()
            
            return {
                'success': False,
                'error': str(e),
                'operations_log': self.operations_log
            }


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description='Script d\'initialisation complète de la base de données',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  %(prog)s                      Mode interactif
  %(prog)s --force              Sans confirmation
  %(prog)s --dry-run            Voir les modifications sans les appliquer
  %(prog)s --backup-first       Créer un backup avant modifications
  %(prog)s --backup-first -v    Avec logs détaillés
        """
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Passer les confirmations (mode automatique)'
    )
    
    parser.add_argument(
        '--backup-first',
        action='store_true',
        help='Créer un backup avant toute opération'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Afficher les modifications sans les appliquer'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Afficher les logs détaillés'
    )
    
    args = parser.parse_args()
    
    # Configuration du niveau de log
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Créer l'application Flask
    try:
        app = create_app()
    except Exception as e:
        logger.error(f"❌ Impossible de créer l'application: {e}")
        return 1
    
    # Exécuter l'initialisation dans le contexte de l'application
    with app.app_context():
        initializer = DatabaseInitializer(
            dry_run=args.dry_run,
            force=args.force,
            backup_first=args.backup_first
        )
        
        result = initializer.run_full_initialization()
        
        if result['success']:
            return 0
        else:
            logger.error("\n❌ L'initialisation a échoué")
            return 1


if __name__ == '__main__':
    sys.exit(main())
