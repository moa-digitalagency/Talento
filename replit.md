# Talento - Platform for Talent Centralization

## Overview

Talento is a professional web application designed to centralize and showcase talent profiles across Africa. The platform enables individuals to create comprehensive professional profiles with unique identifiers, QR codes, and multi-talent capabilities. It features advanced administrative tools for managing users, AI-powered CV analysis, and multiple data export formats (Excel, PDF, CSV).

## Recent Changes

**October 20, 2025 - Version 2.1.0**
1. **Beautiful Registration Form Redesign** with dotted borders:
   - 9 sections with unique colored dotted borders (3px)
   - Each section has a subtle gradient background
   - Color themes: blue (Identity), green (Contact), red (Location), purple (Experience), orange (Talents), cyan (Documents), pink (Social), yellow (Availability), indigo (Work Mode)
   - Hover effects with elevation
   - Step indicators (1/9 through 9/9)

2. **Extended Moroccan Cities Database**:
   - Expanded from 30 to 79+ cities
   - All cities sorted alphabetically
   - Unique city codes (3-letter codes)
   - Coverage of all major Moroccan regions

3. **New Form Sections**:
   - **Section 8 - Availability**: Work time preferences (full-time, part-time, flexible, etc.) with hourly/monthly rate fields
   - **Section 9 - Work Mode**: Remote, on-site, hybrid, nomadic, etc.

**Earlier October 20, 2025**
4. **Database Expansion**: Extended Moroccan cities from 12 to 30 cities covering major urban centers
5. **Enhanced User Model**: Added `languages` (TEXT) and `education` (TEXT) fields with proper database migration
6. **Enriched Demo Profiles**: All 5 demo users now include complete information:
   - Personal details: dates of birth, phone numbers, WhatsApp contacts
   - Professional info: addresses, work preferences, hourly/monthly rates
   - Skills: languages spoken and education history
   - Work modes and availability status
7. **Redesigned Registration Form**: Complete UI/UX overhaul with:
   - 7 color-coded sections (blue, green, red, violet, orange, cyan, pink)
   - Centered, responsive layout for all screen sizes
   - Visual step indicators (1/7, 2/7, etc.)
   - Modern gradient backgrounds and improved spacing
8. **Elaborate Homepage Dashboard**: New comprehensive metrics display:
   - Real-time statistics cards (users, talents, cities, countries)
   - Availability breakdowns with progress bars
   - Top 10 talents with usage counts
   - Category distribution analysis
   - Work mode statistics (remote, on-site, hybrid)
   - Top 5 cities by user count
   - Recent user profiles showcase
9. **Migration Safety**: Implemented `SKIP_AUTO_MIGRATION` environment variable to prevent recursive initialization loops

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Framework
- **Backend Framework**: Flask 3.0.0 with Python 3.11
  - Chosen for its lightweight nature and flexibility for rapid development
  - Provides clear separation of concerns through Blueprint-based routing
  - Easy integration with various extensions (SQLAlchemy, Login, Mail, Migrate)

### Database Architecture
- **ORM**: SQLAlchemy with Flask-SQLAlchemy 3.1.1
  - Provides database-agnostic interface supporting SQLite (development) and PostgreSQL (production)
  - Enables model-based database interactions with relationship management
  - Migration support through Flask-Migrate for schema evolution
  
- **Data Models**:
  - **User**: Core entity storing personal information, credentials, and profile data
  - **Talent**: Catalog of available skills/talents with emoji representation
  - **UserTalent**: Many-to-many relationship linking users to their talents
  - **Country/City**: Location reference data for geographic information
  
- **Security Features**:
  - Encrypted storage for sensitive fields (phone, social media links, addresses)
  - Uses Fernet symmetric encryption with derived keys from environment configuration
  - Password hashing with Werkzeug security utilities

### Unique Identification System
- **Code Format**: PPVVVNNNNG (10 characters without dashes, displayed with dashes)
  - PP: 2-letter country code
  - VVV: 3-letter city code
  - NNNN: 4 random digits
  - G: Gender identifier (M/F/N)
- **QR Code Generation**: Automatic QR code creation linking to profile view URLs
- **Validation**: Regex-based validation and database uniqueness checks

### Authentication & Authorization
- **User Authentication**: Flask-Login for session management
  - Email-based login with password hashing
  - Role-based access control (admin vs. regular users)
  - Protected routes using decorators (@login_required, @admin_required)
  
- **Password Management**: 
  - Random password generation for new users
  - Secure password hashing with bcrypt
  - Email delivery of credentials to new users

### File Management
- **Upload Handling**:
  - Photos: PNG, JPG, JPEG (max 5MB)
  - CVs: PDF, DOC, DOCX (max 10MB)
  - Secure filename generation using UUIDs
  - Organized storage in separate folders (photos/, cvs/, qrcodes/)
  
- **Document Processing**:
  - PDF text extraction using PyPDF2
  - DOCX text extraction using python-docx
  - Image processing with Pillow for photo optimization

### AI Integration
- **CV Analysis Service**:
  - Integration with OpenRouter AI API for intelligent CV analysis
  - Automated extraction of skills, experience, and qualifications
  - Profile scoring (0-100) based on completeness and quality
  - Personalized recommendations for profile improvement
  - Detection of strengths and weaknesses
  
- **Rationale**: Provides automated talent assessment and helps users improve their profiles without manual review

### Data Export System
- **Export Formats**:
  - **Excel (XLSX)**: Structured data with formatting using openpyxl
  - **CSV**: Plain data export for analysis using pandas
  - **PDF**: Professional reports using ReportLab
    - List view: Comprehensive multi-user reports
    - Individual view: Detailed talent sheets with photos and complete information
  
- **Export Service Architecture**: Centralized service class handling all export operations with consistent data transformation

### Email System
- **Email Service**: Flask-Mail with SendGrid support
  - Confirmation emails with login credentials for new registrations
  - HTML-formatted professional email templates
  - Support for both SMTP and SendGrid API configurations
  
- **Design Choice**: Dual configuration allows flexibility for different deployment environments

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask default)
- **CSS Framework**: Tailwind CSS via CDN
  - Utility-first approach for rapid UI development
  - Custom corporate theme overrides for professional appearance
  - Responsive design patterns for mobile compatibility
  
- **UI Components**:
  - Multi-step registration form with visual progress indicators
  - Advanced filtering system with multiple criteria
  - Real-time search capabilities
  - Dashboard with statistics and visualizations

### Routing Structure
- **Blueprint Organization**:
  - `main`: Public pages (index, about)
  - `auth`: Authentication flows (login, logout, register)
  - `profile`: User profile management (dashboard, view, edit)
  - `admin`: Administrative functions (user management, exports, analytics)
  - `api`: JSON endpoints for dynamic data (countries, cities, talents)

### Migration & Database Initialization
- **Migration Strategy**: Custom migration script (migrations_init.py)
  - Automatic table creation if missing
  - Column addition for schema evolution
  - Data seeding for reference tables (countries, cities, talents)
  - Idempotent operations to prevent duplicate data
  
- **Rationale**: Provides robust database setup without external migration tools, suitable for rapid deployment

## External Dependencies

### Core Services
- **Database**: PostgreSQL (production) / SQLite (development)
  - PostgreSQL required for production via DATABASE_URL environment variable
  - SQLite fallback for local development
  
- **AI Service**: OpenRouter API
  - Requires OPENROUTER_API_KEY environment variable
  - Used for CV analysis and profile scoring
  - RESTful API integration for chat completions

### Email Delivery
- **SendGrid** (optional): Professional email delivery service
  - Configured via SENDGRID_API_KEY environment variable
  - Alternative to standard SMTP configuration
  
- **SMTP** (alternative): Standard email protocol
  - Configured via MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
  - TLS support for secure email transmission

### Python Libraries
- **Web Framework**: Flask ecosystem (Flask, Flask-SQLAlchemy, Flask-Login, Flask-Mail, Flask-Migrate)
- **Database**: psycopg2-binary (PostgreSQL adapter), SQLAlchemy (ORM)
- **Security**: cryptography (encryption), bcrypt (password hashing)
- **File Processing**: Pillow (images), PyPDF2 (PDF reading), python-docx (Word documents)
- **Data Export**: pandas (CSV), openpyxl (Excel), ReportLab (PDF generation)
- **Utilities**: qrcode (QR generation), requests (HTTP client), email-validator (email validation)
- **Environment**: python-dotenv (configuration management)

### Configuration Requirements
- **Required Environment Variables**:
  - SECRET_KEY: Flask session encryption
  - DATABASE_URL: Database connection string
  - ENCRYPTION_KEY: Data encryption key for sensitive fields
  - OPENROUTER_API_KEY: AI service authentication (optional but recommended)
  
- **Optional Environment Variables**:
  - MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD: Email configuration
  - SENDGRID_API_KEY: SendGrid email service
  - REPLIT_DEV_DOMAIN: Deployment domain for QR code URLs

### Static Assets
- **Tailwind CSS**: CDN-delivered CSS framework
- **Custom CSS**: Corporate theme overrides in static/css/
- **Uploads Directory**: Local file storage for user uploads (photos, CVs, QR codes)