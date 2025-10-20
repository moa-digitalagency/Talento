# Talento - Platform for Talent Centralization

## Overview

Talento is a professional web application designed to centralize and showcase talent profiles across Africa. The platform enables individuals to create comprehensive professional profiles with unique identifiers, QR codes, and multi-talent capabilities. It features advanced administrative tools for managing users, AI-powered CV analysis, and multiple data export formats (Excel, PDF, CSV). The project aims to provide a robust, scalable solution for talent management and discovery, enhancing professional networking and recruitment across the continent.

## Recent Changes (October 20, 2025)

- **CINEMA Module - Public Registration (v2.21.0)**: Made CINEMA talent registration publicly accessible. Changes include: (1) Removed `@login_required` decorator from `/cinema/register` route for public access, (2) Added "CINEMA 🎬" button in public navigation menu (desktop and mobile) accessible to non-logged users, (3) Modified `base_cinema.html` to conditionally display sidebar only for authenticated users while public users see full-width registration form, (4) Changed submit button from gradient style to corporate `btn-primary` style matching main registration form. Registration form now follows exact same design patterns as `/auth/register` with section-colored boxes, dotted borders, and no gradients anywhere.
- **CINEMA Module (v2.20.0)**: Complete CINEMA universe with full talent registration system. Enhanced features include: (1) Dedicated database model `CinemaTalent` with encrypted sensitive data (ID document number, phone, WhatsApp, social media), (2) Multi-step registration form with 7 sections (Identity, ID Document, Location, Languages & Experience, Physical Characteristics, Photos & Contact, Social Media & Productions) following the same design patterns as main registration, (3) Sidebar navigation with 5 sections: Dashboard, Talents, Productions, Projects, and Technical Team, (4) Full CRUD routes for talent management with `/cinema/register` endpoint, (5) Talent listing page with search filters and table view, (6) File upload support for profile photos, ID photos, and photo galleries stored in `cinema_photos` directory, (7) Data isolation - all CINEMA data is stored separately from main Talento database in `cinema_talents` table. The module is fully functional and ready for talent registration with all fields from the requirements (full name, document type, ethnicity, nationality, languages, physical characteristics, previous productions, etc.).
- **Complete Backup & Restore System (v2.18.0)**: Implemented comprehensive backup/restore functionality for full application migration. Admin settings page now includes: (1) "Créer une sauvegarde complète" button that generates a ZIP archive containing all user profiles with **decrypted sensitive data** (phone, address, passport, residence card, social media), uploaded files (photos, CVs, QR codes), database content, and configuration; (2) "Restauration complète" form with file upload that restores all data and automatically **re-encrypts sensitive fields** during import. Security enhancements include: Zip Slip protection with path validation before extraction, transactional restore with automatic rollback on errors, primary key sequence reset for PostgreSQL/SQLite compatibility, robust ISO datetime parsing with error handling, cleanup of temporary files using `after_this_request`, and CSRF protection via Flask-WTF. System warns users about destructive nature of restore operations with confirmation dialogs.
- **Bulk User Management & Enhanced Admin Controls (v2.17.0)**: Added comprehensive bulk deletion features for admin efficiency. Dashboard (`index.html`) and Talents listing (`talents.html`) now include: (1) individual "Supprimer" buttons in the Actions column for quick single-user deletion with confirmation, (2) checkboxes on each user row enabling multi-select, (3) "Supprimer sélectionnés" button for batch deletion with double confirmation and counter display. All deletion routes include secure redirect validation using `is_safe_url()` function to prevent open redirect vulnerabilities while maintaining navigation flow (admins return to their originating page after deletion). Enhanced Settings page with new "Backup & Restore" section providing clear access to data export tools (Excel, CSV, PDF) and honest messaging about future import functionality. Database section styling fixed with proper dotted borders for visual consistency.
- **Database-Driven Settings (v2.16.0)**: Complete redesign of settings management. API keys (SendGrid, OpenRouter) and configuration are now stored in the database (`app_settings` table) instead of environment variables. Admin settings page includes: (1) API key input fields with secure masking, (2) configurable sender email (default: noreply@myoneart.com), (3) live email testing functionality, and (4) integrated admin user creation. The system reads from database with automatic fallback to environment variables for backward compatibility.
- **Admin Settings Page (v2.15.0)**: New `/admin/settings` page for administrators with API key status monitoring (SendGrid, OpenRouter), admin user management (promote/demote users), and system configuration overview.
- **Enhanced CV Analysis Display (v2.15.0)**: Profile view now intelligently displays three states: (1) "Aucun CV disponible" with upload button when no CV exists, (2) "CV en cours de traitement" when CV uploaded but not analyzed, (3) Full analysis with score when available.
- **Navigation Menu Update (v2.15.0)**: Added "Paramètres" (Settings) link in navigation menu for admin users (desktop and mobile), providing quick access to system configuration.
- **Admin Management Features (v2.15.0)**: Admins can now promote regular users to admin status and demote other admins (with safeguards: cannot self-demote, cannot remove last admin).
- **SendGrid Email Integration (v2.14.0)**: Integrated SendGrid for automated email notifications. New candidates receive two emails: (1) application confirmation with profile link and optional PDF attachment, and (2) login credentials with unique code and randomly generated password.
- **OpenRouter AI Integration (v2.14.0)**: Added intelligent CV analysis using OpenRouter API. System automatically analyzes uploaded CVs, extracts skills, generates professional summaries, and assigns profile scores (0-100).
- **Dual Authentication (v2.14.0)**: Users can now login with either email OR unique code, making access easier for candidates who prefer using their unique identifier.
- **Candidate Self-Service (v2.14.0)**: Candidates can now edit their own profiles, update information, upload new CVs (which triggers automatic re-analysis), and manage their talents.
- **Profile Scoring & Analysis Display (v2.14.0)**: Profile view now shows AI-generated analysis with circular score indicator, detected skills, strengths, recommendations, and experience years.
- **QR Code Fix (v2.13.0)**: Fixed QR code generation to use proper HTTPS URLs that open profile pages in browsers instead of displaying text. QR codes are automatically regenerated on app restart.
- **Navigation Improvements (v2.13.0)**: Fixed back button on profile pages to return to `/talents` list. Added responsive hamburger menu for mobile/tablet navigation while keeping Talento logo always visible.
- **Responsive Design (v2.13.0)**: QR codes are now hidden on mobile and tablet devices (visible only on desktop) to optimize space and improve mobile experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Framework
- **Backend Framework**: Flask 3.0.0 with Python 3.11, leveraging Blueprints for modularity.

### Database Architecture
- **ORM**: SQLAlchemy with Flask-SQLAlchemy 3.1.1, supporting SQLite (development) and PostgreSQL (production).
- **Data Models**: User, Talent, UserTalent, Country, City, and AppSettings entities.
- **Settings Storage**: AppSettings model stores application configuration (API keys, email sender) in encrypted database table with get/set class methods.
- **Security**: Encrypted storage for sensitive data using Fernet, password hashing with Werkzeug.

### Unique Identification System
- **Code Format**: PPVVVNNNNG (Country, City, 4 digits, Gender).
- **QR Code Generation**: Automatic QR code creation linking to profile URLs.
- **Validation**: Regex-based validation and uniqueness checks.

### Authentication & Authorization
- **User Authentication**: Flask-Login for session management with dual login support (email OR unique code), secure password hashing.
- **Access Control**: Role-based (admin vs. regular users) with protected routes. Candidates can edit their own profiles; admins can manage all users.
- **Password Management**: Random generation for new users, secure bcrypt hashing, email delivery of credentials via SendGrid.

### File Management
- **Upload Handling**: Supports photos (PNG, JPG, JPEG up to 5MB) and CVs (PDF, DOC, DOCX up to 10MB).
- **Storage**: Secure filename generation with UUIDs, organized into `photos/`, `cvs/`, `qrcodes/`.
- **Document Processing**: PyPDF2 for PDF, python-docx for DOCX, Pillow for image optimization.

### AI Integration
- **CV Analysis Service**: OpenRouter AI integration for intelligent CV analysis. Automatically triggered on CV upload (registration or profile update). Analyzes CV content, extracts skills, calculates profile score (0-100), identifies strengths/weaknesses, and generates recruiter-style recommendations. Results stored in JSON format and displayed in profile view with visual score indicator.

### Data Export System
- **Export Formats**: Excel (XLSX) using openpyxl, CSV using pandas, and PDF using ReportLab.
- **PDF Export**: Supports list views and detailed individual talent sheets with photos and QR codes.
- **Backup & Restore**: Complete application backup/restore system (`BackupService`) that exports all data to encrypted ZIP archives with automatic decryption on export and re-encryption on restore. Includes transactional safety, Zip Slip protection, sequence reset, and CSRF protection.

### Email System
- **Email Service**: Integrated SendGrid API for professional email delivery. Supports configurable API keys and sender email (stored in database). Two automated emails sent during registration: application confirmation (with profile URL and optional PDF) and login credentials (unique code + password). HTML templates with responsive design and professional styling. Admin can test email configuration with send_test_email functionality.
- **Default Sender**: noreply@myoneart.com (configurable via admin settings page).

### Frontend Architecture
- **Template Engine**: Jinja2.
- **CSS Framework**: Tailwind CSS via CDN for a utility-first approach and responsive design.
- **UI/UX Decisions**:
    - Modern, professional design with consistent use of solid colors and dotted borders.
    - Multi-step registration form with visual progress indicators and color-coded sections.
    - Unified dashboard experience adapted for user roles showing talent category statistics.
    - Enhanced individual profile pages with secure initials, integrated QR codes, and visual badges.
    - Streamlined navigation and improved search/filter functionalities with French availability labels.
    - Complete removal of gradients for a cleaner aesthetic.
    - Dashboard displays top talent categories instead of availability statistics.

### Routing Structure
- **Blueprint Organization**: `main`, `auth`, `profile`, `admin`, and `api` for clear separation of concerns.

### Constants & Configuration
- **Centralized Constants**: `app/constants.py` defines standardized availability options and talent categories for consistency across the application.

### Migration & Database Initialization
- **Migration Strategy**: Custom script (`migrations_init.py`) for table creation, column addition, and data seeding (countries, cities, talents) with idempotent operations.
- **Availability Migration**: Script `migrate_availability.py` converts legacy availability values to new French labels. Must be run on deployment to ensure data compatibility.

## External Dependencies

### Core Services
- **Database**: PostgreSQL (production) / SQLite (development).
- **AI Service**: OpenRouter API for intelligent CV analysis and profile scoring (requires `OPENROUTER_API_KEY`).
- **Email Service**: SendGrid API for transactional email delivery (requires `SENDGRID_API_KEY`).

### Python Libraries
- **Web Framework**: Flask ecosystem (Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail, Flask-Migrate, Flask-WTF).
- **Database**: `psycopg2-binary`, SQLAlchemy.
- **Security**: `cryptography`, `bcrypt`, Flask-WTF (CSRF protection).
- **File Processing**: Pillow, PyPDF2, `python-docx`.
- **Data Export**: `pandas`, `openpyxl`, ReportLab.
- **Email**: `sendgrid` for transactional email delivery.
- **Utilities**: `qrcode`, `requests`, `email-validator`, `python-dotenv`.

### Configuration Requirements
- **Required Environment Variables**: `SECRET_KEY`, `DATABASE_URL`, `ENCRYPTION_KEY`.
- **Optional Environment Variables**: `SENDGRID_API_KEY`, `OPENROUTER_API_KEY` (can be configured via admin settings page instead), `SENDGRID_FROM_EMAIL` (default: noreply@myoneart.com), `REPLIT_DEV_DOMAIN` (auto-detected in Replit environment).
- **Database-Stored Settings**: SendGrid API key, OpenRouter API key, and sender email are stored in the database and configurable through the admin interface.

### Static Assets
- **Tailwind CSS**: CDN-delivered.
- **Custom CSS**: For corporate theme overrides.
- **Uploads Directory**: Local storage for user-generated content.