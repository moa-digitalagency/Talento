# TalentsMaroc.com - Platform for Talent Centralization

## Overview
TalentsMaroc.com is a professional web application designed to centralize and showcase talent profiles across Africa, with a strong focus on the film industry through its CINEMA module. It enables individuals to create comprehensive profiles with unique identifiers and QR codes. The platform features advanced administrative tools, AI-powered CV analysis, and multiple data export formats. TalentsMaroc.com aims to be a robust, scalable solution for talent management and discovery, enhancing professional networking and recruitment. The CINEMA module provides a dedicated system for talent registration with detailed fields, public accessibility, and specialized features for film industry professionals.

## Recent Changes (October 26, 2025)
- **Profile System Implementation (v2.19.0)**: Complete user profile system with:
  - Profile viewing route (`/profile/`) with automatic type detection (admin, regular talent, or cinema talent)
  - Profile editing with locked fields: identity (name, age), email, and ID documents cannot be modified by users
  - Comprehensive edit form (`/profile/edit`) with sections for photo, contact, professional info, skills, CV, and social media
  - All profile sections use colorful dotted-border design (border-2 border-dashed) consistent with CINEMA module
  - "Profil" navigation link added before "Déconnexion" in both desktop and mobile menus
- **Email Notifications (v2.19.0)**: Automatic email system for new talent registrations:
  - Regular talents (via `/auth/register`) automatically receive confirmation email and login credentials (unique code + password)
  - CINEMA talents (via `/cinema/register`) now automatically get a User account created and receive login credentials email
  - Both registration processes use SendGrid API via `email_service.send_login_credentials()` and `send_application_confirmation()`
  - Passwords are randomly generated using `generate_random_password()` from `app.utils.email_service`
- **Dual Email Support (v2.19.0)**: Email constraint modified to allow dual usage:
  - Removed `unique=True` constraint from User.email field in database model
  - Same email can now be used for both regular talent AND cinema talent accounts
  - Unique identifier remains the code (PPGNNNNVVV for regular, PPVVVNNNNNG for cinema)
  - Login system supports both email and unique code as identifiers
- **CINEMA Auto-Account Creation (v2.19.0)**: When a cinema talent registers:
  - System automatically creates a corresponding User account with same email and cinema unique code
  - User account enables cinema talents to log in and manage their profile
  - QR code and profile photo are synchronized between CinemaTalent and User records
- **Codification System Update**: Changed code formats to new specifications:
  - **Main codes**: Now PPGNNNNVVV (was PPVVVNNNNG) with sequential numbering per country
  - **CINEMA codes**: Now PPVVVNNNNNG (11 chars with 4 digits, was 12 chars with 6 digits) with sequential numbering per country
  - **Project codes**: Format CCIIISSSNNN without dashes (no tirets)
  - Both systems now use country-based incrementation (not random)
  - Codes distinguished by component order for clear differentiation
- **Documentation Restructure**: Created comprehensive technical documentation in `docs/TECHNICAL_DOCUMENTATION.md` containing complete system architecture, models, services, routes, security details, and installation instructions.
- **New README Files**: Completely rewrote README.md and README.fr.md with detailed feature descriptions, use cases, installation guide, and roadmap. The new READMEs provide a complete overview of all platform capabilities for both technical and non-technical users.
- **Documentation Organization**: Separated technical documentation from user-facing README to improve clarity and accessibility.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### Application Framework
- **Backend**: Flask 3.0.0 with Python 3.11, utilizing Blueprints for modularity.

### Database Architecture
- **ORM**: SQLAlchemy with Flask-SQLAlchemy, supporting SQLite (development) and PostgreSQL (production).
- **Data Models**: User, Talent, UserTalent, Country, City, AppSettings, CinemaTalent, Production, Project, and ProjectTalent, with sensitive data encrypted using Fernet.
- **Security**: Passwords hashed with Werkzeug. AppSettings stores configurations securely.
- **Recent Schema Updates (v2.16.0)**: Added website, imdb_url_encrypted, and threads_encrypted fields to User and CinemaTalent models for enhanced profile information.
- **Productions Module (v2.17.0)**: New Production model for managing cinematographic production companies with comprehensive fields including basic info (title, type, genre), production details (director, producer, company), dates (production year, release, shooting), descriptions, budget/box-office, media links, technical info, and status tracking.
- **Projects Module (v2.18.0)**: New Project and ProjectTalent models for managing ongoing production projects. Project model includes production details, company link, dates, locations, and status. ProjectTalent model manages talent assignments to projects with unique project codes (PRJ-XXX-YYY format), role types, and badge generation capability. Each talent assignment gets an auto-generated unique code and can have a downloadable PDF badge.
- **Automatic Data Seeding**: System automatically detects if demo data exists on startup. If missing, creates 5 demo users (demo1-5@talento.com), 3 CINEMA talents (emails ending with @demo.cinema) via `migrations_init.py`, and 2 demo productions (film and series). Idempotent design prevents duplicate creation. Admin account (admin@talento.com / MAN0001RAB / @4dm1n) is always guaranteed to exist with required Morocco/Rabat locations.

### Unique Identification System
- **Main Code Format**: PPGNNNNVVV (Country, Gender, 4 sequential digits per country, City) - 10 characters total.
- **CINEMA Code Format**: PPVVVNNNNNG (Country, City, 4 sequential digits per country, Gender) - 11 characters total.
- **Project Code Format**: CCIIISSSNNN (Country, Production Initials, Project ID, Talent Number) - 10+ characters, no dashes.
- **Numbering**: Both main and CINEMA codes use sequential numbering incremented per country (not per city).
- **Distinction**: Codes distinguished by component order - Genre before Number for main codes, City before Number for CINEMA codes.
- **QR Codes**: Automatically generated and linked to profile URLs for both main and CINEMA profiles.

### Authentication & Authorization
- **User Authentication**: Flask-Login, supporting dual login (email OR unique code).
- **Access Control**: Role-based (admin vs. regular users), with admins managing all users and candidates managing their own profiles.

### File Management
- **Uploads**: Supports photos (PNG, JPG, JPEG up to 5MB) and CVs (PDF, DOC, DOCX up to 10MB).
- **Storage**: Files organized into `photos/`, `cvs/`, `qrcodes/` with UUID-based filenames.

### AI Integration
- **CV Analysis**: OpenRouter AI integration analyzes uploaded CVs to extract skills, generate summaries, and assign a profile score (0-100).

### Data Export & Backup
- **Export Formats**: Supports Excel (XLSX), CSV, and PDF for talent data.
- **Backup & Restore**: Comprehensive system for full application backup into encrypted ZIP archives and restoration.

### Email System
- **Service**: SendGrid API for transactional emails, with configurable API keys and sender email.
- **Automated Emails**: Includes application confirmation and login credentials for new candidates.

### Frontend Architecture
- **Template Engine**: Jinja2.
- **CSS Framework**: Tailwind CSS (CDN).
- **UI/UX Decisions**: Modern, professional aesthetic with solid colors, multi-step registration forms, role-adapted dashboards, enhanced individual profile pages with secure display of initials and QR codes, streamlined navigation, and consistent use of French labels. Public CINEMA registration form mirrors main design.

### Routing Structure
- **Blueprints**: Organized into `main`, `auth`, `profile`, `admin`, `api`, `cinema`, and `api_v1` for modularity.

### REST API v1
- **Base URL**: `/api/v1`.
- **Authentication**: Session-based (cookies).
- **CSRF Protection**: Exempt for all API v1 routes.
- **Documentation**: Available in `api_docs/` (French & English).
- **Key Endpoints**: Authentication, User management, Talents & Location data, CINEMA specific data and statistics, and Data Exports.

### CINEMA Module Specifics
- **Registration Form**: Public form (`/cinema/register`) organized into 9 color-coded sections for identity & contact, origins, residence, languages, physical characteristics, talent types (13 options with multi-select), talents (categorized), social networks (encrypted including Telegram), and photos/productions. All buttons use outline style (border-2 with hover:bg-fill).
- **Profile View**: Public profile page (`/cinema/profile/{code}`) mirrors the registration form structure with 9 sections, displaying age (not birth date), encrypted document number, separated contact block, and correctly mapped data (ethnicities in Origins, talent types vs. competences separated).
- **Talents Management**: Talents list page displays Photo, Nom, Ethnicité (first ethnicity + count), Type de talent (first type + count), and Actions (outline "Voir plus" button). Advanced search filter with 12 criteria: name, talent type, gender, age range, ethnicity, eye color, hair color, skin tone, height, country, languages, and experience level.
- **Productions Management**: Complete CRUD system for cinematographic production companies accessible at `/cinema/productions`. Features include: grid-based productions list with poster display, detailed production view with all metadata, comprehensive creation/editing form with organized sections (basic info, production details, dates, descriptions, budget/revenues, media links), soft-delete functionality, and integration with external databases (IMDb, TMDb). Routes: list (`/cinema/productions`), create (`/cinema/productions/new`), view (`/cinema/productions/<id>`), edit (`/cinema/productions/<id>/edit`), delete (`/cinema/productions/<id>/delete`).
- **Projects Management**: Complete system for managing ongoing production projects at `/cinema/projects`. Project model includes: production name, type (film, série, publicité, etc.), production company link, origin country, estimated start/end dates, shooting locations, and status tracking (en_preparation, en_tournage, post_production, termine). Each project can have multiple assigned talents with unique project codes (PRJ-XXX-YYY format), role types, and role descriptions. Features include: project creation/editing forms, detailed project view with talent assignment interface, automatic project code generation for each assigned talent, and badge generation for project talents. Routes: list (`/cinema/projects`), create (`/cinema/projects/new`), view/manage talents (`/cinema/projects/<id>`), edit (`/cinema/projects/<id>/edit`), delete (`/cinema/projects/<id>/delete`), assign talent (`/cinema/projects/<id>/assign-talent`), remove talent (`/cinema/projects/<id>/remove-talent/<pt_id>`), generate badge (`/cinema/projects/talent/<pt_id>/generate-badge`).
- **Features**: Country dropdowns with emoji flags, dynamic city loading, multi-select fields for ethnicities, languages, and talents. All physical characteristic dropdowns (eyes, hair color/type, skin tone, build) are populated from constants. JSON data parsing via custom `from_json` Jinja2 filter.
- **TMDb Integration**: Optional server-side API proxy for movie/TV show search in production history, with real-time search and poster display.
- **Data Model**: `CinemaTalent` model includes personal info with encrypted ID document number, origins vs. residence, physical characteristics, JSON arrays for languages/talent_types/other_talents, encrypted contact/social media (including Telegram), website field (non-encrypted), photo storage, and previous productions as JSON. `Production` model includes comprehensive fields for managing film/TV productions with metadata, scheduling, budgets, and external references.
- **Valid Data Values**: Ethnicities from predefined list (Africaine, Arabe, Berbère, Caucasienne/Blanche, etc.), Talent types from CINEMA_TALENT_TYPES constant (Acteur/Actrice Principal(e), Acteur/Actrice Secondaire, Figurant(e), Silhouette, Doublure, Doublure Lumière, Cascadeur/Cascadeuse, Mannequin, Voix Off, Figurant Spécialisé, Choriste, Danseur/Danseuse de fond, Autre). Production types: Film, Série, Court-métrage, Documentaire, Téléfilm, Animation.
- **UI/UX Style**: Consistent outline button style throughout cinema module for better visual hierarchy and modern appearance.

## External Dependencies

### Core Services
- **Database**: PostgreSQL (production), SQLite (development).
- **AI Service**: OpenRouter API.
- **Email Service**: SendGrid API.
- **Movie Database**: TMDb API (optional, for CINEMA module).

### Python Libraries
- **Web Framework & ORM**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail, Flask-Migrate, Flask-WTF.
- **Database**: `psycopg2-binary`.
- **Security**: `cryptography` (for Fernet encryption), `bcrypt` (for password hashing), Flask-WTF.
- **File Processing**: Pillow, PyPDF2, `python-docx`.
- **Data Export**: `pandas`, `openpyxl`, ReportLab.
- **Email**: `sendgrid`.
- **Utilities**: `qrcode`, `requests`, `email-validator`, `python-dotenv`.

### Configuration Requirements
- **Environment Variables**: `SECRET_KEY`, `DATABASE_URL`, `ENCRYPTION_KEY` are required. Optional variables include `SENDGRID_API_KEY`, `OPENROUTER_API_KEY`, `SENDGRID_FROM_EMAIL`, `REPLIT_DEV_DOMAIN`, `TMDB_API_KEY`. API keys can also be managed via admin settings.