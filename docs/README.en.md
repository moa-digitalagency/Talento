# Talento - Talent Centralization Platform

> Professional platform for centralizing and showcasing talent profiles across Africa

**Version:** 2.0  
**Last Updated:** November 1, 2025

## 📖 Overview

Talento (taalentio.com) is a comprehensive web application designed to centralize and showcase professional talent profiles, with a specialized CINEMA module for the film industry. The platform enables individuals to create detailed profiles with unique identifiers and QR codes, while offering advanced administrative tools and AI-powered features.

## 🎯 Key Features

### Core Features
- **Unique Profile System** - Each talent receives a unique code and QR code
- **CINEMA Module** - Specialized features for film industry professionals
- **Multi-Role Access** - Admin, Recruiter, Presence, and User roles
- **AI Integration** - CV analysis and talent matching
- **Advanced Search** - Find talents by skills, location, and characteristics
- **Export Tools** - Excel, CSV, and PDF data export

### Administrative Features
- **Activity Logging** - Complete audit trail of all user actions
- **Security Monitoring** - Failed login tracking and suspicious activity detection
- **Email System** - Automated notifications and weekly recaps
- **Backup & Restore** - Complete application backup capabilities
- **API Keys Management** - Centralized configuration for external services

## 🏗️ Technology Stack

**Backend:**
- Flask 3.0.0 (Python 3.11)
- SQLAlchemy with PostgreSQL/SQLite support
- Flask-Login for authentication
- APScheduler for automated tasks

**Frontend:**
- Jinja2 templates
- Tailwind CSS (CDN)
- Vanilla JavaScript

**AI Services:**
- OpenRouter API
- Perplexity AI
- OpenAI
- Google Gemini

**Other Services:**
- SendGrid (Email)
- OMDB API (Cinema module)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (production) or SQLite (development)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/talento.git
cd talento

# Install Python dependencies
pip install -r requirements.txt

# Initialize the database
python database_manager.py --force

# Start the application
python app.py
```

### Environment Variables

```bash
SECRET_KEY=your_secret_key
ENCRYPTION_KEY=your_encryption_key
PORT=5000
SKIP_AUTO_MIGRATION=1
```

## 📚 Documentation

### Main Documents (Available in FR/EN)
- **[README](./README.en.md)** - This file
- **[CHANGELOG](./CHANGELOG.en.md)** - Version history
- **[DEPLOYMENT](./DEPLOYMENT.en.md)** - Deployment guide
- **[TECHNICAL_DOCUMENTATION](./TECHNICAL_DOCUMENTATION.en.md)** - Technical details
- **[DATABASE_MANAGER](./DATABASE_MANAGER.en.md)** - Database management guide
- **[DATABASE_USAGE](./DATABASE_USAGE.en.md)** - Database usage guide

### French Versions
All documents are also available in French with `.fr.md` extension.

## 👥 Default Admin Account

After initialization:
- **Email:** admin@talento.com
- **Code:** MAN0001RAB
- **Password:** @4dm1n

⚠️ **Important:** Change the password immediately after first login!

## 🗂️ Project Structure

```
talento/
├── app/                    # Main application
│   ├── data/              # Reference data (countries, cities, talents)
│   ├── models/            # Database models
│   ├── routes/            # Application routes
│   ├── services/          # Business logic
│   ├── static/            # Static files (CSS, JS, images)
│   ├── templates/         # HTML templates
│   └── utils/             # Utilities
├── docs/                  # Documentation (FR/EN)
├── logs/                  # Application logs
├── database_manager.py    # Database management tool
├── app.py                 # Application entry point
├── config.py             # Configuration
└── requirements.txt      # Python dependencies
```

## 🔒 Security Features

- Password hashing with Werkzeug
- Sensitive data encryption with Fernet
- Activity and security logging
- Failed login attempt tracking
- Role-based access control
- QR code generation for secure profile access

## 🌍 Internationalization

The platform is primarily in French but includes:
- Multi-language country and city data
- Bilingual documentation (FR/EN)
- Support for international phone numbers
- Nationality tracking with emoji flags

## 📧 Contact & Support

**MOA Digital Agency LLC**  
Developer: Aisance KALONJI  
Email: moa@myoneart.com  
Website: www.myoneart.com

## 📄 License

Copyright © 2025 MOA Digital Agency LLC. All rights reserved.

---

*For French documentation, see [README.fr.md](./README.fr.md)*
