# Talento - Platform for Talent Centralization

## Overview
Talento is a professional web application designed to centralize and showcase talent profiles across Africa. It enables individuals to create comprehensive profiles with unique identifiers and QR codes. The platform features advanced administrative tools, AI-powered CV analysis, and multiple data export formats. Talento aims to be a robust, scalable solution for talent management and discovery, enhancing professional networking and recruitment across the continent. A key module, CINEMA, provides a dedicated system for talent registration with detailed fields and public accessibility.

## Recent Changes (October 21, 2025)
- **World Countries Database**: Expanded from 54 African countries to 194 world countries with ISO-2 codes and proper nationalities
- **Nationalities System**: Added comprehensive nationality list (Marocaine, Française, Algérienne, etc.) with emoji flags for proper form display; differentiated Congo nationalities (Congolaise Congo-Brazzaville vs Congolaise RDC)
- **Dynamic City Loading**: Implemented automatic city dropdown loading based on selected country via `/cinema/api/cities/<country_code>` endpoint with intelligent fallback to text input for countries without predefined cities
- **Expanded Cities Database**: Massively expanded city lists - now covering 60+ countries with 15-25 cities each (Morocco: 25, France: 25, Algeria: 20, Tunisia: 20, Senegal: 20, plus African, European, Asian, American, and Oceanian countries)
- **CINEMA Form Enhancement**: Nationality field now displays emoji flags alongside nationalities (🇲🇦 Marocaine, 🇫🇷 Française), city selection is dynamic dropdown
- **Backend ISO Conversion**: Country codes automatically converted to country names during form submission
- **Photo Upload Simplification**: Removed "Photo de profil" field from CINEMA registration, keeping only "Photo d'identité" and "Galerie de photos"
- **REST API v1**: Complete RESTful API with 25+ endpoints for authentication, users, talents, CINEMA, statistics, and data exports
- **API Documentation**: Comprehensive documentation in French and English with examples (api_docs/)
- **Postman Collection**: JSON collection for easy API testing with all endpoints pre-configured
- **CSRF Exemption**: API v1 routes exempt from CSRF protection for external client access
- **CINEMA Module Enhancement**: Complete redesign of registration form into 8 organized sections
- **Flag Integration**: Added emoji flags to all country dropdowns (using ISO-2 codes)
- **Expanded Languages**: Enriched language options to 60 languages with centralized LANGUAGES_CINEMA constant
- **Categorized Talents**: Organized talents into 6 categories with emojis (Performance, Arts & Media, Sports & Skills, etc.)
- **Enhanced Social Media**: Added TikTok and Snapchat fields with encrypted storage
- **TMDb Integration**: Server-side movie search API for tracking previous productions (optional, requires TMDB_API_KEY)
- **Database Migration**: Added tiktok_encrypted and snapchat_encrypted columns to cinema_talents table
- **Navigation Update**: CINEMA link moved from public header to authenticated-only header; public access via "Postuler en tant que talent cinéma" button on login page

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
- **Blueprints**: Organized into `main`, `auth`, `profile`, `admin`, `api`, `cinema`, and `api_v1` for modularity.

### REST API v1
- **Base URL**: `/api/v1`
- **Authentication**: Session-based (cookies)
- **CSRF Protection**: Exempt for all API v1 routes
- **Documentation**: Available in `api_docs/` (French & English)
- **Endpoints**:
  - Authentication: `/auth/login`, `/auth/logout`, `/auth/me`
  - Users: `/users` (list, get, delete, toggle-active)
  - Talents & Location: `/talents`, `/countries`, `/cities`
  - CINEMA: `/cinema/talents`, `/cinema/talents/:id`, `/cinema/stats`
  - Statistics: `/stats/overview`, `/stats/talents`
  - Exports: `/export/users/excel`, `/export/users/csv`, `/export/users/pdf`

### Constants & Configuration
- **Centralized Constants**: `app/constants.py` defines:
  - Standardized availability and talent categories for main platform
  - LANGUAGES_CINEMA: 60 language options for CINEMA module
  - TALENT_CATEGORIES: 6 categorized talent groups with emojis for CINEMA

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
- **Environment Variables**: 
  - **Required**: `SECRET_KEY`, `DATABASE_URL`, `ENCRYPTION_KEY`
  - **Optional**: `SENDGRID_API_KEY`, `OPENROUTER_API_KEY`, `SENDGRID_FROM_EMAIL`, `REPLIT_DEV_DOMAIN`, `TMDB_API_KEY`
  - API keys and sender email can be managed via admin settings for SendGrid/OpenRouter
  - TMDb API key enables movie search in CINEMA productions (fallback to manual text entry if not configured)

### Static Assets
- **CSS**: Tailwind CSS (CDN), custom corporate theme.
- **Uploads Directory**: Local storage for user-generated content.

## CINEMA Module

The CINEMA module is a specialized subsystem for managing film industry talents with enhanced features.

### CINEMA Registration Form Structure
The public registration form (`/cinema/register`) is organized into **8 color-coded sections**:

1. **Identité & Contact** (Blue) - Personal information, ID document, and contact details merged into one section
2. **Origines** (Green) - Multiple ethnicities selection, country of origin, and nationality
3. **Résidence** (Purple) - Current country and city of residence
4. **Langues** (Cyan) - Multi-select from 60 languages (Afrikaans, Albanais, Amazigh, Amharique, Arabic, Bambara, French, English, Igbo, Swahili, Wolof, Yoruba, Zoulou, etc.)
5. **Caractéristiques physiques** (Orange) - Eye color, hair color/type, height, skin tone, build
6. **Talents** (Pink) - Organized into 6 categories with emojis:
   - 🎭 Arts de la scène (Acting, Singing, Dancing, Comedy, etc.)
   - 🎨 Arts visuels (Photography, Painting, Design, Makeup, etc.)
   - 🎵 Musique (Musician, Composer, DJ, Sound Engineer, etc.)
   - ⚽ Sports & Arts martiaux (Stunt work, Martial arts, Acrobatics, etc.)
   - 🎬 Techniques & Créatives (Choreography, Directing, Screenwriting, etc.)
   - ✨ Autres (Modeling, Magic, Mime, etc.)
7. **Réseaux sociaux** (Indigo) - All platforms including Facebook, Instagram, TikTok, Snapchat, YouTube, Twitter, LinkedIn (encrypted storage)
8. **Photos & Productions** (Red) - Photo uploads + movie search integration

### CINEMA Access Points
- **Public Access**: "Postuler en tant que talent cinéma" button on login page (`/auth/login`) redirects to public registration form
- **Authenticated Access**: CINEMA link in navigation header (visible only after login) leads to CINEMA dashboard (`/cinema/dashboard`)

### CINEMA Features

#### Country Display Enhancement
- All country dropdowns (origin, residence, nationality) display emoji flags generated from ISO-2 codes
- Countries are sorted alphabetically for easy selection
- Flag generation: `Country.flag` property converts country codes to Unicode flag emojis

#### TMDb Integration (Optional)
- **Service**: `app/services/movie_service.py` provides server-side TMDb API proxy
- **API Endpoint**: `/cinema/api/search_movies` accepts query parameter and returns film/TV results
- **Features**: Real-time search, poster images, year display, type identification (Film/Série TV)
- **Frontend**: JavaScript-powered autocomplete with visual movie cards
- **Fallback**: Manual text entry area if TMDb is not configured or search fails
- **Data Storage**: Selected productions saved as JSON array in `previous_productions` field

#### Social Media Encryption
All social media fields are encrypted using Fernet before storage:
- facebook_encrypted, instagram_encrypted, linkedin_encrypted
- twitter_encrypted, youtube_encrypted
- tiktok_encrypted, snapchat_encrypted

#### Multi-Select Fields
Several fields support multiple selections stored as JSON arrays:
- ethnicities (15+ options)
- languages_spoken (50+ languages)
- other_talents (categorized into 6 groups)

### CINEMA Data Model
The `CinemaTalent` model (`app/models/cinema_talent.py`) includes:
- Personal info with encrypted ID document
- Origins with multiple ethnicities support
- Separate fields for origin vs. residence locations
- Physical characteristics
- JSON arrays for languages and talents
- Encrypted contact and social media
- Photo storage (profile, ID, gallery)
- Previous productions as JSON

### CINEMA Routes
- `/cinema/register` - Public registration form (GET/POST)
- `/cinema/talents` - List view (authenticated)
- `/cinema/dashboard` - Statistics overview (authenticated)
- `/cinema/api/search_movies` - TMDb proxy endpoint