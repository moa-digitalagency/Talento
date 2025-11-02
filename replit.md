# taalentio.com - Platform for Talent Centralization

## Overview
taalentio.com is a professional web application designed to centralize and showcase talent profiles across Africa, with a specialized CINEMA module for the film industry. The platform enables individuals to create comprehensive profiles with unique identifiers and QR codes, offers advanced administrative tools, and integrates AI-powered CV analysis. It aims to be a robust, scalable solution for enhancing professional networking and recruitment, particularly within the African film sector.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### Application Framework
The backend is built with Flask 3.0.0 (Python 3.11), using Blueprints for modular organization. Frontend uses Jinja2 for templating and Tailwind CSS (CDN) for styling, providing a modern and professional UI/UX.

### Database Architecture
SQLAlchemy with Flask-SQLAlchemy serves as the ORM, supporting PostgreSQL (production) and SQLite (development). Data models include User, Talent, UserTalent, Country, City, AppSettings, CinemaTalent, Production, Project, ProjectTalent, NameTracking, and NameTrackingMatch. Sensitive data is encrypted using Fernet, and passwords are hashed with Werkzeug. The system ensures essential data (countries, cities, talents) is loaded and verified at startup.

**Talent Categorization System:**
- Talents are categorized using a `tag` field: 'general' (158 talents) or 'cinema' (57 talents)
- General talents appear in main listings (/, /talents, /admin/users) across 14 service categories
- Cinema talents are exclusive to the CINEMA module (/cinema/talents) organized in 7 skill categories
- Automatic filtering prevents mixing of talent types across different sections
- Cinema categories: Talents artistiques et créatifs, Compétences physiques et sportives, Compétences manuelles et artisanales, Compétences sociales et linguistiques, Compétences techniques diverses, Expériences professionnelles variées valorisantes, Qualités humaines et habitudes de vie

### Authentication & Authorization
Flask-Login manages authentication, supporting dual login via email or unique code. Access control is role-based, with Admin, Recruteur (Recruiter), Presence, and User roles, each having specific permissions.

### File Management
The platform handles uploads of photos, CVs, and SEO images, organizing them into specific directories. QR codes are dynamically generated for multi-environment compatibility.

### AI Integration
Multi-provider AI support (OpenRouter, Bytez, Perplexity, OpenAI, Google Gemini) is integrated for talent matching, CV analysis, and job description analysis. AI-powered search is available for general and cinema-specific talents, with customizable model selection per provider. Bytez provides access to hundreds of open-source and closed-source models through a unified API.

### Data Export & Backup
Talent data can be exported in Excel, CSV, and PDF formats. A comprehensive system for full application backup and restoration is included.

### Email System
SendGrid API is used for transactional emails, including application confirmations, login credentials, and automated weekly admin recaps managed by APScheduler.

### Routing Structure
The application is organized into modular Blueprints: `main`, `auth`, `profile`, `admin`, `api`, `cinema`, `presence`, and `api_v1`.

### Admin Settings & Configuration
Admin features include activity and security logging, centralized API key management, custom HTML head code injection, comprehensive SEO settings, and backup/restore capabilities. Cache management is also implemented.

### CINEMA Module Specifics
This module features a multi-section public registration form, public profile display, and CRUD operations for Productions and Projects, including talent assignment and badge generation.

### Multi-Currency Support
The platform supports 60+ currencies mapped to their respective countries:
- **Currency Mapping**: `app/constants.py` contains `COUNTRY_CURRENCIES` dictionary mapping country codes to currencies
- **Dynamic Currency Display**: Registration forms automatically update currency display based on selected residence country
- **Supported Currencies**: MAD (Morocco), CDF (DRC), EUR (Europe), USD (USA), FCFA (West Africa), and many more
- **Helper Function**: `get_currency_for_country(country_code)` provides easy currency lookup

### Location Data Management
The platform manages two sets of location data for each user:
- **City of Origin** (`city_id`, `country_id`): User's birthplace or origin
- **Residence City** (`residence_city_id`, `residence_country_id`): Current residence location
- **Display Priority**: User listings in admin dashboards display the residence city as it's more relevant for recruitment and availability
- **Filtering**: Search and filter operations use residence_city_id for accurate location-based queries

### Recent Enhancements (November 2025)
- ✅ Implemented talent segregation system (general vs cinema talents)
- ✅ Added dynamic currency display in registration forms based on residence country
- ✅ Synchronized currency mapping between Python backend and JavaScript frontend
- ✅ Updated general talent categories: 160 talents across 14 service categories (Services à la personne, Bâtiment, Commerce, Multimédia, Santé, etc.)
- ✅ Updated cinema talent categories: 57 talents across 7 skill categories (artistic, physical, manual, social, technical, professional experience, personal qualities)
- ✅ Enhanced cinema.py to filter only cinema-tagged talents in registration forms
- ✅ Fixed city display in admin listings to show residence_city instead of city (more relevant for recruitment)
- ✅ Updated filters in main routes to use residence_city_id for accurate location-based searches
- ✅ Enhanced documentation with comprehensive change tracking
- ✅ **[02/11/2025]** Fixed cinema talent profile photo display issue - corrected file path from `uploads/photos/` to `uploads/cinema_photos/` in project badge generation (cinema.py) and talent assignment view template, ensuring profile photos display correctly in all locations (talent list, profile page, PDF, badges)
- ✅ **[02/11/2025]** Major enhancements to statistics, city selection, and PDF customization:
  - Replaced Moroccan city statistics with world city statistics on admin dashboard homepage
  - Added "Autres" (Other) option for all countries in city selection dropdowns - 194 special city entries added
  - Implemented dynamic PDF footer system with admin customization for 4 PDF types (Talent List, Talent Card, Cinema Talent List, Cinema Talent Card)
  - Removed unnecessary PageBreak in Talent PDF that was causing blank second pages
  - Fixed Cinema Talent PDF header: removed subtitle text "Profil Cinématographique - Talents du Cinéma Africain" and green line, kept only blue separator line
  - Enhanced cinema project badge generation to properly display profile photo or ID photo with multiple path fallbacks instead of placeholder image
- ✅ **[02/11/2025]** Implemented image lightbox functionality for profile photo viewing:
  - Added JavaScript-based lightbox for viewing profile photos and gallery images in full screen
  - Created `/app/static/js/image-lightbox.js` - standalone lightbox module with keyboard navigation support (Esc, Arrow keys)
  - Created `/app/static/css/lightbox.css` - responsive lightbox styles with mobile breakpoints
  - Updated `profile/view.html` to enable lightbox on talent profile photos
  - Updated `cinema/profile_view.html` to enable lightbox on cinema talent profile photos and gallery images with navigation between photos
  - Gallery images in cinema profiles can be navigated using previous/next buttons or keyboard arrows
  - Lightbox features: click to enlarge, keyboard navigation, image counter for galleries, responsive design
- ✅ **[02/11/2025]** Implemented image cropping functionality with Cropper.js for all photo uploads:
  - Integrated Cropper.js library (v1.6.1) via CDN for professional image cropping capabilities
  - Created `/app/static/js/image-cropper.js` - standalone cropper manager with 1:1 aspect ratio enforcement
  - Created `/app/static/css/image-cropper.css` - modern modal UI with gradient header and responsive design
  - Automatically intercepts all single-file image uploads and opens cropping modal
  - Features: zoom controls, 90° rotation, drag to reposition, high-quality output (800x800px JPEG)
  - Real-time preview of cropped image before form submission
  - Prevents distorted photos by enforcing square 1:1 ratio for all profile photos
  - Mobile-responsive design with touch support for crop adjustments
- ✅ **[02/11/2025]** Updated city naming convention from "Autres" to "Ville non listée":
  - Modified `init_essential_data.py` to create "Ville non listée" entries (code: VNL) for all 194 countries
  - Updated database schema to use more descriptive city option for unlisted locations
  - Improved user experience with clearer labeling in city selection dropdowns
  - Change applies to both general talent registration and cinema talent registration forms
- ✅ **[02/11/2025]** Enhanced city selection and PDF footer system:
  - Modified city API endpoints (`/api/cities` and `/api/v1/cities`) to always place "Ville non listée" at the bottom of city lists
  - Fixed sorting issue where "Ville non listée" appeared alphabetically in the middle instead of at the end
  - Added PDF footer customization to talent list export (pdf_footer_talent_list) - previously missing
  - Confirmed all 3 PDF export types now use the admin-configurable footer system (Talent List, Talent Card, Cinema Talent Card)
  - Improved user experience with consistent city dropdown ordering across all forms
- ✅ **[02/11/2025]** Integrated Bytez AI provider for multi-model AI services:
  - Added Bytez as a new AI provider option alongside OpenRouter, Perplexity, OpenAI, and Google Gemini
  - Updated `app/services/ai_provider_service.py` to support Bytez API with OpenAI-compatible chat completions endpoint
  - Added Bytez configuration section in admin settings UI (`app/templates/admin/settings/api_keys.html`)
  - Included popular open-source models: Qwen 2.5 72B Instruct, Llama 3.3 70B, Mistral 7B, DeepSeek V3
  - Added BYTEZ_API_KEY environment variable support in `config.py`
  - Bytez provides access to hundreds of open-source and closed-source models through unified API
  - Documentation: https://docs.bytez.com/model-api/docs/welcome

## External Dependencies

### Core Services
- **Database**: PostgreSQL (production), SQLite (development).
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