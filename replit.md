# TalentsMaroc.com - Platform for Talent Centralization

## Overview
TalentsMaroc.com is a professional web application designed to centralize and showcase talent profiles across Africa, with a strong focus on the film industry through its CINEMA module. It enables individuals to create comprehensive profiles with unique identifiers and QR codes. The platform features advanced administrative tools, AI-powered CV analysis, and multiple data export formats. TalentsMaroc.com aims to be a robust, scalable solution for talent management and discovery, enhancing professional networking and recruitment. The CINEMA module provides a dedicated system for talent registration with detailed fields, public accessibility, and specialized features for film industry professionals.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### Application Framework
- **Backend**: Flask 3.0.0 with Python 3.11, utilizing Blueprints for modularity.

### Database Architecture
- **ORM**: SQLAlchemy with Flask-SQLAlchemy, supporting SQLite (development) and PostgreSQL (production).
- **Data Models**: User, Talent, UserTalent, Country, City, AppSettings, and CinemaTalent, with sensitive data encrypted using Fernet.
- **Security**: Passwords hashed with Werkzeug. AppSettings stores configurations securely.
- **Recent Schema Updates (v2.16.0)**: Added website, imdb_url_encrypted, and threads_encrypted fields to User and CinemaTalent models for enhanced profile information.

### Unique Identification System
- **Code Format**: PPVVVNNNNG (Country, City, 4 digits, Gender).
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
- **Registration Form**: Public form (`/cinema/register`) organized into 9 color-coded sections for identity & contact, origins, residence, languages, physical characteristics, talent types (13 options with multi-select), talents (categorized), social networks (encrypted including Telegram), and photos/productions.
- **Profile View**: Public profile page (`/cinema/profile/{code}`) mirrors the registration form structure with 9 sections, displaying age (not birth date), encrypted document number, separated contact block, and correctly mapped data (ethnicities in Origins, talent types vs. competences separated).
- **Features**: Country dropdowns with emoji flags, dynamic city loading, multi-select fields for ethnicities, languages, and talents. All physical characteristic dropdowns (eyes, hair color/type, skin tone, build) are populated from constants.
- **TMDb Integration**: Optional server-side API proxy for movie/TV show search in production history, with real-time search and poster display.
- **Data Model**: `CinemaTalent` model includes personal info with encrypted ID document number, origins vs. residence, physical characteristics, JSON arrays for languages/talent_types/other_talents, encrypted contact/social media (including Telegram), website field (non-encrypted), photo storage, and previous productions as JSON.
- **Valid Data Values**: Ethnicities from predefined list (Africaine, Arabe, Berbère, Caucasienne/Blanche, etc.), Talent types from CINEMA_TALENT_TYPES constant (Acteur/Actrice Principal(e), Acteur/Actrice Secondaire, Figurant(e), Silhouette, Doublure, Doublure Lumière, Cascadeur/Cascadeuse, Mannequin, Voix Off, Figurant Spécialisé, Choriste, Danseur/Danseuse de fond, Autre).

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