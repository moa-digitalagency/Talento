# Talento - Technical Documentation

> Comprehensive technical documentation for the Talento platform

**Version:** 2.0  
**Last Updated:** November 1, 2025

## 📖 Overview

This document provides detailed technical information about the Talento platform architecture, implementation, and best practices.

## 🏗️ Architecture

### Application Framework

**Backend:** Flask 3.0.0 (Python 3.11)
- Modular organization using Blueprints
- SQLAlchemy ORM for database abstraction
- Flask-Login for session management
- APScheduler for background tasks

**Frontend:** Server-side rendered with Jinja2
- Tailwind CSS (CDN) for styling
- Vanilla JavaScript for interactivity
- No heavy frontend framework dependency

### Database Architecture

**ORM:** SQLAlchemy with Flask-SQLAlchemy

**Supported Databases:**
- PostgreSQL (production recommended)
- SQLite (development)

**Key Models:**
- `User` - User accounts and authentication
- `Talent` - Main talent profiles
- `CinemaTalent` - Specialized cinema industry profiles
- `Production` - Production companies
- `Project` - Film/media projects
- `Country`, `City` - Location data
- `ActivityLog` - Activity tracking
- `SecurityLog` - Security events
- `AppSettings` - Application configuration

### Unique Identification System

**Main Talent Profiles:** `PPGNNNNVVV`
- PP: Country code
- G: Gender code
- NNNN: Sequential number
- VVV: City code

**Cinema Profiles:** `PPVVVNNNNNG`
- PP: Country code
- VVV: City code  
- NNNN: Sequential number
- G: Gender code

**Project Codes:** `CCIIISSSNNN`
- CC: Country code
- III: City code
- SSS: Specialty code
- NNN: Sequential number

## 🔐 Security

### Authentication

**Method:** Flask-Login
**Features:**
- Email or unique code login
- Password hashing with Werkzeug
- Session management
- Remember me functionality

### Data Encryption

**Method:** Fernet (symmetric encryption)
**Encrypted Fields:**
- Sensitive personal data
- Identity documents
- Private contact information

### Access Control

**Roles:**
- **Admin** - Full system access
- **Recruteur** - Recruiter functions
- **Presence** - Attendance management
- **User** - Basic profile access

### Activity Logging

**Tracked Events:**
- Login/logout
- Profile creation/modification
- Data exports
- Settings changes
- File uploads
- Page views

**Security Logging:**
- Failed login attempts
- Suspicious activities
- IP blocking events
- Account lockouts

## 🗄️ File Management

### Upload System

**Supported File Types:**
- **Photos:** PNG, JPG, JPEG, GIF, WEBP
- **Documents:** PDF, DOCX, DOC
- **Data:** XLSX, XLS, CSV

**Storage Structure:**
```
app/static/uploads/
├── photos/      # Profile photos
├── cvs/         # Curriculum vitae
├── qrcodes/     # Generated QR codes
├── seo/         # SEO images
└── logos/       # Company logos
```

**Security Measures:**
- File extension validation
- File size limits
- Unique filename generation
- Secure path handling

## 🤖 AI Integration

### Supported Providers

1. **OpenRouter**
   - Multi-model access
   - Customizable model selection

2. **Bytez** (NEW)
   - Hundreds of open-source and closed-source models
   - Models: Qwen 2.5 72B, Llama 3.3 70B, Mistral 7B, DeepSeek V3
   - Unified API for all models
   - Documentation: https://docs.bytez.com

3. **Perplexity AI**
   - Models: llama-3.1-sonar (small/large/huge)
   - Online search capabilities

4. **OpenAI**
   - Models: GPT-4o, GPT-4-turbo, GPT-3.5-turbo
   - CV analysis and matching

5. **Google Gemini**
   - Models: gemini-2.0-flash-exp, gemini-1.5-pro
   - Advanced reasoning

### Features

- **CV Analysis** - Extract skills and experience
- **Talent Matching** - Find candidates by description
- **Job Description Analysis** - Match jobs to talents
- **Cinema Search** - Specialized film industry search

## 📧 Email System

### Provider

**SendGrid API**

### Email Types

- **Welcome emails** - New registrations
- **Login credentials** - Account information
- **Password resets** - Secure password recovery
- **Weekly recaps** - Admin summary emails

### Scheduling

**APScheduler** handles automated emails:
- Weekly recap: Sundays at 12:59 PM
- Configurable fields and recipients

## 📊 Data Export

### Supported Formats

1. **Excel (XLSX)**
   - Full talent data export
   - Formatted and styled sheets

2. **CSV**
   - Simple data export
   - Compatible with all tools

3. **PDF**
   - Professional talent reports
   - QR codes included
   - Custom formatting

### Export Features

- Filtered exports
- Custom field selection
- Batch processing
- Progress tracking

## 🔄 Backup & Restore

### Backup System

**Components:**
- Database dump (PostgreSQL/SQLite)
- Uploaded files (photos, CVs, documents)
- Configuration files
- QR codes

**Storage:**
- ZIP archives
- Timestamped filenames
- Automatic cleanup of old backups

### Restore Process

1. Upload backup ZIP file
2. Extract and validate contents
3. Restore database
4. Restore uploaded files
5. Verification and rollback if needed

## 🛣️ Routing Structure

### Blueprints

- **main** (`/`) - Public pages and landing
- **auth** (`/auth`) - Authentication routes
- **profile** (`/profile`) - User profile management
- **admin** (`/admin`) - Admin panel
- **cinema** (`/cinema`) - Cinema module
- **presence** (`/presence`) - Attendance tracking
- **api_v1** (`/api/v1`) - REST API
- **legal** (`/legal`) - Legal pages

### API Endpoints

**Base:** `/api/v1`

**Authentication:**
- `POST /api/v1/login` - User login
- `POST /api/v1/logout` - User logout

**Users:**
- `GET /api/v1/users` - List users
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/<id>` - Get user details

**Talents:**
- `GET /api/v1/talents` - List talents
- `GET /api/v1/talents/<code>` - Get talent by code

**Data:**
- `GET /api/v1/countries` - List countries
- `GET /api/v1/cities` - List cities

## 🎨 Frontend

### Template Engine

**Jinja2** with custom filters and functions

**Template Structure:**
```
app/templates/
├── base.html           # Base template
├── auth/               # Authentication pages
├── admin/              # Admin pages
├── cinema/             # Cinema module
├── profile/            # User profiles
└── legal/              # Legal pages
```

### Styling

**Tailwind CSS (CDN)**
- Utility-first approach
- Responsive design
- Dark mode ready

### JavaScript

**Vanilla JavaScript** for:
- Form validation
- Dynamic dropdowns
- AJAX requests
- Error logging

## 🚀 Performance

### Optimization Techniques

1. **Database Indexing**
   - Indexed foreign keys
   - Composite indexes for searches

2. **Query Optimization**
   - Eager loading with joinedload
   - Limited result sets
   - Pagination

3. **Caching**
   - Static file caching
   - Template caching

4. **File Serving**
   - Nginx for static files (production)
   - Optimized file paths

## 📝 Configuration

### Environment Variables

**Required:**
- `SECRET_KEY` - Flask secret key
- `ENCRYPTION_KEY` - Fernet encryption key
- `DATABASE_URL` - Database connection

**Optional:**
- `DEBUG` - Debug mode (default: False)
- `PORT` - Server port (default: 5000)
- `SENDGRID_API_KEY` - Email service
- `ADMIN_PASSWORD` - Default admin password

### Database Configuration

**PostgreSQL (Production):**
```
DATABASE_URL=postgresql://user:pass@host/dbname
```

**SQLite (Development):**
```
DATABASE_URL=sqlite:///talento_dev.db
```

## 🧪 Testing

### Manual Testing

1. **Functionality Tests**
   - User registration and login
   - Profile creation and editing
   - File uploads
   - Data export

2. **Security Tests**
   - Failed login attempts
   - Access control verification
   - Data encryption validation

3. **Performance Tests**
   - Large data set handling
   - Concurrent user simulation

## 📚 Additional Resources

- **Deployment Guide:** [DEPLOYMENT.en.md](./DEPLOYMENT.en.md)
- **Database Manager:** [DATABASE_MANAGER.en.md](./DATABASE_MANAGER.en.md)
- **Changelog:** [CHANGELOG.en.md](./CHANGELOG.en.md)
- **Main README:** [README.en.md](./README.en.md)

## 📞 Support

**MOA Digital Agency LLC**  
Developer: Aisance KALONJI  
Email: moa@myoneart.com  
Website: www.myoneart.com

---

*For French version, see [TECHNICAL_DOCUMENTATION.fr.md](./TECHNICAL_DOCUMENTATION.fr.md)*

*This is a condensed English version. For complete technical details, refer to the French documentation.*
