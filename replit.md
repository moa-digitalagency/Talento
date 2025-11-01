# taalentio.com - Platform for Talent Centralization

## Overview
taalentio.com is a professional web application designed to centralize and showcase talent profiles across Africa. Its primary purpose is talent management and discovery, with a specialized CINEMA module for the film industry. The platform enables individuals to create comprehensive profiles with unique identifiers and QR codes, offers advanced administrative tools, and integrates AI-powered CV analysis. It aims to be a robust, scalable solution for enhancing professional networking and recruitment, particularly within the African film sector.

## User Preferences
Preferred communication style: Simple, everyday language.

## Recent Changes

### November 1, 2025 - Activity Logging, Legal Pages & Email Improvements
- **Legal Mentions Enhancement**: Enhanced legal mentions system with 12 comprehensive fields organized in 4 grouped blocks (Informations sur l'entreprise, Coordonnées, Direction, Hébergement). Added new fields: company_phone, company_email, company_website, hosting_address. Redesigned `/legal/mentions` page with modern grouped dashed-border blocks for better organization and readability.
- **Activity Logs Display Enhancement**: Enhanced activity logs view to show both page name AND page path for consultation actions (view). Page name appears in bold with the path displayed below in smaller text for better visibility and tracking.
- **Activity Logs Enhancement**: Implemented comprehensive page name mapping system (PAGE_NAMES_MAP) in `app/utils/activity_logger.py` to display human-readable page names (e.g., "Paramètres - Administration") instead of raw URLs in activity logs.
- **Action Type Icons**: Enhanced action types with visual icons and labels in the admin activity logs dropdown:
  - 👁️ Consultation (view)
  - ➕ Création (create)
  - ✏️ Modification (update)
  - 🗑️ Suppression (delete)
  - 🔐 Connexion (login)
  - 🚪 Déconnexion (logout)
  - ⚠️ Erreur (error)
  - 🧭 Navigation (navigation - new)
- **Email CC Logic**: Improved email service to prevent duplicate admin CC when admin is already the primary recipient. Now handles all SendGrid recipient formats (string, list, dict) with defensive type checking and case-insensitive comparison.
- **Legal Pages Fix**: Corrected url_for blueprint references in `/legal/mentions` template (legal.privacy, legal.cookies) to prevent 500 errors when legal pages are enabled.
- **Error Logging**: Enhanced error logging with complete JSON format including stack traces.

### October 31, 2025
- **Weekly Admin Recap**: Automated weekly email system that sends a summary every Sunday at 12:59 PM to the admin with new registrations from the past week, separated into regular talents and cinema talents. Includes registration count, names, locations, unique codes, and direct profile view buttons.
- **Scheduler**: APScheduler integrated for automated task scheduling (`app/scheduler.py`).
- **Per-Provider Model Selection**: Added model selection dropdowns in admin settings for all AI providers (Perplexity, OpenAI, Gemini) to complement the existing OpenRouter model selection.
- **Name Tracking System**: Created database models (`NameTracking`, `NameTrackingMatch`) to enable administrators to monitor specific names during registration and receive notifications when tracked individuals register.

## System Architecture

### Application Framework
The backend is built with Flask 3.0.0 (Python 3.11), using Blueprints for modular organization.

### Database Architecture
- **ORM**: SQLAlchemy with Flask-SQLAlchemy, supporting PostgreSQL (production) and SQLite (development).
- **Data Models**: Includes User, Talent, UserTalent, Country, City, AppSettings, CinemaTalent, Production, Project, ProjectTalent, NameTracking, and NameTrackingMatch. Sensitive data is encrypted using Fernet, and passwords are hashed with Werkzeug.
- **Unique Identification**: Distinct codes for main talent profiles (PPGNNNNVVV), CINEMA profiles (PPVVVNNNNNG), and project codes (CCIIISSSNNN).
- **Automatic Data Verification**: Ensures essential data (countries, cities, talents) is loaded and verified at startup, automatically reloading if thresholds are not met.
- **Data Sources**: Utilizes `WORLD_COUNTRIES`, `WORLD_CITIES`, `TALENT_CATEGORIES`, and `NATIONALITIES_WITH_FLAGS`.
- **Name Tracking**: NameTracking and NameTrackingMatch models enable monitoring of specific names during registration.

### Authentication & Authorization
- **Authentication**: Flask-Login, supporting dual login via email or unique code.
- **Access Control**: Role-based system with Admin, Recruteur (Recruiter), Presence, and User roles, each with specific permissions.

### File Management
Supports uploads of photos, CVs, and SEO images. Files are organized into specific directories (`photos/`, `cvs/`, `qrcodes/`, `seo/`) with secure handling, including extension validation and unique filenames. QR codes are generated dynamically for multi-environment compatibility.

### AI Integration
Features multi-provider AI support (OpenRouter, Perplexity, OpenAI, Google Gemini) for talent matching, CV analysis, and job description analysis. Includes AI-powered search for both general talents and cinema-specific characteristics. Each provider now supports customizable model selection through admin settings, with sensible defaults configured per provider.

### Data Export & Backup
Provides talent data export in Excel, CSV, and PDF formats. Includes a comprehensive system for full application backup and restoration.

### Email System
Utilizes SendGrid API for transactional emails, including application confirmations, login credentials, and automated weekly admin recaps. APScheduler manages scheduled email tasks.

### Frontend Architecture
Employs Jinja2 for templating and Tailwind CSS (CDN) for styling. The UI/UX is designed for a modern, professional aesthetic with multi-step forms, role-based dynamic navigation, and consistent branding.

### Routing Structure
Organized into modular Blueprints: `main`, `auth`, `profile`, `admin`, `api`, `cinema`, `presence`, and `api_v1`.

### Admin Settings & Configuration
Includes activity and security logging, centralized API key management, custom HTML head code injection, comprehensive SEO settings with secure image upload, and fully functional backup/restore capabilities. Cache management is also implemented.

### Contract Management
Planned features for general contracts (`/contrats`) and dedicated cinema contracts (`/cinema/contrats`).

### Attendance Management (Présence)
Allows users with `admin` or `presence` roles to manage attendance via QR code scanning or manual entry, with project-based tracking, history, and Excel export.

### REST API v1
Offers a session-based API (`/api/v1`) with endpoints for authentication, user management, talents, location data, CINEMA specific data, and data exports.

### CINEMA Module Specifics
- **Public Registration**: A multi-section public registration form (`/cinema/register`).
- **Public Profile**: Public profile display (`/cinema/profile/{code}`).
- **Management Systems**: CRUD for `Productions` and `Projects`, including talent assignment and badge generation.
- **UI Features**: Dynamic dropdowns, multi-select fields, and country dropdowns with emoji flags.

## External Dependencies

### Core Services
- **Database**: PostgreSQL (production), SQLite (development).
- **AI Service**: OpenRouter API, Perplexity AI, OpenAI, Google Gemini.
- **Email Service**: SendGrid API.
- **Movie Database**: OMDB API (for CINEMA module).

### Python Libraries
- **Web Framework & ORM**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail, Flask-Migrate, Flask-WTF.
- **Database**: `psycopg2-binary`.
- **Security**: `cryptography` (Fernet), `bcrypt`.
- **File Processing**: Pillow, PyPDF2, `python-docx`.
- **Data Export**: `pandas`, `openpyxl`, ReportLab.
- **Email**: `sendgrid`.
- **Scheduling**: APScheduler (for automated tasks).
- **Utilities**: `qrcode`, `requests`, `email-validator`, `python-dotenv`, `phonenumbers`, `psutil`.