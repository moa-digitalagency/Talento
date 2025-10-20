# Talento - Platform for Talent Centralization

## Overview

Talento is a professional web application designed to centralize and showcase talent profiles across Africa. The platform enables individuals to create comprehensive professional profiles with unique identifiers, QR codes, and multi-talent capabilities. It features advanced administrative tools for managing users, AI-powered CV analysis, and multiple data export formats (Excel, PDF, CSV). The project aims to provide a robust, scalable solution for talent management and discovery, enhancing professional networking and recruitment across the continent.

## Recent Changes (October 20, 2025)

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
- **Data Models**: User, Talent, UserTalent, Country, and City entities.
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

### Email System
- **Email Service**: Integrated SendGrid API for professional email delivery. Two automated emails sent during registration: application confirmation (with profile URL and optional PDF) and login credentials (unique code + password). HTML templates with responsive design and professional styling.

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
- **Web Framework**: Flask ecosystem (Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail, Flask-Migrate).
- **Database**: `psycopg2-binary`, SQLAlchemy.
- **Security**: `cryptography`, `bcrypt`.
- **File Processing**: Pillow, PyPDF2, `python-docx`.
- **Data Export**: `pandas`, `openpyxl`, ReportLab.
- **Email**: `sendgrid` for transactional email delivery.
- **Utilities**: `qrcode`, `requests`, `email-validator`, `python-dotenv`.

### Configuration Requirements
- **Required Environment Variables**: `SECRET_KEY`, `DATABASE_URL`, `ENCRYPTION_KEY`, `SENDGRID_API_KEY`, `OPENROUTER_API_KEY`.
- **Optional Environment Variables**: `SENDGRID_FROM_EMAIL` (default: noreply@talento.com), `REPLIT_DEV_DOMAIN` (auto-detected in Replit environment).

### Static Assets
- **Tailwind CSS**: CDN-delivered.
- **Custom CSS**: For corporate theme overrides.
- **Uploads Directory**: Local storage for user-generated content.