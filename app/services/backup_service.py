"""
Service de sauvegarde et restauration complète de l'application TalentsMaroc.com
Permet de créer des backups complets et de restaurer l'application
"""
import os
import json
import zipfile
import shutil
from datetime import datetime
from flask import current_app
from app import db
from app.models.user import User
from app.models.talent import Talent, UserTalent
from app.models.location import Country, City
from app.models.settings import AppSettings
import tempfile


class BackupService:
    """Service de sauvegarde et restauration"""
    
    @staticmethod
    def list_backups():
        """
        Lister les sauvegardes disponibles
        Retourne une liste de dictionnaires avec les informations sur chaque backup
        """
        # Pour l'instant, retourne une liste vide
        # Cette fonctionnalité peut être développée pour lister les backups stockés
        return []
    
    @staticmethod
    def create_full_backup():
        """
        Créer une sauvegarde complète de l'application
        Retourne un tuple (zip_path, temp_dir) pour permettre le nettoyage après envoi
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'talento_backup_{timestamp}'
        
        # Créer un dossier temporaire pour préparer le backup
        temp_dir = tempfile.mkdtemp()
        backup_dir = os.path.join(temp_dir, backup_name)
        os.makedirs(backup_dir)
        
        try:
            # 1. Exporter les données de la base de données (DÉCRYPTÉES)
            BackupService._export_database(backup_dir)
            
            # 2. Copier les fichiers uploadés
            BackupService._export_uploaded_files(backup_dir)
            
            # 3. Exporter la configuration
            BackupService._export_configuration(backup_dir)
            
            # 4. Créer le fichier manifest (métadonnées du backup)
            BackupService._create_manifest(backup_dir)
            
            # 5. Créer le fichier ZIP
            zip_path = os.path.join(temp_dir, f'{backup_name}.zip')
            BackupService._create_zip(backup_dir, zip_path)
            
            # Retourner le chemin ET le temp_dir pour nettoyage ultérieur
            return zip_path, temp_dir
            
        except Exception as e:
            # Nettoyer en cas d'erreur
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            raise Exception(f"Erreur lors de la création du backup: {str(e)}")
    
    @staticmethod
    def _export_database(backup_dir):
        """Exporter toutes les données de la base de données (DÉCRYPTÉES)"""
        data_dir = os.path.join(backup_dir, 'database')
        os.makedirs(data_dir)
        
        # Exporter les utilisateurs avec données DÉCRYPTÉES
        users_data = []
        for user in User.query.all():
            user_dict = {
                'id': user.id,
                'unique_code': user.unique_code,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'password_hash': user.password_hash,
                'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
                'gender': user.gender,
                
                # Données DÉCRYPTÉES
                'phone': user.phone,
                'whatsapp': user.whatsapp,
                'address': user.address,
                'passport_number': user.passport_number,
                'residence_card': user.residence_card,
                
                'country_id': user.country_id,
                'city_id': user.city_id,
                'photo_filename': user.photo_filename,
                'cv_filename': user.cv_filename,
                'portfolio_url': user.portfolio_url,
                
                # Réseaux sociaux DÉCRYPTÉS
                'linkedin': user.linkedin,
                'instagram': user.instagram,
                'twitter': user.twitter,
                'facebook': user.facebook,
                'tiktok': user.tiktok,
                'youtube': user.youtube,
                'github': user.github,
                'behance': user.behance,
                'dribbble': user.dribbble,
                'pinterest': user.pinterest,
                'snapchat': user.snapchat,
                'telegram': user.telegram,
                
                'bio': user.bio,
                'years_experience': user.years_experience,
                'profile_score': user.profile_score,
                'availability': user.availability,
                'work_mode': user.work_mode,
                'rate_range': user.rate_range,
                'languages': user.languages,
                'education': user.education,
                'cv_analysis': user.cv_analysis,
                'cv_analyzed_at': user.cv_analyzed_at.isoformat() if user.cv_analyzed_at else None,
                'is_admin': user.is_admin,
                'account_active': user.account_active,
                'qr_code_filename': user.qr_code_filename,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None,
            }
            users_data.append(user_dict)
        
        with open(os.path.join(data_dir, 'users.json'), 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
        
        # Exporter les talents
        talents_data = []
        for talent in Talent.query.all():
            talents_data.append({
                'id': talent.id,
                'name': talent.name,
                'category': talent.category,
                'emoji': talent.emoji
            })
        
        with open(os.path.join(data_dir, 'talents.json'), 'w', encoding='utf-8') as f:
            json.dump(talents_data, f, ensure_ascii=False, indent=2)
        
        # Exporter les associations user-talent
        user_talents_data = []
        for ut in UserTalent.query.all():
            user_talents_data.append({
                'user_id': ut.user_id,
                'talent_id': ut.talent_id
            })
        
        with open(os.path.join(data_dir, 'user_talents.json'), 'w', encoding='utf-8') as f:
            json.dump(user_talents_data, f, ensure_ascii=False, indent=2)
        
        # Exporter les pays
        countries_data = []
        for country in Country.query.all():
            countries_data.append({
                'id': country.id,
                'name': country.name,
                'code': country.code
            })
        
        with open(os.path.join(data_dir, 'countries.json'), 'w', encoding='utf-8') as f:
            json.dump(countries_data, f, ensure_ascii=False, indent=2)
        
        # Exporter les villes
        cities_data = []
        for city in City.query.all():
            cities_data.append({
                'id': city.id,
                'name': city.name,
                'code': city.code,
                'country_id': city.country_id
            })
        
        with open(os.path.join(data_dir, 'cities.json'), 'w', encoding='utf-8') as f:
            json.dump(cities_data, f, ensure_ascii=False, indent=2)
        
        # Exporter les paramètres (settings)
        settings_data = []
        for setting in AppSettings.query.all():
            settings_data.append({
                'id': setting.id,
                'key': setting.key,
                'value': setting.value
            })
        
        with open(os.path.join(data_dir, 'settings.json'), 'w', encoding='utf-8') as f:
            json.dump(settings_data, f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def _export_uploaded_files(backup_dir):
        """Copier tous les fichiers uploadés"""
        uploads_source = os.path.join('app', 'static', 'uploads')
        uploads_dest = os.path.join(backup_dir, 'uploads')
        
        if os.path.exists(uploads_source):
            shutil.copytree(uploads_source, uploads_dest)
    
    @staticmethod
    def _export_configuration(backup_dir):
        """Exporter la configuration de l'application"""
        config_data = {
            'backup_version': '1.0',
            'app_name': 'TalentsMaroc.com',
            'backup_date': datetime.now().isoformat(),
            'database_type': 'sqlite',  # ou PostgreSQL selon config
        }
        
        with open(os.path.join(backup_dir, 'config.json'), 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def _create_manifest(backup_dir):
        """Créer le fichier manifest avec les métadonnées du backup"""
        manifest = {
            'backup_date': datetime.now().isoformat(),
            'app_version': '1.0',
            'backup_format_version': '1.0',
            'total_users': User.query.count(),
            'total_talents': Talent.query.count(),
            'total_countries': Country.query.count(),
            'total_cities': City.query.count(),
        }
        
        with open(os.path.join(backup_dir, 'manifest.json'), 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def _create_zip(source_dir, zip_path):
        """Créer le fichier ZIP"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
    
    @staticmethod
    def restore_from_backup(zip_path):
        """
        Restaurer l'application depuis un fichier de backup
        ATTENTION: Cette opération va REMPLACER toutes les données existantes
        """
        temp_dir = tempfile.mkdtemp()
        
        try:
            # 1. Extraire le ZIP avec validation des chemins (protection Zip Slip)
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                # Valider tous les chemins avant extraction
                for member in zipf.namelist():
                    # Normaliser le chemin
                    member_path = os.path.normpath(os.path.join(temp_dir, member))
                    # Vérifier qu'il reste dans temp_dir (pas de traversée)
                    if not member_path.startswith(temp_dir):
                        raise Exception(f"Chemin suspect détecté dans le ZIP: {member}")
                zipf.extractall(temp_dir)
            
            # 2. Vérifier le manifest
            manifest_path = os.path.join(temp_dir, 'manifest.json')
            if not os.path.exists(manifest_path):
                raise Exception("Fichier de backup invalide: manifest.json manquant")
            
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            # 3. Restaurer dans une transaction complète
            try:
                # Nettoyer la base de données actuelle
                BackupService._clear_database()
                
                # Restaurer les données
                BackupService._restore_database(temp_dir)
                
                # Réinitialiser les séquences de clés primaires
                BackupService._reset_sequences()
                
                # Commit de la transaction
                db.session.commit()
                
            except Exception as e:
                # Rollback en cas d'erreur
                db.session.rollback()
                raise Exception(f"Erreur lors de la restauration de la base de données: {str(e)}")
            
            # 4. Restaurer les fichiers uploadés (après succès de la DB)
            BackupService._restore_uploaded_files(temp_dir)
            
            return {
                'success': True,
                'message': 'Restauration réussie',
                'manifest': manifest
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la restauration: {str(e)}")
        
        finally:
            # Nettoyer le dossier temporaire
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    @staticmethod
    def _clear_database():
        """Supprimer toutes les données de la base de données"""
        # Ordre important pour respecter les contraintes de clé étrangère
        UserTalent.query.delete()
        User.query.delete()
        AppSettings.query.delete()
        # Ne pas supprimer les talents, pays et villes de base
        db.session.commit()
    
    @staticmethod
    def _restore_database(backup_dir):
        """Restaurer les données de la base de données"""
        data_dir = os.path.join(backup_dir, 'database')
        
        # Restaurer les utilisateurs avec RECHIFFREMENT des données sensibles
        users_file = os.path.join(data_dir, 'users.json')
        if os.path.exists(users_file):
            with open(users_file, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            for user_dict in users_data:
                user = User()
                user.id = user_dict['id']
                user.unique_code = user_dict['unique_code']
                user.first_name = user_dict['first_name']
                user.last_name = user_dict['last_name']
                user.email = user_dict['email']
                user.password_hash = user_dict['password_hash']
                
                if user_dict.get('date_of_birth'):
                    from datetime import date
                    try:
                        user.date_of_birth = date.fromisoformat(user_dict['date_of_birth'])
                    except (ValueError, TypeError):
                        user.date_of_birth = None
                
                user.gender = user_dict.get('gender')
                
                # RECHIFFRER les données sensibles
                user.phone = user_dict.get('phone')
                user.whatsapp = user_dict.get('whatsapp')
                user.address = user_dict.get('address')
                user.passport_number = user_dict.get('passport_number')
                user.residence_card = user_dict.get('residence_card')
                
                user.country_id = user_dict.get('country_id')
                user.city_id = user_dict.get('city_id')
                user.photo_filename = user_dict.get('photo_filename')
                user.cv_filename = user_dict.get('cv_filename')
                user.portfolio_url = user_dict.get('portfolio_url')
                
                # RECHIFFRER les réseaux sociaux
                user.linkedin = user_dict.get('linkedin')
                user.instagram = user_dict.get('instagram')
                user.twitter = user_dict.get('twitter')
                user.facebook = user_dict.get('facebook')
                user.tiktok = user_dict.get('tiktok')
                user.youtube = user_dict.get('youtube')
                user.github = user_dict.get('github')
                user.behance = user_dict.get('behance')
                user.dribbble = user_dict.get('dribbble')
                user.pinterest = user_dict.get('pinterest')
                user.snapchat = user_dict.get('snapchat')
                user.telegram = user_dict.get('telegram')
                
                user.bio = user_dict.get('bio')
                user.years_experience = user_dict.get('years_experience')
                user.profile_score = user_dict.get('profile_score')
                user.availability = user_dict.get('availability')
                user.work_mode = user_dict.get('work_mode')
                user.rate_range = user_dict.get('rate_range')
                user.languages = user_dict.get('languages')
                user.education = user_dict.get('education')
                user.cv_analysis = user_dict.get('cv_analysis')
                
                if user_dict.get('cv_analyzed_at'):
                    try:
                        user.cv_analyzed_at = datetime.fromisoformat(user_dict['cv_analyzed_at'])
                    except (ValueError, TypeError):
                        user.cv_analyzed_at = None
                
                user.is_admin = user_dict.get('is_admin', False)
                user.account_active = user_dict.get('account_active', True)
                user.qr_code_filename = user_dict.get('qr_code_filename')
                
                if user_dict.get('created_at'):
                    try:
                        user.created_at = datetime.fromisoformat(user_dict['created_at'])
                    except (ValueError, TypeError):
                        pass
                if user_dict.get('updated_at'):
                    try:
                        user.updated_at = datetime.fromisoformat(user_dict['updated_at'])
                    except (ValueError, TypeError):
                        pass
                
                db.session.add(user)
            
            db.session.commit()
        
        # Restaurer les associations user-talent
        user_talents_file = os.path.join(data_dir, 'user_talents.json')
        if os.path.exists(user_talents_file):
            with open(user_talents_file, 'r', encoding='utf-8') as f:
                user_talents_data = json.load(f)
            
            for ut_dict in user_talents_data:
                ut = UserTalent(
                    user_id=ut_dict['user_id'],
                    talent_id=ut_dict['talent_id']
                )
                db.session.add(ut)
            
            db.session.commit()
        
        # Restaurer les settings
        settings_file = os.path.join(data_dir, 'settings.json')
        if os.path.exists(settings_file):
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings_data = json.load(f)
            
            for setting_dict in settings_data:
                setting = AppSettings(
                    key=setting_dict['key'],
                    value=setting_dict['value']
                )
                db.session.add(setting)
            
            db.session.commit()
    
    @staticmethod
    def _reset_sequences():
        """Réinitialiser les séquences de clés primaires après restauration"""
        try:
            # Obtenir le type de base de données
            db_uri = db.engine.url
            
            if 'postgresql' in str(db_uri):
                # PostgreSQL - Réinitialiser les séquences
                db.session.execute(db.text("SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 1))"))
                db.session.execute(db.text("SELECT setval('app_settings_id_seq', COALESCE((SELECT MAX(id) FROM app_settings), 1))"))
                db.session.commit()
            elif 'sqlite' in str(db_uri):
                # SQLite - Les séquences sont gérées automatiquement via AUTOINCREMENT
                # Mais on peut forcer la mise à jour de sqlite_sequence
                db.session.execute(db.text("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM users) WHERE name = 'users'"))
                db.session.execute(db.text("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM app_settings) WHERE name = 'app_settings'"))
                db.session.commit()
        except Exception as e:
            current_app.logger.warning(f"Impossible de réinitialiser les séquences: {e}")
            # Ne pas bloquer la restauration si la réinitialisation des séquences échoue
    
    @staticmethod
    def _restore_uploaded_files(backup_dir):
        """Restaurer les fichiers uploadés"""
        uploads_source = os.path.join(backup_dir, 'uploads')
        uploads_dest = os.path.join('app', 'static', 'uploads')
        
        if os.path.exists(uploads_source):
            # Supprimer l'ancien dossier uploads
            if os.path.exists(uploads_dest):
                shutil.rmtree(uploads_dest)
            
            # Copier le nouveau
            shutil.copytree(uploads_source, uploads_dest)
