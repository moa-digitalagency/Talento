# Talento - Platform for Talent Centralization

## Overview
Talento is a professional web application designed to centralize and showcase talent profiles across Africa. It enables individuals to create comprehensive profiles with unique identifiers and QR codes. The platform features advanced administrative tools, AI-powered CV analysis, and multiple data export formats. Talento aims to be a robust, scalable solution for talent management and discovery, enhancing professional networking and recruitment across the continent. A key module, CINEMA, provides a dedicated system for talent registration with detailed fields and public accessibility.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### Application Framework
- **Backend**: Flask 3.0.0 with Python 3.11, utilizing Blueprints for modularity.

### Database Architecture
- **ORM**: SQLAlchemy with Flask-SQLAlchemy 3.1.1, supporting SQLite (development) and PostgreSQL (production).
- **Data Models**: User, Talent, UserTalent, Country, City, AppSettings, and CinemaTalent.
- **Security**: Sensitive data (e.g., ID numbers, phone, social media links) is encrypted using Fernet; passwords are hashed with Werkzeug. AppSettings stores configurations like API keys securely in the database.

### Unique Identification System
- **Code Format**: PPVVVNNNNG (Country, City, 4 digits, Gender).
- **QR Codes**: Automatically generated and linked to profile URLs.

### Authentication & Authorization
- **User Authentication**: Flask-Login, supporting dual login (email OR unique code).
- **Access Control**: Role-based (admin vs. regular users). Admins manage all users; candidates manage their own profiles.
- **Password Management**: Randomly generated passwords for new users, sent via email.

### File Management
- **Uploads**: Supports photos (PNG, JPG, JPEG up to 5MB) and CVs (PDF, DOC, DOCX up to 10MB).
- **Storage**: Files are organized into `photos/`, `cvs/`, `qrcodes/` with UUID-based filenames.

### AI Integration
- **CV Analysis**: OpenRouter AI integration automatically analyzes uploaded CVs, extracting skills, generating summaries, and assigning a profile score (0-100). This analysis is displayed on the user's profile.

### Data Export & Backup
- **Export Formats**: Supports Excel (XLSX), CSV, and PDF for talent data and lists.
- **Backup & Restore**: A comprehensive system allows for full application backup into encrypted ZIP archives and restoration, including transactional safety and secure handling of sensitive data (decryption on export, re-encryption on import).

### Email System
- **Service**: SendGrid API for transactional emails, with configurable API keys and sender email stored in the database.
- **Automated Emails**: Includes application confirmation and login credentials for new candidates.

### Frontend Architecture
- **Template Engine**: Jinja2.
- **CSS Framework**: Tailwind CSS (CDN) for responsive, utility-first design.
- **UI/UX Decisions**:
    - Modern, professional aesthetic with solid colors and dotted borders.
    - Multi-step registration forms with visual progress.
    - Unified, role-adapted dashboards displaying talent category statistics.
    - Enhanced individual profile pages with secure display of initials, integrated QR codes, and visual badges.
    - Streamlined navigation with search/filter functionalities.
    - Consistent use of French labels for availability and other options.
    - Public CINEMA talent registration form mirrors the main registration design.

### Routing Structure
- **Blueprints**: Organized into `main`, `auth`, `profile`, `admin`, `api`, and `cinema` for modularity.

### Constants & Configuration
- **Centralized Constants**: `app/constants.py` defines standardized availability and talent categories.

### Migration & Database Initialization
- **Strategy**: Custom scripts for table creation, column addition, and data seeding (countries, cities, talents) with idempotent operations.

## External Dependencies

### Core Services
- **Database**: PostgreSQL (production), SQLite (development).
- **AI Service**: OpenRouter API.
- **Email Service**: SendGrid API.

### Python Libraries
- **Web Framework**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail, Flask-Migrate, Flask-WTF.
- **Database**: `psycopg2-binary`, SQLAlchemy.
- **Security**: `cryptography`, `bcrypt`, Flask-WTF.
- **File Processing**: Pillow, PyPDF2, `python-docx`.
- **Data Export**: `pandas`, `openpyxl`, ReportLab.
- **Email**: `sendgrid`.
- **Utilities**: `qrcode`, `requests`, `email-validator`, `python-dotenv`.

### Configuration Requirements
- **Environment Variables**: `SECRET_KEY`, `DATABASE_URL`, `ENCRYPTION_KEY` are required. `SENDGRID_API_KEY`, `OPENROUTER_API_KEY`, `SENDGRID_FROM_EMAIL`, `REPLIT_DEV_DOMAIN` are optional (API keys and sender email can be managed via admin settings).

### Static Assets
- **CSS**: Tailwind CSS (CDN), custom corporate theme.
- **Uploads Directory**: Local storage for user-generated content.