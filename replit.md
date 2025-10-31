# taalentio.com - Platform for Talent Centralization

## Overview
taalentio.com is a professional web application designed to centralize and showcase talent profiles across Africa. Its primary purpose is talent management and discovery, with a specialized CINEMA module for the film industry. The platform enables individuals to create comprehensive profiles with unique identifiers and QR codes, offers advanced administrative tools, and integrates AI-powered CV analysis. It aims to be a robust, scalable solution for enhancing professional networking and recruitment, particularly within the African film sector.

## User Preferences
Preferred communication style: Simple, everyday language.

## Recent Changes (October 31, 2025)

### Automated Email Recaps
- **Weekly Admin Recap**: Automated weekly email system that sends a summary every Sunday at 12:59 PM to the admin with new registrations from the past week, separated into regular talents and cinema talents. Includes registration count, names, locations, unique codes, and direct profile view buttons.
- **Scheduler**: APScheduler integrated for automated task scheduling (`app/scheduler.py`).

### Enhanced AI Configuration
- **Per-Provider Model Selection**: Added model selection dropdowns in admin settings for all AI providers (Perplexity, OpenAI, Gemini) to complement the existing OpenRouter model selection. Administrators can now choose specific models for each provider:
  - **Perplexity**: llama-3.1-sonar-small/large/huge-128k-online
  - **OpenAI**: gpt-4o-mini, gpt-4o, gpt-4-turbo, gpt-3.5-turbo
  - **Gemini**: gemini-2.0-flash-exp, gemini-1.5-flash, gemini-1.5-pro
- **Dynamic Configuration**: AIProviderService now reads model selections from AppSettings, allowing runtime configuration changes without code modifications.

### Name Tracking System
- **NameTracking Model**: Created database models (`NameTracking`, `NameTrackingMatch`) to enable administrators to monitor specific names during registration and receive notifications when tracked individuals register.
- **Infrastructure Ready**: Models are in place and ready for implementation of admin UI and notification system.

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