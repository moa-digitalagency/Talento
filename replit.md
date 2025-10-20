# Talento - Platform for Talent Centralization

## Overview

Talento is a professional web application designed to centralize and showcase talent profiles across Africa. The platform enables individuals to create comprehensive professional profiles with unique identifiers, QR codes, and multi-talent capabilities. It features advanced administrative tools for managing users, AI-powered CV analysis, and multiple data export formats (Excel, PDF, CSV). The project aims to provide a robust, scalable solution for talent management and discovery, enhancing professional networking and recruitment across the continent.

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
- **User Authentication**: Flask-Login for session management, email-based login, and password hashing.
- **Access Control**: Role-based (admin vs. regular users) with protected routes.
- **Password Management**: Random generation for new users, secure bcrypt hashing, and email delivery of credentials.

### File Management
- **Upload Handling**: Supports photos (PNG, JPG, JPEG up to 5MB) and CVs (PDF, DOC, DOCX up to 10MB).
- **Storage**: Secure filename generation with UUIDs, organized into `photos/`, `cvs/`, `qrcodes/`.
- **Document Processing**: PyPDF2 for PDF, python-docx for DOCX, Pillow for image optimization.

### AI Integration
- **CV Analysis Service**: Integration with OpenRouter AI API for automated CV analysis, skill extraction, profile scoring (0-100), and personalized recommendations.

### Data Export System
- **Export Formats**: Excel (XLSX) using openpyxl, CSV using pandas, and PDF using ReportLab.
- **PDF Export**: Supports list views and detailed individual talent sheets with photos and QR codes.

### Email System
- **Email Service**: Flask-Mail with SendGrid support for sending confirmation emails and credentials using HTML templates.

### Frontend Architecture
- **Template Engine**: Jinja2.
- **CSS Framework**: Tailwind CSS via CDN for a utility-first approach and responsive design.
- **UI/UX Decisions**:
    - Modern, professional design with consistent use of solid colors and dotted borders.
    - Multi-step registration form with visual progress indicators and color-coded sections.
    - Unified dashboard experience adapted for user roles.
    - Enhanced individual profile pages with secure initials, integrated QR codes, and visual badges.
    - Streamlined navigation and improved search/filter functionalities.
    - Complete removal of gradients for a cleaner aesthetic.

### Routing Structure
- **Blueprint Organization**: `main`, `auth`, `profile`, `admin`, and `api` for clear separation of concerns.

### Migration & Database Initialization
- **Migration Strategy**: Custom script (`migrations_init.py`) for table creation, column addition, and data seeding (countries, cities, talents) with idempotent operations.

## External Dependencies

### Core Services
- **Database**: PostgreSQL (production) / SQLite (development).
- **AI Service**: OpenRouter API for CV analysis (requires `OPENROUTER_API_KEY`).

### Email Delivery
- **SendGrid**: Optional professional email delivery (requires `SENDGRID_API_KEY`).
- **SMTP**: Alternative standard email protocol for secure transmission.

### Python Libraries
- **Web Framework**: Flask ecosystem (Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail, Flask-Migrate).
- **Database**: `psycopg2-binary`, SQLAlchemy.
- **Security**: `cryptography`, `bcrypt`.
- **File Processing**: Pillow, PyPDF2, `python-docx`.
- **Data Export**: `pandas`, `openpyxl`, ReportLab.
- **Utilities**: `qrcode`, `requests`, `email-validator`, `python-dotenv`.

### Configuration Requirements
- **Required Environment Variables**: `SECRET_KEY`, `DATABASE_URL`, `ENCRYPTION_KEY`.
- **Optional Environment Variables**: `OPENROUTER_API_KEY`, `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `SENDGRID_API_KEY`, `REPLIT_DEV_DOMAIN`.

### Static Assets
- **Tailwind CSS**: CDN-delivered.
- **Custom CSS**: For corporate theme overrides.
- **Uploads Directory**: Local storage for user-generated content.