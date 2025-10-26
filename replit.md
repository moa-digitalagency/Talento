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
- **Data Models**: User, Talent, UserTalent, Country, City, AppSettings, CinemaTalent, Production, Project, and ProjectTalent. Sensitive data is encrypted using Fernet. Passwords hashed with Werkzeug.
- **Unique Identification System**:
    - **Main Code**: PPGNNNNVVV (Country, Gender, 4 sequential digits per country, City) - 10 characters.
    - **CINEMA Code**: PPVVVNNNNNG (Country, City, 4 sequential digits per country, Gender) - 11 characters.
    - **Project Code**: CCIIISSSNNN (Country, Production Initials, Project ID, Talent Number) - 10+ characters, no dashes.
    - Both main and CINEMA codes use sequential numbering incremented per country.
    - Codes are distinguished by component order.
- **Automatic Data Seeding**: System creates demo users, CINEMA talents, productions, and an admin account (admin@talento.com / MAN0001RAB / @4dm1n) if not present.

### Authentication & Authorization
- **User Authentication**: Flask-Login, supporting dual login (email OR unique code).
- **Access Control**: Role-based (admin vs. regular users).

### File Management
- **Uploads**: Photos (PNG, JPG, JPEG up to 5MB) and CVs (PDF, DOC, DOCX up to 10MB).
- **Storage**: Files organized into `photos/`, `cvs/`, `qrcodes/` with UUID-based filenames.

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
- **UI/UX Decisions**: Modern, professional aesthetic with solid colors, multi-step registration forms, role-adapted dashboards, enhanced individual profile pages with secure display of initials and QR codes, streamlined navigation, and consistent use of French labels.

### Routing Structure
- **Blueprints**: Organized into `main`, `auth`, `profile`, `admin`, `api`, `cinema`, and `api_v1` for modularity.

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
- **Movie Database**: TMDb API (optional, for CINEMA module).

### Python Libraries
- **Web Framework & ORM**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail, Flask-Migrate, Flask-WTF.
- **Database**: `psycopg2-binary`.
- **Security**: `cryptography` (for Fernet encryption), `bcrypt` (for password hashing).
- **File Processing**: Pillow, PyPDF2, `python-docx`.
- **Data Export**: `pandas`, `openpyxl`, ReportLab.
- **Email**: `sendgrid`.
- **Utilities**: `qrcode`, `requests`, `email-validator`, `python-dotenv`, `phonenumbers`.