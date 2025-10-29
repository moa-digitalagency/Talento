# TalentsMaroc.com - Platform for Talent Centralization

## Overview
TalentsMaroc.com is a professional web application designed to centralize and showcase talent profiles across Africa, with a strong focus on the film industry through its CINEMA module. It enables individuals to create comprehensive profiles with unique identifiers and QR codes. The platform features advanced administrative tools, AI-powered CV analysis, and multiple data export formats. TalentsMaroc.com aims to be a robust, scalable solution for talent management and discovery, enhancing professional networking and recruitment. The CINEMA module provides a dedicated system for talent registration with detailed fields, public accessibility, and specialized features for film industry professionals.

## User Preferences
Preferred communication style: Simple, everyday language.

## Recent Changes (October 2025)
- **Logo dans Emails et PDFs** (29 Oct 2025): Ajout systématique du logo TalentsMaroc.com dans tous les emails et exports PDF. Emails: Logo encodé en base64 inclus dans les templates de confirmation d'inscription, identifiants de connexion, et email de test. PDFs: Logo ajouté dans export_list_to_pdf et print_project_talents_list (avec ajustement des positions). Vérification de la présence du logo dans export_talent_card_pdf, export_cinema_talent_card_pdf, et generate_project_badge (déjà présents). Utilise une vérification à deux chemins (app/static/img/logo-full.png et static/img/logo-full.png) pour garantir la compatibilité multi-environnement.
- **Fix: Formulaire Inscription - Champ Nationalité** (29 Oct 2025): Le champ "Nationalité" dans le formulaire d'inscription (`/auth/register`) est maintenant une liste déroulante (select) au lieu d'un champ texte. Le select est automatiquement rempli avec tous les pays du monde via l'API `/api/countries`, avec drapeaux emoji pour chaque pays. Cohérent avec les autres champs de localisation (Pays d'origine, Pays de résidence). Configuration Git repository ajoutée: `https://github.com/moa-digitalagency/Talento.git` pour activer la fonctionnalité de mise à jour depuis les paramètres admin.
- **Script de Mise à Jour Sécurisée** (29 Oct 2025): Nouveau script `update_app.sh` qui permet de mettre à jour l'application sans risque de perte de données. Le script protège automatiquement .env, les bases de données, les uploads, et crée des sauvegardes avant toute modification. Il gère aussi les migrations de schéma de base de données avec Flask-Migrate. Amélioration du .gitignore pour protéger tous les fichiers critiques (.env, *.db, uploads/, backups/). Documentation complète dans `README_UPDATE.md`.
- **Fix: SQLAlchemy Ambiguous Join Error** (29 Oct 2025): Fixed a critical database query error that occurred when loading the admin dashboard. The error was caused by an ambiguous join between the `cities` and `users` tables (User model has two foreign keys to City: `city_id` and `residence_city_id`). The fix explicitly specifies the join conditions in the query: `join(User, City.id == User.city_id).join(Country, Country.id == User.country_id)`. This resolves the `AmbiguousForeignKeysError` when counting top Morocco cities by talent.
- **Désactivation Données de Démo** (28 Oct 2025): Les données de démonstration (utilisateurs et profils CINEMA) ne sont plus chargées automatiquement par le script `migrations_init.py`. Seul le compte admin est créé lors de l'initialisation. Les fonctions de création de démo sont commentées pour garder une base de données propre en production.
- **Champs Nationalité et Résidence** (28 Oct 2025): Ajout des champs "Nationalité", "Pays de résidence" et "Ville de résidence" au formulaire d'édition utilisateur (`/admin/user/<id>/edit`). Les champs utilisent la base de données User existante (nationality, residence_country_id, residence_city_id) et permettent aux administrateurs de gérer les informations de nationalité et de lieu de résidence des talents. Optimisation du démarrage de l'application en désactivant temporairement la création automatique de données démo.
- **Script de Nettoyage de Base de Données** (28 Oct 2025): Nouveau script `clean_all_data.py` pour supprimer toutes les données de démo (utilisateurs, talents CINEMA, productions, projets, présence) tout en préservant les comptes admin et les données de référence (compétences, pays, villes, paramètres). Inclut une gestion sécurisée des transactions avec rollback automatique en cas d'erreur.
- **Désactivation Données de Démo** (28 Oct 2025): La création automatique des productions de démo au démarrage de l'application a été désactivée (`ensure_demo_productions()` commenté dans `app.py`). La base de données reste propre après nettoyage sans recréation automatique.
- **Navigation Basée sur les Rôles** (28 Oct 2025): Implémentation d'un menu de navigation dynamique simplifié qui s'adapte au rôle de l'utilisateur. Les administrateurs voient Dashboard, Talents, Contrats, CINEMA, Présence, Paramètres, Mon Profil, Déconnexion. Les utilisateurs avec rôle "presence" voient Présence, Mon Profil, Déconnexion. Les talents standards voient Accueil, Mon Profil, Déconnexion. Le menu est cohérent sur desktop et mobile.
- **QR Code Multi-Plateforme**: Système de génération de QR codes portable fonctionnant sur Replit, VPS, serveurs dédiés via configuration BASE_URL.
- **Boutons Profil Améliorés**: Page de profil avec 3 boutons principaux (Modifier profil, Télécharger profil, Modifier mot de passe) avec style de contour plein (border-2).
- **Script de Régénération QR Codes** (28 Oct 2025): Nouveau script `regenerate_qrcodes.py` pour régénérer tous les QR codes avec l'URL correcte lors d'un changement d'environnement.
- **Champs Profil Supplémentaires** (28 Oct 2025): Ajout des champs "Langues parlées" (multi-select avec drapeaux) et "Formation & Éducation" (textarea) à la page d'édition de profil utilisateur.
- **Boutons de Retour Accueil** (28 Oct 2025): Ajout d'un bouton "🏠 Retour à l'accueil" dans les pages /talents et /cinema/talents pour faciliter la navigation.
- **Correction Affichage Langues** (28 Oct 2025): Les langues s'affichent maintenant proprement sans guillemets ni crochets, avec support des formats JSON et CSV.
- **Correction PDF Text Wrapping** (28 Oct 2025): Les champs "Langues" et "Éducation" utilisent maintenant le retour à la ligne automatique dans l'export PDF.

## System Architecture

### Application Framework
- **Backend**: Flask 3.0.0 with Python 3.11, utilizing Blueprints for modularity.

### Database Architecture
- **ORM**: SQLAlchemy with Flask-SQLAlchemy, supporting SQLite (development) and PostgreSQL (production).
- **Data Models**: User, Talent, UserTalent, Country, City, AppSettings, CinemaTalent, Production, Project, and ProjectTalent. Sensitive data is encrypted using Fernet. Passwords hashed with Werkzeug.
- **Unique Identification System**:
    - **Main Code**: PPGNNNNVVV (Country, Gender, 4 sequential digits per country, City) - 10 characters.
    - **CINEMA Code**: PPVVVNNNNNG (Country, City, 4 sequential digits per country, Gender) - 11 characters.
    - **Project Code**: CCIIISSSNNN (Country, Production Initials, Project ID, Talent Number) - 10+ characters, no dashes.
    - Both main and CINEMA codes use sequential numbering incremented per country.
    - Codes are distinguished by component order.
- **Automatic Data Seeding**: System creates an admin account (admin@talento.com / MAN0001RAB / @4dm1n) if not present. Demo data creation is disabled by default.
- **Data Cleanup Script**: `clean_all_data.py` - Safely removes all user-generated data (users, CINEMA talents, productions, projects, attendance records) while preserving admin accounts and reference data (skills, countries, cities, system settings). Features transaction rollback protection.

### Authentication & Authorization
- **User Authentication**: Flask-Login, supporting dual login (email OR unique code).
- **Access Control**: Role-based (admin vs. regular users).

### File Management
- **Uploads**: Photos (PNG, JPG, JPEG up to 5MB) and CVs (PDF, DOC, DOCX up to 10MB).
- **Storage**: Files organized into `photos/`, `cvs/`, `qrcodes/` with UUID-based filenames.
- **QR Code Generation**: Portable system using `Config.get_base_url()` supporting Replit (auto-detect via REPLIT_DOMAINS), VPS/production (via BASE_URL env variable), and local development (localhost:5000 fallback). See `DEPLOYMENT_CONFIG.md` for deployment configuration.

### AI Integration
- **CV Analysis**: OpenRouter AI integration analyzes CVs for skills, summaries, and profile scores.

### Data Export & Backup
- **Export Formats**: Excel (XLSX), CSV, and PDF for talent data.
- **Backup & Restore**: Comprehensive system for full application backup and restoration.

### Email System
- **Service**: SendGrid API for transactional emails.
- **Automated Emails**: Includes application confirmation and login credentials for new candidates.

### Frontend Architecture
- **Template Engine**: Jinja2.
- **CSS Framework**: Tailwind CSS (CDN).
- **UI/UX Decisions**: Modern, professional aesthetic with solid colors, multi-step registration forms, role-based dynamic navigation menus (admin/presence/standard user), enhanced profile pages with action buttons (border-2 solid outline style), secure display of initials and QR codes, and consistent use of French labels.

### Routing Structure
- **Blueprints**: Organized into `main`, `auth`, `profile`, `admin`, `api`, `cinema`, `presence`, and `api_v1` for modularity.

### Admin Settings & Configuration
- **Activity Logs** (`/admin/settings/activity-logs`): Real-time tracking of user actions throughout the platform using LoggingService integration. Displays user activity with timestamps, actions, and details.
- **API Keys Management** (`/admin/settings/api-keys`): Centralized management for external service API keys (SendGrid, OpenRouter, OMDB). Features masked display (first 4 + last 4 characters visible) and status indicators for each service.
- **System Settings** (`/admin/settings/system`): Custom HTML head code injection feature allowing administrators to add analytics scripts (Google Analytics, Facebook Pixel), SEO meta tags, or custom CSS/JavaScript to all pages. Uses context processor for site-wide availability with CSRF protection.

### Contract Management
- **Main Contracts Page**: `/contrats` - Accessible from main navigation for all talents. Currently under development with planned features including contract creation, electronic signature, tracking, notifications, archiving, and PDF export.
- **Cinema Contracts Page**: `/cinema/contrats` - Dedicated contracts management for cinema talents. Accessible from cinema module sidebar with same planned features tailored for film industry contracts.

### Attendance Management (Présence)
- **Access Control**: Accessible only by users with `admin` role or `presence` role. Link visible in main navigation.
- **Core Features**:
  - QR code scanning or manual code entry for talent check-in/check-out
  - Automatic detection: First scan of the day = arrival, second scan = departure
  - Bulk actions: "Mark all present" and "Auto departure" for all present talents
  - Project-based attendance tracking linked to CINEMA projects
  - Attendance history view per talent with duration calculations
- **Data Export**: Excel export of attendance records by project with customizable date ranges
- **Database Model**: New `Attendance` model with fields: project_id, cinema_talent_code, check_in_time, check_out_time, recorded_by, date
- **User Roles**: New `role` field added to User model (values: 'user', 'admin', 'presence')

### REST API v1
- **Base URL**: `/api/v1`.
- **Authentication**: Session-based (cookies). CSRF Protection exempt for all API v1 routes.
- **Documentation**: Available in `api_docs/`.
- **Key Endpoints**: Authentication, User management, Talents & Location data, CINEMA specific data and statistics, and Data Exports.

### CINEMA Module Specifics
- **Registration Form**: Public form (`/cinema/register`) with 9 color-coded sections for comprehensive talent data capture.
- **Profile View**: Public profile page (`/cinema/profile/{code}`) mirrors registration, displaying age, encrypted document number, and mapped data.
- **Talents Management**: List page with advanced search filters (12 criteria).
- **Productions Management**: Complete CRUD system for cinematographic production companies (`/cinema/productions`).
- **Projects Management**: System for managing ongoing production projects (`/cinema/projects`), including talent assignment, unique project codes, and badge generation.
- **Features**: Country dropdowns with emoji flags, dynamic city loading, multi-select fields, and constant-populated dropdowns for physical characteristics.
- **UI/UX Style**: Consistent outline button style.

## External Dependencies

### Core Services
- **Database**: PostgreSQL (production), SQLite (development).
- **AI Service**: OpenRouter API.
- **Email Service**: SendGrid API.
- **Movie Database**: OMDB API (optional, for CINEMA module).

### Python Libraries
- **Web Framework & ORM**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail, Flask-Migrate, Flask-WTF.
- **Database**: `psycopg2-binary`.
- **Security**: `cryptography` (for Fernet encryption), `bcrypt` (for password hashing).
- **File Processing**: Pillow, PyPDF2, `python-docx`.
- **Data Export**: `pandas`, `openpyxl`, ReportLab.
- **Email**: `sendgrid`.
- **Utilities**: `qrcode`, `requests`, `email-validator`, `python-dotenv`, `phonenumbers`.