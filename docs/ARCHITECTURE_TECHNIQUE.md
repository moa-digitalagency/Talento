# Architecture Technique - taalentio.com

**Documentation Technique Detaillee**
**Version 2.0 | Decembre 2024**

---

## Table des matieres

1. [Vue d'ensemble](#vue-densemble)
2. [Stack technologique](#stack-technologique)
3. [Architecture applicative](#architecture-applicative)
4. [Structure du projet](#structure-du-projet)
5. [Base de donnees](#base-de-donnees)
6. [Securite](#securite)
7. [Services externes](#services-externes)
8. [API REST](#api-rest)
9. [Deploiement](#deploiement)

---

## Vue d'ensemble

taalentio.com est une application web monolithique basee sur Flask (Python), utilisant une architecture MVC (Model-View-Controller) avec separation claire des responsabilites.

### Diagramme d'architecture

```
                    ┌─────────────────────────────────────┐
                    │          NAVIGATEUR CLIENT          │
                    └──────────────────┬──────────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────┐
                    │         SERVEUR WEB (Gunicorn)      │
                    │              Port 5000              │
                    └──────────────────┬──────────────────┘
                                       │
                    ┌──────────────────▼──────────────────┐
                    │         APPLICATION FLASK           │
                    │                                     │
                    │  ┌───────────┐  ┌───────────────┐  │
                    │  │  Routes   │  │   Templates   │  │
                    │  │  (Views)  │  │   (Jinja2)    │  │
                    │  └─────┬─────┘  └───────────────┘  │
                    │        │                            │
                    │  ┌─────▼─────┐  ┌───────────────┐  │
                    │  │  Models   │  │   Services    │  │
                    │  │(SQLAlchemy│  │   (Logic)     │  │
                    │  └─────┬─────┘  └───────────────┘  │
                    └────────┼────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────────┐
        │PostgreSQL│  │ SendGrid │  │  OpenRouter  │
        │    DB    │  │  (Email) │  │    (IA)      │
        └──────────┘  └──────────┘  └──────────────┘
```

---

## Stack technologique

### Backend

| Technologie | Version | Role |
|-------------|---------|------|
| Python | 3.11 | Langage principal |
| Flask | 3.0.0 | Framework web |
| SQLAlchemy | 2.0+ | ORM base de donnees |
| Flask-Login | 0.6.3 | Gestion authentification |
| Flask-Migrate | 4.0.5 | Migrations base de donnees |
| Flask-WTF | - | Protection CSRF |
| Flask-Mail | 0.9.1 | Integration email |
| Gunicorn | - | Serveur WSGI production |

### Base de donnees

| Technologie | Role |
|-------------|------|
| PostgreSQL | Base de donnees principale |
| psycopg2-binary | Driver PostgreSQL Python |

### Frontend

| Technologie | Role |
|-------------|------|
| Jinja2 | Moteur de templates |
| Tailwind CSS | Framework CSS |
| JavaScript vanilla | Interactions client |

### Services externes

| Service | Role |
|---------|------|
| SendGrid | Envoi d'emails transactionnels |
| OpenRouter | API IA (Gemini) |
| OMDB (optionnel) | Recherche de films |

### Bibliotheques cles

| Bibliotheque | Role |
|--------------|------|
| bcrypt | Hachage mots de passe |
| cryptography (Fernet) | Chiffrement donnees |
| Pillow | Traitement images |
| PyPDF2 | Lecture PDF |
| python-docx | Lecture documents Word |
| reportlab | Generation PDF |
| qrcode | Generation QR codes |
| APScheduler | Planification taches |
| pandas | Traitement donnees |
| openpyxl | Export Excel |

---

## Architecture applicative

### Pattern MVC

**Models (app/models/)**
- Definition des entites
- Relations entre tables
- Logique metier basique

**Views (app/routes/)**
- Points d'entree HTTP
- Validation des requetes
- Rendu des templates

**Controllers (app/services/)**
- Logique metier complexe
- Integration services externes
- Traitement des donnees

### Blueprints Flask

L'application est organisee en blueprints :

| Blueprint | Prefix | Description |
|-----------|--------|-------------|
| auth | /auth | Authentification |
| profile | /profile | Profils utilisateurs |
| admin | /admin | Administration |
| main | / | Pages principales |
| api | /api | API interne |
| cinema | /cinema | Module CINEMA |
| presence | /presence | Gestion presences |
| legal | /legal | Pages legales |
| sitemap | /sitemap | SEO |
| api_v1 | /api/v1 | API REST v1 |

---

## Structure du projet

```
taalentio.com/
├── app/
│   ├── __init__.py          # Factory application Flask
│   ├── constants.py         # Constantes globales
│   ├── scheduler.py         # Taches planifiees
│   │
│   ├── models/              # Modeles SQLAlchemy
│   │   ├── __init__.py
│   │   ├── user.py          # Utilisateurs
│   │   ├── talent.py        # Talents et associations
│   │   ├── cinema_talent.py # Talents cinema
│   │   ├── production.py    # Boites de production
│   │   ├── project.py       # Projets et assignations
│   │   ├── attendance.py    # Presences
│   │   ├── location.py      # Pays et villes
│   │   ├── settings.py      # Parametres application
│   │   ├── activity_log.py  # Journaux activite
│   │   ├── security_log.py  # Journaux securite
│   │   ├── email_log.py     # Journaux emails
│   │   └── name_tracking.py # Surveillance noms
│   │
│   ├── routes/              # Controleurs/Vues
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentification
│   │   ├── profile.py       # Profils
│   │   ├── admin.py         # Administration
│   │   ├── main.py          # Pages principales
│   │   ├── api.py           # API interne
│   │   ├── cinema.py        # Module cinema
│   │   ├── presence.py      # Presences
│   │   ├── legal.py         # Pages legales
│   │   ├── sitemap.py       # Sitemap SEO
│   │   └── api_v1/          # API REST v1
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── talents.py
│   │       ├── cinema.py
│   │       ├── stats.py
│   │       ├── exports.py
│   │       └── logging.py
│   │
│   ├── services/            # Services metier
│   │   ├── __init__.py
│   │   ├── email_service.py     # Envoi emails
│   │   ├── export_service.py    # Exports donnees
│   │   ├── cv_analyzer.py       # Analyse CV par IA
│   │   ├── ai_matching_service.py # Matching IA
│   │   ├── ai_provider_service.py # Abstraction providers IA
│   │   ├── backup_service.py    # Sauvegardes
│   │   ├── cache_service.py     # Gestion cache
│   │   ├── database_service.py  # Operations DB
│   │   ├── logging_service.py   # Journalisation
│   │   ├── maintenance_service.py # Maintenance
│   │   ├── movie_service.py     # Recherche films
│   │   ├── seo_service.py       # SEO
│   │   ├── update_service.py    # Mises a jour
│   │   └── watchlist_service.py # Surveillance noms
│   │
│   ├── utils/               # Utilitaires
│   │   ├── __init__.py
│   │   ├── encryption.py        # Chiffrement Fernet
│   │   ├── file_handler.py      # Gestion fichiers
│   │   ├── id_generator.py      # Generation codes uniques
│   │   ├── qr_generator.py      # Generation QR codes
│   │   ├── email_service.py     # Helpers email
│   │   ├── activity_logger.py   # Middleware logging
│   │   ├── auto_migrate.py      # Migration auto
│   │   ├── validation_service.py # Validation donnees
│   │   ├── cinema_code_generator.py
│   │   └── project_code_generator.py
│   │
│   ├── data/                # Donnees statiques
│   │   ├── world_countries.py   # 54 pays africains
│   │   └── world_cities.py      # Villes par pays
│   │
│   ├── templates/           # Templates Jinja2
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── profile/
│   │   ├── admin/
│   │   ├── cinema/
│   │   ├── presence/
│   │   ├── legal/
│   │   └── includes/
│   │
│   └── static/              # Fichiers statiques
│       ├── css/
│       ├── js/
│       ├── img/
│       └── uploads/
│           ├── photos/
│           ├── cvs/
│           ├── qrcodes/
│           └── cinema_photos/
│
├── docs/                    # Documentation
├── logs/                    # Journaux application
├── migrations_archive/      # Scripts migration
├── api_docs/               # Documentation API
│
├── app.py                  # Point d'entree
├── config.py               # Configuration
├── requirements.txt        # Dependances Python
├── database_manager.py     # Outil gestion DB
└── init_essential_data.py  # Initialisation donnees
```

---

## Base de donnees

### Schema relationnel

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   users     │────<│ user_talents │>────│   talents   │
└─────────────┘     └──────────────┘     └─────────────┘
      │
      │ FK
      ▼
┌─────────────┐     ┌──────────────┐
│  countries  │     │    cities    │
└─────────────┘     └──────────────┘

┌──────────────┐    ┌───────────────┐    ┌─────────────┐
│cinema_talents│    │project_talents│    │   projects  │
└──────────────┘    └───────────────┘    └─────────────┘
                          │                     │
                          │ FK                  │ FK
                          ▼                     ▼
                    ┌──────────────┐     ┌─────────────┐
                    │  attendances │     │ productions │
                    └──────────────┘     └─────────────┘

┌──────────────┐    ┌───────────────┐    ┌─────────────┐
│ app_settings │    │ activity_logs │    │security_logs│
└──────────────┘    └───────────────┘    └─────────────┘

┌──────────────┐    ┌───────────────┐
│  email_logs  │    │ name_tracking │
└──────────────┘    └───────────────┘
```

### Tables principales

**users** - Utilisateurs standards
- id, unique_code, first_name, last_name, email
- password_hash, date_of_birth, gender
- phone_encrypted, whatsapp_encrypted, address_encrypted
- country_id, city_id, nationality
- photo_filename, cv_filename, qr_code_filename
- is_admin, role, account_active
- created_at, updated_at

**talents** - Categories de talents
- id, name, emoji, category, tag, is_active

**user_talents** - Association utilisateurs-talents
- id, user_id, talent_id, created_at

**cinema_talents** - Talents cinematographiques
- id, unique_code
- first_name, last_name, gender, date_of_birth
- id_document_type, id_document_number_encrypted
- ethnicities, nationality, country_of_residence, city_of_residence
- languages_spoken, years_of_experience
- talent_types, other_talents
- eye_color, hair_color, hair_type, height, skin_tone, build
- profile_photo_filename, gallery_photos
- email, phone_encrypted, whatsapp_encrypted
- reseaux sociaux (encrypted)
- created_at, updated_at, is_active

**productions** - Societes de production
- id, name, logo_url, description, specialization
- coordonnees, contact, reseaux sociaux
- founded_year, ceo, employees_count
- certifications, awards
- is_active, is_verified, created_by

**projects** - Projets de production
- id, name, production_type
- production_company_id
- origin_country, shooting_locations
- start_date, end_date, status
- is_active, created_by

**project_talents** - Assignation talents aux projets
- id, project_id, cinema_talent_id
- talent_type, role_description
- project_code, badge_generated, badge_filename
- assigned_at, assigned_by

**attendances** - Presences
- id, project_id, cinema_talent_code
- date, check_in_time, check_out_time
- recorded_by, created_at, updated_at

---

## Securite

### Chiffrement des donnees

**Algorithme** : Fernet (AES-128 CBC)

**Donnees chiffrees** :
- Numeros de telephone
- Adresses postales
- Numeros de documents d'identite
- Tous les liens reseaux sociaux

**Implementation** :
```python
# app/utils/encryption.py
from cryptography.fernet import Fernet

def encrypt_sensitive_data(data):
    key = get_encryption_key()
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_sensitive_data(encrypted_data):
    key = get_encryption_key()
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()
```

### Authentification

**Hachage mots de passe** : bcrypt (12 rounds)

**Sessions** : Flask-Login avec cookies securises

**Protection CSRF** : Flask-WTF sur tous les formulaires

### Roles et permissions

| Role | Permissions |
|------|-------------|
| user | Lecture/modification profil personnel |
| recruteur | user + lecture tous profils + exports |
| presence | user + gestion presences |
| admin | Acces complet |

### Upload fichiers

- Validation type MIME (python-magic)
- Limitation taille (5 Mo photos, 10 Mo CV)
- Renommage UUID
- Stockage separe par type

---

## Services externes

### SendGrid (Emails)

**Configuration** :
- Variable : SENDGRID_API_KEY
- Expediteur : configurable via AppSettings

**Types d'emails** :
- Confirmation inscription
- Envoi identifiants
- Notification selection projet
- Match IA
- Recapitulatif hebdomadaire
- Alerte surveillance

### OpenRouter (IA)

**Configuration** :
- Variable : OPENROUTER_API_KEY
- Modeles : google/gemini-2.0-flash-001:free

**Utilisations** :
- Analyse de CV
- Matching talents/postes
- Casting IA cinema

### OMDB (Films)

**Configuration** :
- Variable : OMDB_API_KEY

**Utilisation** :
- Recherche films pour historique productions

---

## API REST

### Base URL

```
/api/v1
```

### Authentification

Session-based via cookies.

**Login** :
```
POST /api/v1/auth/login
Body: { "email": "...", "password": "..." }
```

### Endpoints principaux

**Utilisateurs** :
- GET /api/v1/users - Liste paginee
- GET /api/v1/users/{id} - Detail
- PUT /api/v1/users/{id} - Mise a jour (admin)
- DELETE /api/v1/users/{id} - Suppression (admin)

**Talents** :
- GET /api/v1/talents - Liste
- GET /api/v1/talents/{id} - Detail
- GET /api/v1/talents/{id}/users - Utilisateurs par talent

**Cinema** :
- GET /api/v1/cinema/talents - Liste talents cinema
- GET /api/v1/cinema/talents/{id} - Detail
- GET /api/v1/cinema/productions - Productions
- GET /api/v1/cinema/projects - Projets

**Statistiques** :
- GET /api/v1/stats/overview - Vue d'ensemble
- GET /api/v1/stats/users - Stats utilisateurs
- GET /api/v1/stats/cinema - Stats cinema

**Exports** :
- GET /api/v1/exports/users/excel
- GET /api/v1/exports/users/csv
- GET /api/v1/exports/cinema/excel

---

## Deploiement

### Prerequis

- Python 3.11+
- PostgreSQL 14+
- Espace disque 5 Go minimum

### Variables d'environnement

```bash
# Base de donnees
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Securite
SECRET_KEY=<cle-secrete-32-chars>
ENCRYPTION_KEY=<cle-fernet-base64>

# Services
SENDGRID_API_KEY=<cle-sendgrid>
OPENROUTER_API_KEY=<cle-openrouter>

# Application
PORT=5000
FLASK_ENV=production
```

### Commandes de demarrage

**Developpement** :
```bash
python app.py
```

**Production** :
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

### Initialisation

```bash
# Installer dependances
pip install -r requirements.txt

# Initialiser donnees
python init_essential_data.py

# Demarrer
python app.py
```

---

*Documentation technique par MOA Digital Agency LLC - www.myoneart.com*
