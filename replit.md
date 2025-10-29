# taalentio.com - Platform for Talent Centralization

## Overview
taalentio.com is a professional web application designed to centralize and showcase talent profiles across Africa, with a strong focus on the film industry through its CINEMA module. It enables individuals to create comprehensive profiles with unique identifiers and QR codes. The platform features advanced administrative tools, AI-powered CV analysis, and multiple data export formats. taalentio.com aims to be a robust, scalable solution for talent management and discovery, enhancing professional networking and recruitment. The CINEMA module provides a dedicated system for talent registration with detailed fields, public accessibility, and specialized features for film industry professionals.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### Application Framework
- **Backend**: Flask 3.0.0 with Python 3.11, utilizing Blueprints for modularity.

### Database Architecture
- **ORM**: SQLAlchemy with Flask-SQLAlchemy, supporting SQLite (development) and PostgreSQL (production).
- **Data Models**: User, Talent, UserTalent, Country, City, AppSettings, CinemaTalent, Production, Project, and ProjectTalent. Sensitive data is encrypted using Fernet. Passwords hashed with Werkzeug. City model includes country_id foreign key for proper country-city relationships.
- **Unique Identification System**: Distinct codes for main talent profiles (PPGNNNNVVV) and CINEMA profiles (PPVVVNNNNNG), plus project codes (CCIIISSSNNN). Codes are sequential and country-specific.
- **Automatic Data Verification & Loading**: Critical system that verifies and auto-loads essential data at every startup via `ensure_essential_data()` in `app/__init__.py`. Checks minimum thresholds (100+ countries, 1000+ cities with country_id, 50+ talents). If data is missing or incomplete, automatically calls `migrations_init.py` to reload. Displays detailed logs at startup. Anti-recursion protection with SKIP_AUTO_MIGRATION env variable. Guarantees dropdown lists (countries, cities, nationalities, talents) are always available at deployment and after restart.
- **World Data Sources**: WORLD_COUNTRIES (194 countries) and WORLD_CITIES (1,710 cities from 142 countries) from app/data/. TALENT_CATEGORIES and NATIONALITIES_WITH_FLAGS from app/constants.py. Performance index on cities.country_id for fast lookups.
- **Data Cleanup Script**: `clean_all_data.py` safely removes all user-generated data while preserving admin accounts and reference data. Demo data creation disabled by default.

### Authentication & Authorization
- **User Authentication**: Flask-Login, supporting dual login (email OR unique code).
- **Access Control**: Role-based (admin, presence, regular users).

### File Management
- **Uploads**: Photos (PNG, JPG, JPEG up to 5MB) and CVs (PDF, DOC, DOCX up to 10MB).
- **Storage**: Files organized into `photos/`, `cvs/`, `qrcodes/` with UUID-based filenames.
- **QR Code Generation**: Portable system using `Config.get_base_url()` for multi-environment compatibility (Replit, VPS, local).

### AI Integration
- **CV Analysis**: OpenRouter AI integration analyzes CVs for skills, summaries, and profile scores.

### Data Export & Backup
- **Export Formats**: Excel (XLSX), CSV, and PDF for talent data.
- **Backup & Restore**: Comprehensive system for full application backup and restoration.

### Email System
- **Service**: SendGrid API for transactional emails.
- **Automated Emails**: Includes application confirmation and login credentials for new candidates, incorporating the taalentio.com logo.

### Frontend Architecture
- **Template Engine**: Jinja2.
- **CSS Framework**: Tailwind CSS (CDN).
- **UI/UX Decisions**: Modern, professional aesthetic with solid colors, multi-step registration forms, role-based dynamic navigation menus, enhanced profile pages with action buttons, secure display of initials and QR codes, and consistent use of French labels. Logo systematically added to emails and PDFs. Nationality field in registration forms is a dropdown with emoji flags.

### Routing Structure
- **Blueprints**: Organized into `main`, `auth`, `profile`, `admin`, `api`, `cinema`, `presence`, and `api_v1` for modularity.

### Admin Settings & Configuration
- **Activity Logs**: Real-time tracking of user actions.
- **API Keys Management**: Centralized management for external service API keys (SendGrid, OpenRouter, OMDB) with masked display.
- **System Settings**: Custom HTML head code injection for analytics, SEO, or custom CSS/JS.

### Contract Management
- **Main Contracts Page**: `/contrats` - Planned features include creation, electronic signature, tracking, notifications, archiving, and PDF export.
- **Cinema Contracts Page**: `/cinema/contrats` - Dedicated contract management for cinema talents with tailored features.

### Attendance Management (Présence)
- **Access Control**: Accessible by users with `admin` or `presence` roles.
- **Core Features**: QR code scanning or manual entry for check-in/check-out, automatic arrival/departure detection, bulk actions, project-based tracking, attendance history with duration calculations.
- **Data Export**: Excel export of attendance records.
- **Database Model**: New `Attendance` model.

### REST API v1
- **Base URL**: `/api/v1`.
- **Authentication**: Session-based (cookies), CSRF protection exempt.
- **Documentation**: Available in `api_docs/`.
- **Key Endpoints**: Authentication, User management, Talents & Location data, CINEMA specific data and statistics, and Data Exports.

### CINEMA Module Specifics
- **Registration Form**: Public form (`/cinema/register`) with 9 color-coded sections for comprehensive talent data capture.
- **Profile View**: Public profile page (`/cinema/profile/{code}`) mirroring registration.
- **Talents Management**: List page with advanced search filters.
- **Productions Management**: Complete CRUD system for cinematographic production companies.
- **Projects Management**: System for managing ongoing production projects, including talent assignment, unique project codes, and badge generation.
- **Features**: Country dropdowns with emoji flags, dynamic city loading, multi-select fields, constant-populated dropdowns.

## External Dependencies

### Core Services
- **Database**: PostgreSQL (production), SQLite (development).
- **AI Service**: OpenRouter API.
- **Email Service**: SendGrid API.
- **Movie Database**: OMDB API (for CINEMA module).

### Python Libraries
- **Web Framework & ORM**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail, Flask-Migrate, Flask-WTF.
- **Database**: `psycopg2-binary`.
- **Security**: `cryptography` (for Fernet encryption), `bcrypt` (for password hashing).
- **File Processing**: Pillow, PyPDF2, `python-docx`.
- **Data Export**: `pandas`, `openpyxl`, ReportLab.
- **Email**: `sendgrid`.
- **Utilities**: `qrcode`, `requests`, `email-validator`, `python-dotenv`, `phonenumbers`.