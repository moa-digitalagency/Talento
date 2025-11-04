# taalentio.com - Platform for Talent Centralization

## Overview
taalentio.com is a professional web application designed to centralize and showcase talent profiles across Africa, with a specialized CINEMA module for the film industry. The platform enables individuals to create comprehensive profiles with unique identifiers and QR codes, offers advanced administrative tools, and integrates AI-powered CV analysis. It aims to be a robust, scalable solution for enhancing professional networking and recruitment, particularly within the African film sector.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### Application Framework
The backend is built with Flask 3.0.0 (Python 3.11), using Blueprints for modular organization. The frontend uses Jinja2 for templating and Tailwind CSS (CDN) for styling, providing a modern and professional UI/UX. The application is organized into modular Blueprints: `main`, `auth`, `profile`, `admin`, `api`, `cinema`, `presence`, and `api_v1`.

### Database Architecture
SQLAlchemy with Flask-SQLAlchemy serves as the ORM, supporting PostgreSQL (production) and SQLite (development). Data models include User, Talent, UserTalent, Country, City, AppSettings, CinemaTalent, Production, Project, ProjectTalent, NameTracking, and NameTrackingMatch. Sensitive data is encrypted, and passwords are hashed. The system ensures essential data (countries, cities, talents) is loaded and verified at startup.

**Talent Categorization System:**
- Talents are categorized using a `tag` field: 'general' (across 14 service categories) or 'cinema' (across 7 skill categories).
- General talents appear in main listings; cinema talents are exclusive to the CINEMA module.
- Automatic filtering prevents mixing of talent types.

### Authentication & Authorization
Flask-Login manages authentication, supporting dual login via email or unique code. Access control is role-based, with Admin, Recruiter, Presence, and User roles, each having specific permissions.

### File Management
The platform handles uploads of photos, CVs, and SEO images, organizing them into specific directories. QR codes are dynamically generated. Image cropping with Cropper.js enforces a 1:1 aspect ratio for profile photos, and a lightbox functionality is implemented for viewing images.

### AI Integration
Multi-provider AI support (OpenRouter, Bytez, Perplexity, OpenAI, Google Gemini) is integrated for talent matching, CV analysis, and job description analysis. AI-powered search is available for general and cinema-specific talents, with customizable model selection per provider.

### Data Export & Backup
Talent data can be exported in Excel, CSV, and PDF formats. A comprehensive system for full application backup and restoration is included. PDF footers are customizable via admin settings.

### Email System
SendGrid API is used for transactional emails, including application confirmations, login credentials, and automated weekly admin recaps managed by APScheduler.

### Admin Settings & Configuration
Admin features include activity and security logging, centralized API key management, custom HTML head code injection, comprehensive SEO settings, backup/restore capabilities, and cache management. An API status dashboard provides real-time configuration status for all integrated services.

### CINEMA Module Specifics
This module features a multi-section public registration form, public profile display, and CRUD operations for Productions and Projects, including talent assignment and badge generation.

### Multi-Currency Support
The platform supports 60+ currencies mapped to their respective countries. Currency display is dynamic, updating based on the selected residence country in registration forms.

### Location Data Management
The platform manages two sets of location data for each user: City of Origin and Residence City. User listings in admin dashboards prioritize the residence city for recruitment relevance, and search/filter operations use the residence city. A "Ville non listée" option is available for all countries in city selection dropdowns.

## Recent Changes

### [04/11/2025] Navigation Menu and Admin Settings Enhancements
- **Navigation buttons redesign**: Renamed and restyled registration buttons for better clarity
  - "S'inscrire" → "Inscription Talent" (blue outline style)
  - "Inscription Talent" → "Inscription Cinema" (red outline style)
  - Both buttons now use consistent outline styling with brand-specific colors
- **Admin API status dashboard**: Added comprehensive API status overview section in `/admin/settings/api-keys`
  - Displays all 7 configured services: SendGrid, OpenRouter, Bytez, Perplexity, OpenAI, Gemini, OMDB
  - Real-time configuration indicators (green dot = configured, red dot = not configured)
  - Improved at-a-glance service health monitoring

### [04/11/2025] Bytez API Integration Fix (CRITICAL)
- **Root cause**: Bytez API uses a different request format than OpenAI-compatible providers
- **Corrected request format**: Changed from `{"messages": [...]}` to `{"text": "...", "stream": false, "params": {...}}`
- **Parameter updates**: Uses `max_new_tokens` instead of `max_length` in params object
- **Endpoint correction**: Uses `/models/v2/{provider}/{model}` directly (model path includes provider, e.g., "Qwen/Qwen2.5-72B-Instruct")
- **System message handling**: System messages are prepended to user prompt as plain text
- **Enhanced logging**: Added detailed request/response logging for debugging
- **Documentation reference**: https://docs.bytez.com/model-api/docs/welcome
- **Resolves**: "Cannot read properties of undefined (reading 'name')" error

## External Dependencies

### Core Services
- **Database**: PostgreSQL, SQLite.
- **AI Service**: OpenRouter API, Bytez API, Perplexity AI, OpenAI, Google Gemini.
- **Email Service**: SendGrid API.
- **Movie Database**: OMDB API.

### Python Libraries
- **Web Framework & ORM**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail, Flask-Migrate, Flask-WTF.
- **Security**: `cryptography`, `bcrypt`.
- **File Processing**: Pillow, PyPDF2, `python-docx`.
- **Data Export**: `pandas`, `openpyxl`, ReportLab.
- **Scheduling**: APScheduler.
- **Utilities**: `qrcode`, `requests`, `email-validator`, `python-dotenv`, `phonenumbers`, `psutil`.