# Talento - Plateforme de Centralisation des Talents

## Overview
Talento is an intelligent web application designed to centralize talent profiles, including skills, CVs, portfolios, and contact information. Each profile automatically generates a unique code and a QR code for easy sharing. The platform aims to streamline talent management and sharing. Key capabilities include AI-powered CV analysis, advanced export options, and a comprehensive administrator dashboard, reflecting a business vision to enhance talent visibility and recruitment efficiency.

## User Preferences
I prefer clear and concise explanations. When proposing changes, please outline the high-level approach first and ask for confirmation before diving into detailed implementation. Focus on delivering robust and scalable solutions. I value iterative development and expect the agent to integrate seamlessly with the existing architecture. Do not make changes to the `replit.md` file without explicit instruction.

## System Architecture
Talento is built on a Flask (Python 3.11) backend utilizing SQLAlchemy for ORM and PostgreSQL for the database. Authentication is handled by Flask-Login, and sensitive data is encrypted using Fernet. The frontend uses Jinja2 templates, styled with Tailwind CSS 3.4.

**Key Architectural Decisions & Features:**
-   **AI-Powered CV Analysis**: Integrates OpenRouter for automated CV scoring, skill detection, and personalized recommendations.
-   **Robust Data Management**: Features an auto-repairing migration script (`migrations_init.py`) for database consistency and idempotent seeding of essential data (countries, cities, talents, admin account).
-   **Advanced Admin Dashboard**: Provides comprehensive filtering capabilities (text, QR code, talents, location, availability, CV/portfolio presence, registration dates) and multi-format exports (Excel, CSV, PDF).
-   **Unique Profile Identification**: Each user profile generates a unique alphanumeric code (e.g., `PP-VVV-NNNN-G`) and a personal QR code.
-   **Security**: Implements password hashing (bcrypt), file validation, size limits for uploads, unique email enforcement, and admin route protection. Encryption of sensitive data is mandatory.
-   **UI/UX**: Features a colorful and structured design for user registration, organizing information into distinct sections (Identity, Contact, Location, Talents, Documents, Social Networks) with outline-style icons. Includes support for 54 African countries with emoji flags and 74 talents across 14 categories.
-   **Services**: Dedicated services for CV analysis (`cv_analyzer.py`) and various export formats (`export_service.py`).

## External Dependencies
-   **Database**: PostgreSQL (Replit Helium)
-   **AI**: OpenRouter API (`OPENROUTER_API_KEY`) for CV analysis.
-   **Email**: SendGrid API (`SENDGRID_API_KEY`) or custom SMTP for notifications.
-   **Python Libraries**: Flask, SQLAlchemy, Flask-Login, Flask-Mail, Flask-Migrate, Pillow, qrcode, pandas, openpyxl, reportlab, cryptography (for Fernet).
-   **Frontend Libraries**: Tailwind CSS 3.4, Vanilla JavaScript.