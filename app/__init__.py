import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
csrf = CSRFProtect()

def seed_database():
    """
    Seed the database with initial data (idempotent)
    DEPRECATED: Utiliser migrations_init.py à la place
    """
    import os
    
    # Ne pas lancer migrations_init.py si on est déjà dedans
    if os.environ.get('SKIP_AUTO_MIGRATION') == '1':
        return
    
    import subprocess
    import sys
    try:
        print("🔄 Exécution du script de migration...")
        # Empêcher la récursion infinie
        env = os.environ.copy()
        env['SKIP_AUTO_MIGRATION'] = '1'
        subprocess.run([sys.executable, 'migrations_init.py'], check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Erreur lors de la migration: {e}")
        print("Utilisation du seeding interne de secours...")
        _seed_database_fallback()

def _seed_database_fallback():
    """Seed de secours (ancienne méthode)"""
    from app.models.user import User
    from app.models.talent import Talent
    from app.models.location import Country, City
    
    countries_data = [
        {'name': 'Maroc', 'code': 'MA'},
        {'name': 'Algérie', 'code': 'DZ'},
        {'name': 'Tunisie', 'code': 'TN'},
        {'name': 'Libye', 'code': 'LY'},
        {'name': 'Égypte', 'code': 'EG'},
        {'name': 'Mauritanie', 'code': 'MR'},
        {'name': 'Mali', 'code': 'ML'},
        {'name': 'Sénégal', 'code': 'SN'},
        {'name': 'Gambie', 'code': 'GM'},
        {'name': 'Guinée-Bissau', 'code': 'GW'},
        {'name': 'Guinée', 'code': 'GN'},
        {'name': 'Sierra Leone', 'code': 'SL'},
        {'name': 'Liberia', 'code': 'LR'},
        {'name': 'Côte d\'Ivoire', 'code': 'CI'},
        {'name': 'Ghana', 'code': 'GH'},
        {'name': 'Togo', 'code': 'TG'},
        {'name': 'Bénin', 'code': 'BJ'},
        {'name': 'Nigéria', 'code': 'NG'},
        {'name': 'Niger', 'code': 'NE'},
        {'name': 'Burkina Faso', 'code': 'BF'},
        {'name': 'Cameroun', 'code': 'CM'},
        {'name': 'Tchad', 'code': 'TD'},
        {'name': 'République Centrafricaine', 'code': 'CF'},
        {'name': 'Guinée Équatoriale', 'code': 'GQ'},
        {'name': 'Gabon', 'code': 'GA'},
        {'name': 'Congo', 'code': 'CG'},
        {'name': 'RD Congo', 'code': 'CD'},
        {'name': 'Angola', 'code': 'AO'},
        {'name': 'Soudan', 'code': 'SD'},
        {'name': 'Soudan du Sud', 'code': 'SS'},
        {'name': 'Éthiopie', 'code': 'ET'},
        {'name': 'Érythrée', 'code': 'ER'},
        {'name': 'Djibouti', 'code': 'DJ'},
        {'name': 'Somalie', 'code': 'SO'},
        {'name': 'Kenya', 'code': 'KE'},
        {'name': 'Ouganda', 'code': 'UG'},
        {'name': 'Rwanda', 'code': 'RW'},
        {'name': 'Burundi', 'code': 'BI'},
        {'name': 'Tanzanie', 'code': 'TZ'},
        {'name': 'Malawi', 'code': 'MW'},
        {'name': 'Mozambique', 'code': 'MZ'},
        {'name': 'Zimbabwe', 'code': 'ZW'},
        {'name': 'Zambie', 'code': 'ZM'},
        {'name': 'Botswana', 'code': 'BW'},
        {'name': 'Namibie', 'code': 'NA'},
        {'name': 'Afrique du Sud', 'code': 'ZA'},
        {'name': 'Lesotho', 'code': 'LS'},
        {'name': 'Eswatini', 'code': 'SZ'},
        {'name': 'Madagascar', 'code': 'MG'},
        {'name': 'Maurice', 'code': 'MU'},
        {'name': 'Comores', 'code': 'KM'},
        {'name': 'Seychelles', 'code': 'SC'},
        {'name': 'Cap-Vert', 'code': 'CV'},
        {'name': 'São Tomé-et-Príncipe', 'code': 'ST'},
    ]
    
    for data in countries_data:
        if not Country.query.filter_by(code=data['code']).first():
            country = Country(**data)
            db.session.add(country)
    
    cities_data = [
        {'name': 'Rabat', 'code': 'RAB'},
        {'name': 'Casablanca', 'code': 'CAS'},
        {'name': 'Tanger', 'code': 'TNG'},
        {'name': 'Marrakech', 'code': 'MAR'},
        {'name': 'Fès', 'code': 'FES'},
        {'name': 'Agadir', 'code': 'AGA'},
        {'name': 'Meknès', 'code': 'MEK'},
        {'name': 'Oujda', 'code': 'OUJ'},
        {'name': 'Tétouan', 'code': 'TET'},
        {'name': 'Salé', 'code': 'SAL'},
        {'name': 'Kenitra', 'code': 'KEN'},
        {'name': 'El Jadida', 'code': 'ELJ'},
    ]
    
    for data in cities_data:
        if not City.query.filter_by(code=data['code']).first():
            city = City(**data)
            db.session.add(city)
    
    talents_data = [
        {'name': 'Maçonnerie', 'emoji': '🧱', 'category': 'Construction'},
        {'name': 'Carrelage', 'emoji': '⬜', 'category': 'Construction'},
        {'name': 'Plomberie', 'emoji': '🔧', 'category': 'Construction'},
        {'name': 'Électricité', 'emoji': '⚡', 'category': 'Construction'},
        {'name': 'Menuiserie', 'emoji': '🪚', 'category': 'Construction'},
        {'name': 'Peinture', 'emoji': '🎨', 'category': 'Construction'},
        {'name': 'Soudure', 'emoji': '🔥', 'category': 'Construction'},
        {'name': 'Ferronnerie', 'emoji': '⚒️', 'category': 'Construction'},
        {'name': 'Charpenterie', 'emoji': '🪵', 'category': 'Construction'},
        {'name': 'Toiture', 'emoji': '🏠', 'category': 'Construction'},
        {'name': 'Isolation', 'emoji': '🧰', 'category': 'Construction'},
        {'name': 'Climatisation', 'emoji': '❄️', 'category': 'Construction'},
        {'name': 'Cuisine', 'emoji': '🍳', 'category': 'Restauration'},
        {'name': 'Pâtisserie', 'emoji': '🧁', 'category': 'Restauration'},
        {'name': 'Boulangerie', 'emoji': '🥖', 'category': 'Restauration'},
        {'name': 'Serveur', 'emoji': '🍽️', 'category': 'Restauration'},
        {'name': 'Barista', 'emoji': '☕', 'category': 'Restauration'},
        {'name': 'Chef cuisine', 'emoji': '👨‍🍳', 'category': 'Restauration'},
        {'name': 'Développement Web', 'emoji': '🖥️', 'category': 'Technologie'},
        {'name': 'Développement Mobile', 'emoji': '📱', 'category': 'Technologie'},
        {'name': 'Data Science', 'emoji': '📊', 'category': 'Technologie'},
        {'name': 'IA/ML', 'emoji': '🤖', 'category': 'Technologie'},
        {'name': 'Cybersécurité', 'emoji': '🔒', 'category': 'Technologie'},
        {'name': 'DevOps', 'emoji': '⚙️', 'category': 'Technologie'},
        {'name': 'Maintenance IT', 'emoji': '💻', 'category': 'Technologie'},
        {'name': 'Réseaux', 'emoji': '🌐', 'category': 'Technologie'},
        {'name': 'Graphisme', 'emoji': '🖌️', 'category': 'Créatif'},
        {'name': 'UI/UX Design', 'emoji': '📐', 'category': 'Créatif'},
        {'name': 'Illustration', 'emoji': '✏️', 'category': 'Créatif'},
        {'name': 'Animation 3D', 'emoji': '🎬', 'category': 'Créatif'},
        {'name': 'Motion Design', 'emoji': '🎞️', 'category': 'Créatif'},
        {'name': 'Photographie', 'emoji': '📸', 'category': 'Médias'},
        {'name': 'Vidéographie', 'emoji': '🎥', 'category': 'Médias'},
        {'name': 'Montage vidéo', 'emoji': '🎬', 'category': 'Médias'},
        {'name': 'Rédaction', 'emoji': '📝', 'category': 'Médias'},
        {'name': 'Journalisme', 'emoji': '📰', 'category': 'Médias'},
        {'name': 'Community Management', 'emoji': '📣', 'category': 'Marketing'},
        {'name': 'SEO/SEA', 'emoji': '🔍', 'category': 'Marketing'},
        {'name': 'Marketing digital', 'emoji': '📈', 'category': 'Marketing'},
        {'name': 'Content Marketing', 'emoji': '✍️', 'category': 'Marketing'},
        {'name': 'Email Marketing', 'emoji': '📧', 'category': 'Marketing'},
        {'name': 'Musique', 'emoji': '🎶', 'category': 'Artistique'},
        {'name': 'Chant', 'emoji': '🎤', 'category': 'Artistique'},
        {'name': 'Danse', 'emoji': '💃', 'category': 'Artistique'},
        {'name': 'Théâtre', 'emoji': '🎭', 'category': 'Artistique'},
        {'name': 'Mannequinat', 'emoji': '👗', 'category': 'Artistique'},
        {'name': 'Comédie', 'emoji': '😂', 'category': 'Artistique'},
        {'name': 'Ménage', 'emoji': '🧹', 'category': 'Services'},
        {'name': 'Jardinage', 'emoji': '🌱', 'category': 'Services'},
        {'name': 'Garde d\'enfants', 'emoji': '👶', 'category': 'Services'},
        {'name': 'Aide à domicile', 'emoji': '🏡', 'category': 'Services'},
        {'name': 'Coiffure', 'emoji': '💇', 'category': 'Services'},
        {'name': 'Esthétique', 'emoji': '💅', 'category': 'Services'},
        {'name': 'Chauffeur', 'emoji': '🚗', 'category': 'Transport'},
        {'name': 'Livreur', 'emoji': '🏍️', 'category': 'Transport'},
        {'name': 'Taxi', 'emoji': '🚕', 'category': 'Transport'},
        {'name': 'Enseignant', 'emoji': '👩‍🏫', 'category': 'Éducation'},
        {'name': 'Formation professionnelle', 'emoji': '📚', 'category': 'Éducation'},
        {'name': 'Cours particuliers', 'emoji': '✏️', 'category': 'Éducation'},
        {'name': 'Coaching', 'emoji': '🎯', 'category': 'Éducation'},
        {'name': 'Infirmier', 'emoji': '💉', 'category': 'Santé'},
        {'name': 'Aide-soignant', 'emoji': '🩺', 'category': 'Santé'},
        {'name': 'Pharmacien', 'emoji': '💊', 'category': 'Santé'},
        {'name': 'Vente', 'emoji': '🛍️', 'category': 'Commerce'},
        {'name': 'Commerce', 'emoji': '🏪', 'category': 'Commerce'},
        {'name': 'Caissier', 'emoji': '💰', 'category': 'Commerce'},
        {'name': 'Organisation événements', 'emoji': '🎉', 'category': 'Événementiel'},
        {'name': 'Animation', 'emoji': '🎈', 'category': 'Événementiel'},
        {'name': 'DJ', 'emoji': '🎧', 'category': 'Événementiel'},
        {'name': 'Secrétariat', 'emoji': '📋', 'category': 'Bureautique'},
        {'name': 'Comptabilité', 'emoji': '🧮', 'category': 'Bureautique'},
        {'name': 'Ressources Humaines', 'emoji': '👥', 'category': 'Bureautique'},
        {'name': 'Gestion de projet', 'emoji': '📊', 'category': 'Bureautique'},
    ]
    
    for data in talents_data:
        if not Talent.query.filter_by(name=data['name']).first():
            talent = Talent(**data)
            db.session.add(talent)
    
    admin_email = 'admin@talento.com'
    admin_code = 'MAN0001RAB'
    
    admin = User.query.filter(
        (User.email == admin_email) | (User.unique_code == admin_code)
    ).first()
    
    if not admin:
        morocco = Country.query.filter_by(code='MA').first()
        rabat = City.query.filter_by(code='RAB').first()
        
        if morocco and rabat:
            admin = User()
            admin.first_name = 'Admin'
            admin.last_name = 'taalentio.com'
            admin.email = admin_email
            import os
            admin_password = os.environ.get('ADMIN_PASSWORD', '@4dm1n')
            admin.set_password(admin_password)
            admin.phone = '+212600000000'
            admin.whatsapp = '+212600000000'
            admin.gender = 'N'
            admin.is_admin = True
            admin.unique_code = admin_code
            admin.country_id = morocco.id
            admin.city_id = rabat.id
            db.session.add(admin)
            
            try:
                db.session.commit()
                print(f"✅ Compte admin créé (fallback): {admin_email}")
            except Exception as e:
                db.session.rollback()
                print(f"⚠️  Admin existe déjà ou erreur (fallback): {e}")
        else:
            print("⚠️  Impossible de créer admin - Morocco/Rabat introuvables")
    else:
        print(f"✅ Compte admin existe déjà (fallback): {admin.email}")
        db.session.commit()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    
    @app.template_filter('from_json')
    def from_json_filter(value):
        """Filtre pour parser les chaînes JSON dans les templates"""
        if not value:
            return []
        try:
            import json
            return json.loads(value)
        except (ValueError, TypeError):
            return []
    
    @app.context_processor
    def inject_custom_head_code():
        """Injecter le code personnalisé du <head> dans tous les templates"""
        try:
            from app.models.settings import AppSettings
            custom_head_code = AppSettings.get('custom_head_code', '')
            return {'CUSTOM_HEAD_CODE': custom_head_code}
        except Exception:
            return {'CUSTOM_HEAD_CODE': ''}
    
    from app.routes import auth, profile, admin, main, api, cinema, presence
    from app.routes import api_v1
    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(cinema.bp)
    app.register_blueprint(presence.bp)
    app.register_blueprint(api_v1.bp)
    
    # Exemption CSRF pour toutes les routes API v1
    csrf.exempt(api_v1.bp)
    
    # Désactiver le cache pour éviter les problèmes avec les mises à jour
    @app.after_request
    def add_no_cache_headers(response):
        """Ajouter des en-têtes pour désactiver le cache navigateur"""
        # Ne pas mettre en cache les pages HTML et les données JSON
        if response.content_type and ('text/html' in response.content_type or 'application/json' in response.content_type):
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '-1'
        return response
    
    # Gestionnaire d'erreur 404 pour gérer les URLs mal encodées
    @app.errorhandler(404)
    def handle_404(e):
        from flask import request, redirect, url_for
        # Si l'URL contient %3F (qui est un ? encodé), rediriger vers login
        if '%3F' in request.url or '%2F' in request.url:
            return redirect(url_for('auth.login'))
        # Sinon, retourner une vraie page 404
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>404 - Page non trouvée</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-50 min-h-screen flex items-center justify-center">
            <div class="text-center">
                <h1 class="text-6xl font-bold text-gray-800 mb-4">404</h1>
                <p class="text-xl text-gray-600 mb-8">Page non trouvée</p>
                <a href="{url_for('auth.login')}" class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Retour à l'accueil
                </a>
            </div>
        </body>
        </html>
        ''', 404
    
    with app.app_context():
        try:
            from app.utils.auto_migrate import safe_auto_migrate
            import os
            
            logger = app.logger
            logger.info("🚀 Démarrage de taalentio.com...")
            
            safe_auto_migrate(db)
            
            # Auto-détecter si les données demo doivent être créées
            # Temporarily disabled to speed up startup
            # _ensure_demo_data_exists(db, logger)
            
            # Garantir que le compte admin existe toujours
            _ensure_admin_exists(db, logger)
            
            logger.info("✅ Application prête")
            
        except Exception as e:
            app.logger.error(f"❌ Erreur lors de l'initialisation: {e}")
            app.logger.warning("⚠️ L'application continue malgré l'erreur")
    
    return app

def _ensure_demo_data_exists(db, logger):
    """Créer automatiquement les données demo si elles n'existent pas encore"""
    try:
        from app.models.user import User
        from app.models.cinema_talent import CinemaTalent
        import os
        import subprocess
        import sys
        
        # Vérifier si les données demo existent déjà
        demo_user_exists = User.query.filter(User.email.like('demo%')).first() is not None
        demo_cinema_exists = CinemaTalent.query.filter(CinemaTalent.email.like('%@demo.cinema')).first() is not None
        
        if demo_user_exists and demo_cinema_exists:
            logger.info("✓ Données demo déjà présentes")
            return True
        
        logger.info("🌱 Création automatique des données de démonstration...")
        
        # Exécuter le script de seeding
        env = os.environ.copy()
        env['SKIP_AUTO_MIGRATION'] = '1'  # Éviter la récursion
        
        result = subprocess.run(
            [sys.executable, 'migrations_init.py'],
            env=env,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            logger.info("✅ Données de démonstration créées avec succès")
            return True
        else:
            logger.warning(f"⚠️ Erreur lors de la création des données demo: {result.stderr[:200]}")
            return False
            
    except Exception as e:
        logger.warning(f"⚠️ Impossible de créer les données demo: {e}")
        return False

def _ensure_admin_exists(db, logger):
    """Garantir que le compte admin existe avec les bons identifiants"""
    try:
        from app.models.user import User
        from app.models.location import Country, City
        import os
        
        # ÉTAPE 1: Garantir que Morocco et Rabat existent (OBLIGATOIRE pour créer l'admin)
        morocco = Country.query.filter_by(code='MA').first()
        if not morocco:
            logger.info("🌍 Création du pays Morocco (requis pour admin)...")
            morocco = Country(name='Maroc', code='MA')
            db.session.add(morocco)
            db.session.commit()
            logger.info("✅ Maroc créé")
        
        rabat = City.query.filter_by(code='RAB').first()
        if not rabat:
            logger.info("🏙️ Création de la ville Rabat (requis pour admin)...")
            rabat = City(name='Rabat', code='RAB')
            db.session.add(rabat)
            db.session.commit()
            logger.info("✅ Rabat créé")
        
        # ÉTAPE 2: Créer ou mettre à jour l'admin
        admin_email = 'admin@talento.com'
        admin_code = 'MAN0001RAB'
        admin_password = os.environ.get('ADMIN_PASSWORD')
        if not admin_password:
            logger.warning("⚠️ ADMIN_PASSWORD non défini dans .env - impossible de créer/mettre à jour l'admin")
            return
        
        admin = User.query.filter(
            (User.email == admin_email) | (User.unique_code == admin_code)
        ).first()
        
        if not admin:
            logger.info("👤 Création du compte admin...")
            morocco = Country.query.filter_by(code='MA').first()
            rabat = City.query.filter_by(code='RAB').first()
            
            if morocco and rabat:
                admin = User(
                    email=admin_email,
                    first_name='Admin',
                    last_name='Talento',
                    unique_code=admin_code,
                    is_admin=True,
                    account_active=True,
                    country_id=morocco.id,
                    city_id=rabat.id,
                    gender='N'
                )
                admin.set_password(admin_password)
                admin.phone = '+212600000000'
                db.session.add(admin)
                db.session.commit()
                logger.info(f"✅ Admin créé: {admin_email} / {admin_code}")
            else:
                logger.warning("⚠️  Impossible de créer admin - Morocco/Rabat manquants")
        else:
            # Vérifier et corriger le mot de passe si nécessaire
            if not admin.check_password(admin_password):
                admin.set_password(admin_password)
                db.session.commit()
                logger.info(f"🔐 Mot de passe admin mis à jour")
            if not admin.is_admin:
                admin.is_admin = True
                db.session.commit()
                logger.info(f"👑 Droits admin activés")
            else:
                logger.info(f"✅ Compte admin OK: {admin_email}")
    except Exception as e:
        logger.error(f"⚠️  Erreur lors de la vérification admin: {e}")

def ensure_essential_data(db, logger=None):
    """
    Vérifie et charge automatiquement les données essentielles au démarrage
    Cette fonction s'assure que les pays, villes et talents sont toujours chargés
    """
    try:
        from app.models.location import Country, City
        from app.models.talent import Talent
        import subprocess
        import sys
        
        # Seuil minimum attendu pour chaque type de données
        MIN_COUNTRIES = 100  # Au moins 100 pays
        MIN_CITIES = 1000    # Au moins 1000 villes
        MIN_TALENTS = 50     # Au moins 50 talents
        
        # Compter les données actuelles
        countries_count = Country.query.count()
        cities_count = City.query.count()
        cities_with_country = City.query.filter(City.country_id.isnot(None)).count()
        talents_count = Talent.query.count()
        
        print("📊 Vérification des données essentielles...")
        print(f"   Pays: {countries_count} (min: {MIN_COUNTRIES})")
        print(f"   Villes: {cities_count} (min: {MIN_CITIES}, avec pays: {cities_with_country})")
        print(f"   Talents: {talents_count} (min: {MIN_TALENTS})")
        
        # Vérifier si les données sont insuffisantes
        needs_reload = (
            countries_count < MIN_COUNTRIES or
            cities_count < MIN_CITIES or
            cities_with_country < MIN_CITIES or
            talents_count < MIN_TALENTS
        )
        
        if needs_reload:
            print("⚠️  Données essentielles manquantes ou incomplètes!")
            print("🔄 Chargement automatique des données du monde...")
            
            # Empêcher la récursion infinie
            if os.environ.get('SKIP_AUTO_MIGRATION') == '1':
                print("⚠️  Auto-migration déjà en cours, arrêt pour éviter la récursion")
                return False
            
            # Appeler le script de migration
            env = os.environ.copy()
            env['SKIP_AUTO_MIGRATION'] = '1'
            
            result = subprocess.run(
                [sys.executable, 'migrations_init.py'],
                env=env,
                capture_output=True,
                text=True,
                timeout=180
            )
            
            if result.returncode == 0:
                print("✅ Données essentielles chargées avec succès")
                
                # Recompter pour confirmer
                countries_count = Country.query.count()
                cities_count = City.query.count()
                talents_count = Talent.query.count()
                print(f"📊 Nouvelles statistiques:")
                print(f"   Pays: {countries_count}")
                print(f"   Villes: {cities_count}")
                print(f"   Talents: {talents_count}")
                return True
            else:
                print(f"❌ Erreur lors du chargement des données: {result.stderr[:300]}")
                return False
        else:
            print("✅ Toutes les données essentielles sont présentes")
            return True
            
    except Exception as e:
        print(f"⚠️  Erreur lors de la vérification des données essentielles: {e}")
        return False
