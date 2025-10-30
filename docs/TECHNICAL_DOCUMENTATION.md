# taalentio.com - Documentation Technique

## Table des Matières

1. [Architecture Système](#architecture-système)
2. [Modèles de Données](#modèles-de-données)
3. [Services](#services)
4. [Routes et Endpoints](#routes-et-endpoints)
5. [Sécurité](#sécurité)
6. [Installation et Configuration](#installation-et-configuration)
7. [Système de Codification](#système-de-codification)
8. [API REST v1](#api-rest-v1)

---

## Architecture Système

### Stack Technologique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| Backend Framework | Flask | 3.0.0 |
| Langage | Python | 3.11+ |
| Base de Données | PostgreSQL | 2.9.11 (psycopg2-binary) |
| ORM | SQLAlchemy | Latest via Flask-SQLAlchemy 3.1.1 |
| Authentification | Flask-Login | 0.6.3 |
| Templates | Jinja2 | 3.1.6 (via Flask) |
| CSS Framework | Tailwind CSS | CDN |
| Migration DB | Flask-Migrate (Alembic) | 4.0.5 |
| Email Service | SendGrid | Latest |
| AI Service | OpenRouter API | google/gemini-2.5-flash |

### Services IA

taalentio.com intègre trois services IA majeurs utilisant l'API OpenRouter pour automatiser le recrutement et le casting.

#### OpenRouter AI Integration

**Configuration Technique**:
- **Provider**: OpenRouter AI (https://openrouter.ai)
- **Endpoint**: `https://openrouter.ai/api/v1/chat/completions`
- **Modèles**:
  - CV Analyzer: `google/gemini-2.5-flash`
  - AI Matching (Standard & CINEMA): `google/gemini-2.0-flash-001:free`
- **API Key**: 
  - CV Analyzer: Variable d'environnement `OPENROUTER_API_KEY`
  - AI Matching: Table `app_settings` avec clé `openrouter_api_key` (via admin)
- **Température**: 0.3 (cohérence des résultats)
- **Timeout**: 
  - CV Analyzer: 30 secondes
  - AI Matching: 60 secondes
- **Coût**: Gratuit (modèles free)

**Headers (varient selon le service)**:

CV Analyzer:
```python
{
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'HTTP-Referer': os.environ.get('REPLIT_DEV_DOMAIN', 'http://localhost:5004')
}
```

AI Matching Services:
```python
{
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'HTTP-Referer': 'https://taalentio.com',
    'X-Title': 'taalentio.com - AI Matching'
}
```

**Gestion d'Erreurs**:
- Vérification de la présence de la clé API
- Timeout configuré par service
- Logging détaillé des erreurs (via Flask logger)
- Messages d'erreur utilisateur conviviaux
- Retour gracieux en cas d'échec

---

#### 1. CVAnalyzerService (app/services/cv_analyzer.py)

**Objectif**: Analyser automatiquement les CV uploadés et calculer un score de profil.

**Extraction de Texte**:

```python
def _extract_cv_text(cv_filename: str) -> str
```

Supporte:
- **PDF**: Extraction via PyPDF2.PdfReader
- **DOCX**: Extraction via python-docx.Document
- **TXT**: Lecture directe
- **Limite**: 3000 caractères pour optimisation

**Analyse IA**:

```python
def analyze_cv(cv_path: str, user_data: dict = None) -> dict
```

**Prompt de Scoring**:
L'IA évalue selon ces critères (0-100):
- Clarté et structure: 20 points
- Expérience pertinente: 25 points
- Compétences techniques: 25 points
- Formation et certifications: 15 points
- Réalisations mesurables: 15 points

**Résultat JSON**:
```json
{
    "success": true,
    "score": 75,
    "strengths": ["..."],
    "weaknesses": ["..."],
    "recommendations": ["..."],
    "skills_detected": ["..."],
    "experience_years": 5
}
```

**Calcul du Score de Complétude**:

```python
def calculate_profile_score(user: User) -> int
```

Points attribués:
- Nom/email/téléphone/date/pays/ville: 5 points chacun
- Photo: 10 points
- CV: 20 points
- Portfolio: 10 points
- Bio: 10 points
- Talents: 15 points
- Réseaux sociaux: jusqu'à 15 points (3 par réseau)

**Déclenchement**:
- Bouton admin "Analyser le CV"
- Endpoint API: `POST /admin/analyze-cv/<user_id>`

**Stockage**:
Résultats stockés dans le modèle User après analyse

---

#### 2. AIMatchingService - Talents Standards

**Fichier**: `app/services/ai_matching_service.py`

**Méthode Principale**:

```python
@staticmethod
def analyze_job_description(
    job_description: str, 
    user_profiles: List[User], 
    api_key: str = None
) -> dict
```

**Extraction de Profil**:

```python
def _extract_profile_data(user: User) -> dict
```

Extrait:
- Informations de base (code, nom, email)
- Localisation (ville, pays)
- Disponibilité et mode de travail
- Talents déclarés
- Compétences CV (3000 premiers caractères)

**Analyse Individuelle**:

```python
def _analyze_single_candidate(
    job_description: str,
    profile_data: dict,
    user: User,
    api_key: str
) -> dict
```

**Prompt de Matching**:
```
Tu es un expert en recrutement.
Analyse le profil du candidat par rapport à cette description de poste.

DESCRIPTION DU POSTE:
{job_description}

PROFIL DU CANDIDAT:
Nom: {nom}
Code: {code}
Localisation: {ville}, {pays}
Disponibilité: {disponibilite}
Talents: {talents}
Compétences CV: {competences_cv}

Fournis:
1. Score de matching (0-100)
2. Explication détaillée
3. Points forts
4. Points faibles

Format JSON uniquement.
```

**Résultat par Candidat**:
```json
{
    "user": {...},
    "score": 85,
    "explication": "Candidat hautement qualifié avec 5 ans d'expérience...",
    "points_forts": [
        "Maîtrise complète de React et Node.js",
        "Portfolio impressionnant",
        "Disponible immédiatement"
    ],
    "points_faibles": [
        "Localisation éloignée du bureau",
        "Pas d'expérience en TypeScript"
    ]
}
```

**Traitement JSON**:
- Nettoyage des balises markdown (```json)
- Parsing JSON robuste
- Gestion des erreurs de format
- Validation des champs requis

**Endpoint**: `POST /ai-search`

---

#### 3. AIMatchingService - Talents CINEMA

**Méthode Principale**:

```python
@staticmethod
def analyze_cinema_talents(
    job_description: str,
    cinema_talent_profiles: List[CinemaTalent],
    api_key: str = None
) -> dict
```

**Extraction de Profil CINEMA**:

```python
def _extract_cinema_profile_data(talent: CinemaTalent) -> dict
```

Extrait:
- Informations physiques (âge, taille, poids, teint, yeux, cheveux)
- Ethnicités (JSON array)
- Types de talents (Acteur, Figurant, Cascadeur, etc.)
- Langues parlées (JSON array)
- Compétences spéciales (JSON array)
- Expérience (années)
- Bio professionnelle

**Prompt de Casting**:
```
Tu es un directeur de casting professionnel.
Analyse le profil du talent par rapport à cette description de rôle.

DESCRIPTION DU RÔLE:
{job_description}

PROFIL DU TALENT:
Nom: {nom}
Code: {code}
Âge: {age} ans
Genre: {genre}
Taille: {taille} cm
Poids: {poids} kg
Teint: {teint}
Yeux: {couleur_yeux}
Cheveux: {couleur_cheveux} - {type_cheveux}
Ethnicités: {ethnicites}
Types de talents: {types_talents}
Langues: {langues}
Compétences: {competences}
Expérience: {experience} ans
Bio: {bio}

Fournis:
1. Score de matching (0-100)
2. Explication détaillée
3. Points forts (physiques, artistiques)
4. Points faibles

Format JSON uniquement.
```

**Spécificités CINEMA**:
- Analyse des caractéristiques physiques détaillées
- Évaluation de l'adéquation au rôle
- Prise en compte de l'expérience cinématographique
- Vérification des compétences spéciales requises
- Analyse des productions précédentes

**Endpoint**: `POST /cinema/ai-search`

---

#### Endpoints API IA

**1. Recherche IA de Talents Standards**

```
POST /ai-search
Content-Type: multipart/form-data

Paramètres:
- job_description (text) : Description du poste
- job_file (file) : PDF/DOCX/TXT (optionnel)

Réponse:
{
    "success": true,
    "candidates": [...],
    "total_analyzed": 50,
    "total_matched": 12
}
```

**2. Recherche IA CINEMA**

```
POST /cinema/ai-search
Content-Type: multipart/form-data

Paramètres:
- role_description (text) : Description du rôle
- role_file (file) : PDF/DOCX/TXT (optionnel)

Réponse:
{
    "success": true,
    "candidates": [...],
    "total_analyzed": 30,
    "total_matched": 8
}
```

**3. Analyse IA de CV (Admin)**

```
POST /admin/analyze-cv/<user_id>
Authorization: Admin requis

Réponse:
{
    "success": true,
    "message": "CV analysé avec succès",
    "profile_score": 75,
    "analysis": {...}
}
```

---

#### Sécurité et Optimisation IA

**Sécurité**:
- Clés API stockées chiffrées dans la base
- Validation des inputs utilisateur
- Sanitization des prompts
- Rate limiting sur les endpoints IA
- Logs de toutes les requêtes IA
- Pas de stockage des prompts côté OpenRouter

**Optimisation**:
- Limitation CV à 3000 caractères
- Timeout configuré par service (30s ou 60s)
- Max tokens: 1000 (CV Analyzer)
- Tri automatique par score (AI Matching)
- Traitement séquentiel des candidats

**Coûts**:
- Modèle gratuit utilisé
- Pas de limite de requêtes stricte
- Monitoring de l'utilisation
| Cryptographie | Fernet (cryptography) | Latest |
| Hachage Mots de Passe | bcrypt | 4.1.2 |

### Architecture en Couches

```
┌─────────────────────────────────────┐
│     Présentation (Templates)         │
│   Jinja2 + Tailwind CSS + JavaScript │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│       Routes (Blueprints)            │
│  auth, profile, admin, cinema, api   │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│         Services Business            │
│ CV Analyzer, Export, Email, Backup   │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│      Modèles (ORM SQLAlchemy)        │
│   User, Talent, Cinema, Production   │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│     Base de Données PostgreSQL       │
└─────────────────────────────────────┘
```

### Blueprints

L'application utilise 7 blueprints principaux:

1. **main** (`/`) - Pages principales et dashboard
2. **auth** (`/auth`) - Authentification et inscription
3. **profile** (`/profile`) - Gestion du profil utilisateur
4. **admin** (`/admin`) - Administration système
5. **cinema** (`/cinema`) - Module CINEMA pour talents cinématographiques
6. **api** (`/api`) - API ancienne (legacy)
7. **api_v1** (`/api/v1`) - API REST moderne

---

## Modèles de Données

### 1. User (Utilisateur Principal)

**Table**: `users`

**Champs Principaux**:
- `id` (Integer, PK) - Identifiant unique
- `email` (String, unique, indexed) - Email de connexion
- `unique_code` (String, unique, indexed) - Code unique format PPVVVNNNNG
- `password_hash` (String) - Mot de passe haché (bcrypt)
- `first_name`, `last_name` (String) - Nom et prénom
- `date_of_birth` (Date) - Date de naissance
- `gender` (String) - Genre (M/F/N)
- `phone_encrypted`, `whatsapp_encrypted` (Text) - Contacts chiffrés (Fernet)
- `address_encrypted` (Text) - Adresse chiffrée
- `country_id`, `city_id` (ForeignKey) - Localisation
- `availability` (String) - Disponibilité (disponible_maintenant, disponible_prochainement, etc.)
- `work_mode` (String) - Mode de travail (sur_site, à_distance, hybride, etc.)
- `rate_range` (String) - Fourchette de tarifs
- `years_experience` (Integer) - Années d'expérience
- `bio` (Text) - Biographie professionnelle
- `portfolio_url` (String) - URL portfolio
- `website` (String) - Site web personnel
- `linkedin`, `instagram`, `twitter`, `facebook`, `github`, `behance`, `dribbble` (Text, encrypted) - Réseaux sociaux chiffrés
- `imdb_url_encrypted`, `threads_encrypted` (Text) - URLs chiffrées
- `cv_filename` (String) - Nom du fichier CV
- `photo_filename` (String) - Nom du fichier photo
- `qr_code_path` (String) - Chemin vers le QR code
- `profile_score` (Integer) - Score du profil (0-100) calculé par IA
- `is_admin` (Boolean) - Statut administrateur
- `account_active` (Boolean) - Compte actif
- `created_at`, `updated_at` (DateTime) - Horodatage

**Relations**:
- `country` → Country (Many-to-One)
- `city` → City (Many-to-One)
- `talents` → UserTalent (One-to-Many)

### 2. Talent

**Table**: `talents`

**Champs**:
- `id` (Integer, PK)
- `name` (String, unique) - Nom du talent (ex: Développeur Web, Designer, Photographe)
- `category` (String) - Catégorie (Tech, Creative, etc.)

**Relations**:
- `users` → UserTalent (One-to-Many)

### 3. UserTalent (Association)

**Table**: `user_talents`

**Champs**:
- `id` (Integer, PK)
- `user_id` (ForeignKey → users)
- `talent_id` (ForeignKey → talents)

### 4. CinemaTalent (Talents Cinématographiques)

**Table**: `cinema_talents`

**Champs Principaux**:
- `id`, `unique_code` (format PPVVVNNNNNNNG)
- Informations personnelles: `first_name`, `last_name`, `date_of_birth`, `gender`
- Origines: `country_of_origin_id`, `city_of_origin_id`, `ethnicities` (JSON array)
- Résidence: `country_id`, `city_id`
- Caractéristiques physiques:
  - `height` (Integer, cm)
  - `eye_color` (String) - Couleur des yeux
  - `hair_color`, `hair_type` (String) - Cheveux
  - `skin_tone` (String) - Teint
  - `build` (String) - Morphologie
- Compétences:
  - `languages` (JSON array) - Langues parlées
  - `talent_types` (JSON array) - Types de talents (Acteur Principal, Figurant, etc.)
  - `other_talents` (JSON array) - Autres talents
  - `experience_level` (String) - Niveau d'expérience
- Contact (chiffré):
  - `phone_encrypted`, `whatsapp_encrypted`, `email_encrypted`
  - `telegram_encrypted`, `facebook_encrypted`, `instagram_encrypted`, `tiktok_encrypted`
  - `website` (non chiffré)
- Média:
  - `photo_filename`, `qr_code_path`
  - `previous_productions` (JSON) - Productions précédentes
- `id_document_number_encrypted` (Text) - Numéro de document d'identité chiffré

### 5. Production (Boîtes de Production)

**Table**: `productions`

**Champs**:
- Informations de base: `name`, `description`, `specialization`
- Contact: `address`, `city`, `country`, `postal_code`, `phone`, `email`, `website`
- Réseaux sociaux: `facebook`, `instagram`, `linkedin`, `twitter`
- Détails: `founded_year`, `ceo`, `employees_count`, `productions_count`
- Données JSON:
  - `notable_productions` (JSON array)
  - `services` (JSON array)
  - `certifications` (JSON array)
  - `memberships` (JSON array)
  - `awards` (JSON array)
- Équipements: `equipment`, `studios`
- Statut: `is_active`, `is_verified`

### 6. Project (Projets de Production)

**Table**: `projects`

**Champs**:
- `production_name` (String) - Nom de la production
- `production_type` (String) - Type (film, série, publicité, etc.)
- `production_id` (ForeignKey → productions) - Société de production associée
- `origin_country` (String) - Pays d'origine
- `estimated_start_date`, `estimated_end_date` (Date)
- `shooting_locations` (Text) - Lieux de tournage
- `project_status` (String) - Statut (en_preparation, en_tournage, post_production, termine)

**Relations**:
- `production` → Production (Many-to-One)
- `assigned_talents` → ProjectTalent (One-to-Many)

### 7. ProjectTalent (Assignation de Talents aux Projets)

**Table**: `project_talents`

**Champs**:
- `project_id` (ForeignKey → projects)
- `cinema_talent_id` (ForeignKey → cinema_talents)
- `project_code` (String, unique) - Code unique format PRJ-XXX-YYY
- `role_type` (String) - Type de rôle (acteur_principal, figurant, etc.)
- `role_description` (Text) - Description du rôle

### 8. Country & City (Localisation)

**Tables**: `countries`, `cities`

**Champs Country**:
- `id`, `name` (String)
- `code` (String, 2 lettres ISO) - Ex: MA, FR, SN

**Champs City**:
- `id`, `name` (String)
- `code` (String, 3 lettres) - Ex: RAB, CAS, DAK
- `country_id` (ForeignKey)

### 9. AppSettings (Paramètres Application)

**Table**: `app_settings`

**Champs**:
- `id`, `key` (String, unique) - Clé du paramètre
- `value` (Text) - Valeur
- `description` (Text) - Description

**Paramètres stockés**:
- `SENDGRID_API_KEY`, `SENDGRID_FROM_EMAIL`
- `OPENROUTER_API_KEY`
- `OMDB_API_KEY`
- Version de l'application

---

## Services

### 1. CVAnalyzerService (`app/services/cv_analyzer.py`)

**Responsabilité**: Analyse de CV avec IA

**Méthodes**:
- `analyze_cv(cv_path, user_data=None)` - Analyse complète d'un CV
- `_extract_cv_text(cv_path)` - Extraction du texte (PDF, DOCX)
- `_build_analysis_prompt(cv_text, user_data)` - Construction du prompt IA
- `_parse_ai_response(ai_response)` - Parsing de la réponse JSON
- `_calculate_profile_score(analysis)` - Calcul du score (0-100)

**API Utilisée**: OpenRouter AI (google/gemini-2.5-flash)

**Retour**:
```json
{
  "success": true,
  "score": 85,
  "skills": ["Python", "Flask", "React"],
  "summary": "Développeur full-stack expérimenté...",
  "recommendations": ["Ajouter certifications", "..."]
}
```

### 2. ExportService (`app/services/export_service.py`)

**Responsabilité**: Export des données

**Méthodes**:
- `export_to_excel(users)` - Export Excel (.xlsx) avec pandas/openpyxl
- `export_to_csv(users)` - Export CSV
- `export_to_pdf(users)` - Export PDF avec ReportLab
- `export_cinema_talent_card(cinema_talent)` - Carte de talent PDF individuelle

**Formats supportés**: XLSX, CSV, PDF

### 3. EmailService (`app/services/email_service.py`)

**Responsabilité**: Envoi d'emails transactionnels

**Méthodes**:
- `send_confirmation_email(to_email, user_data)` - Email de confirmation d'inscription
- `send_login_credentials(to_email, unique_code, password)` - Envoi des identifiants

**Provider**: SendGrid API

### 4. BackupService (`app/services/backup_service.py`)

**Responsabilité**: Sauvegarde et restauration

**Méthodes**:
- `create_backup()` - Création d'une archive ZIP chiffrée
- `restore_backup(backup_file)` - Restauration depuis archive

**Contenu sauvegardé**:
- Dump PostgreSQL
- Fichiers uploads (photos, CVs, QR codes)

### 5. DatabaseService (`app/services/database_service.py`)

**Responsabilité**: Diagnostics base de données

**Méthodes**:
- `get_database_stats()` - Statistiques complètes
- `test_connection()` - Test de connexion

### 6. UpdateService (`app/services/update_service.py`)

**Responsabilité**: Gestion des mises à jour

**Méthodes**:
- `check_for_updates()` - Vérification des mises à jour Git
- `apply_update()` - Application des mises à jour
- `get_update_history()` - Historique des mises à jour

### 7. MovieService (`app/services/movie_service.py`)

**Responsabilité**: Proxy OMDB API

**Méthodes**:
- `search_movies(query)` - Recherche de films/séries

**API**: OMDB (optionnel)

---

## Routes et Endpoints

### Blueprint: main (`/`)

| Route | Méthode | Auth | Description |
|-------|---------|------|-------------|
| `/` | GET | Oui | Dashboard adaptatif (admin ou utilisateur) |
| `/talents` | GET | Oui | Liste des utilisateurs talents |
| `/about` | GET | Non | Page À propos |

### Blueprint: auth (`/auth`)

| Route | Méthode | Auth | Description |
|-------|---------|------|-------------|
| `/auth/login` | GET/POST | Non | Connexion (email OU code unique) |
| `/auth/logout` | GET | Oui | Déconnexion |
| `/auth/register` | GET/POST | Non | Inscription multi-étapes |

### Blueprint: profile (`/profile`)

| Route | Méthode | Auth | Description |
|-------|---------|------|-------------|
| `/profile/dashboard` | GET | Oui | Dashboard personnel |
| `/profile/edit` | GET/POST | Oui | Édition du profil |
| `/profile/view/<code>` | GET | Oui | Visualisation publique d'un profil |
| `/profile/upload-cv` | POST | Oui | Upload et analyse IA du CV |
| `/profile/upload-photo` | POST | Oui | Upload photo de profil |

### Blueprint: admin (`/admin`)

| Route | Méthode | Auth | Description |
|-------|---------|------|-------------|
| `/admin/users` | GET | Admin | Liste des utilisateurs |
| `/admin/user/<id>/toggle-active` | POST | Admin | Activer/désactiver compte |
| `/admin/user/<id>/delete` | POST | Admin | Supprimer utilisateur |
| `/admin/user/<id>/edit` | GET/POST | Admin | Éditer utilisateur |
| `/admin/user/<id>/analyze-cv` | POST | Admin | Lancer analyse IA du CV |
| `/admin/talent/create` | GET/POST | Admin | Créer nouveau talent |
| `/admin/export/excel` | GET | Admin | Export Excel |
| `/admin/export/csv` | GET | Admin | Export CSV |
| `/admin/export/pdf` | GET | Admin | Export PDF |
| `/admin/settings` | GET/POST | Admin | Paramètres système |
| `/admin/update` | GET/POST | Admin | Mise à jour application |
| `/admin/backup/create` | POST | Admin | Créer sauvegarde |
| `/admin/backup/restore` | POST | Admin | Restaurer sauvegarde |

### Blueprint: cinema (`/cinema`)

| Route | Méthode | Auth | Description |
|-------|---------|------|-------------|
| `/cinema/dashboard` | GET | Oui | Dashboard CINEMA |
| `/cinema/register` | GET/POST | Non | Inscription publique CINEMA |
| `/cinema/talents` | GET | Oui | Liste talents CINEMA |
| `/cinema/profile/<code>` | GET | Non | Profil public CINEMA |
| `/cinema/profile/<code>/pdf` | GET | Non | Carte talent PDF |
| `/cinema/productions` | GET | Oui | Liste productions |
| `/cinema/productions/new` | GET/POST | Admin | Créer production |
| `/cinema/productions/<id>` | GET | Oui | Détails production |
| `/cinema/productions/<id>/edit` | GET/POST | Admin | Éditer production |
| `/cinema/productions/<id>/delete` | POST | Admin | Supprimer production |
| `/cinema/projects` | GET | Oui | Liste projets |
| `/cinema/projects/new` | GET/POST | Admin | Créer projet |
| `/cinema/projects/<id>` | GET | Oui | Détails projet + gestion talents |
| `/cinema/projects/<id>/edit` | GET/POST | Admin | Éditer projet |
| `/cinema/projects/<id>/delete` | POST | Admin | Supprimer projet |
| `/cinema/projects/<id>/assign-talent` | POST | Admin | Assigner talent au projet |
| `/cinema/projects/<id>/remove-talent/<pt_id>` | POST | Admin | Retirer talent du projet |
| `/cinema/projects/talent/<pt_id>/generate-badge` | GET | Admin | Générer badge PDF |
| `/cinema/stats` | GET | Oui | Statistiques CINEMA |

### API v1 (`/api/v1`)

Voir [API_DOCUMENTATION_EN.md](../api_docs/API_DOCUMENTATION_EN.md) et [API_DOCUMENTATION_FR.md](../api_docs/API_DOCUMENTATION_FR.md) pour la documentation complète.

**Principales catégories**:
- `/api/v1/auth/*` - Authentification
- `/api/v1/users/*` - Gestion utilisateurs
- `/api/v1/talents/*` - Talents
- `/api/v1/cinema/*` - Module CINEMA
- `/api/v1/stats/*` - Statistiques
- `/api/v1/exports/*` - Exports de données

---

## Sécurité

### 1. Authentification

- **Système**: Flask-Login avec session cookies
- **Hachage**: bcrypt (rounds=12)
- **Login dual**: Email OU code unique

### 2. Chiffrement des Données Sensibles

**Algorithme**: Fernet (AES 128-bit en mode CBC)

**Données chiffrées**:
- Numéros de téléphone (`phone_encrypted`, `whatsapp_encrypted`)
- Adresses (`address_encrypted`)
- Réseaux sociaux (tous les champs sociaux)
- Numéros de documents d'identité (CINEMA)

**Clé**: Variable d'environnement `ENCRYPTION_KEY`

**Exemple d'utilisation**:
```python
from app.utils.encryption import encrypt_data, decrypt_data

# Chiffrement
encrypted_phone = encrypt_data("+212600000000")

# Déchiffrement
phone = decrypt_data(encrypted_phone)
```

### 3. Protection CSRF

- **Flask-WTF**: Protection CSRF activée globalement
- **Exception**: API v1 exemptée (`@csrf.exempt`)

### 4. Contrôle d'Accès

**Décorateurs**:
```python
@login_required  # Utilisateur authentifié
@admin_required  # Utilisateur administrateur
```

**Middleware**: Vérification des rôles avant chaque action sensible

### 5. Upload de Fichiers

**Restrictions**:
- Photos: PNG, JPG, JPEG (max 5 MB)
- CVs: PDF, DOC, DOCX (max 10 MB)
- Validation MIME type avec `python-magic`
- Noms de fichiers UUID pour éviter collisions

### 6. Validation des Données

- **Email**: `email-validator`
- **Formulaires**: Flask-WTF
- **Sanitization**: Échappement automatique Jinja2

---

## Installation et Configuration

### Prérequis

- Python 3.11+
- PostgreSQL 14+ (ou SQLite pour développement)
- Git

### Installation

```bash
# 1. Cloner le repository
git clone <repository-url>
cd talentsmaroc

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs
```

### Variables d'Environnement

**Obligatoires**:
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/talentsmaroc
ENCRYPTION_KEY=your-32-byte-base64-encoded-key
```

**Optionnelles**:
```bash
SENDGRID_API_KEY=SG.xxxxx
SENDGRID_FROM_EMAIL=noreply@talentsmaroc.com
OPENROUTER_API_KEY=sk-or-xxxxx
OMDB_API_KEY=xxxxx
REPLIT_DEV_DOMAIN=https://your-replit-domain.repl.co
ADMIN_PASSWORD=@4dm1n
```

### Initialisation de la Base de Données

```bash
# Créer les tables et données de démonstration
python migrations_init.py

# Ou utiliser Flask-Migrate pour des migrations personnalisées
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Lancement

```bash
# Développement
python app.py

# Production (avec Gunicorn)
gunicorn --bind 0.0.0.0:5004 --reuse-port --workers 4 app:app
```

### Comptes par Défaut

**Administrateur**:
- Email: `admin@talento.com`
- Code: `MAN0001RAB`
- Mot de passe: `@4dm1n`

**Démonstration** (5 comptes):
- Emails: `demo1@talento.com` à `demo5@talento.com`
- Mot de passe: `demo123`

**CINEMA Démo** (3 comptes):
- Emails: Se terminent par `@demo.cinema`

---

## Système de Codification

### Format Standard (Profils Principaux)

**Structure**: `PPGNNNNVVV` (10 caractères)

| Composant | Description | Exemple |
|-----------|-------------|---------|
| **PP** | Code pays ISO-2 | `MA` (Maroc) |
| **G** | Genre | `M`, `F`, ou `N` |
| **NNNN** | 4 chiffres **séquentiels par pays** | `0001` |
| **VVV** | 3 premières lettres de la ville | `RAB` (Rabat) |

**Exemple**: `MAM0001RAB` (Maroc, Masculin, 1ère personne au Maroc, Rabat)

**Important**: Le numéro est **séquentiel et incrémenté par pays**, pas par ville:
- `MAM0001RAB` = 1ère personne au Maroc (de Rabat), genre masculin
- `MAF0002CAS` = 2ème personne au Maroc (de Casablanca), genre féminin
- `SNM0001DAK` = 1ère personne au Sénégal (de Dakar), genre masculin

### Format CINEMA (Talents Cinématographiques)

**Structure**: `PPVVVNNNNNG` (11 caractères)

| Composant | Description | Exemple |
|-----------|-------------|---------|
| **PP** | Code pays ISO-2 | `MA` (Maroc) |
| **VVV** | 3 premières lettres de la ville | `CAS` (Casablanca) |
| **NNNN** | 4 chiffres **séquentiels par pays** | `0001` |
| **G** | Genre | `M`, `F` |

**Exemple**: `MACAS0001F` (Maroc, Casablanca, 1ère personne CINEMA au Maroc, Femme)

**Important**: Le numéro est **séquentiel par pays**, identique au système standard:
- `MACAS0001F` = 1ère personne CINEMA au Maroc (de Casablanca)
- `MARAB0002M` = 2ème personne CINEMA au Maroc (de Rabat)
- `SNDAG0001F` = 1ère personne CINEMA au Sénégal (de Dakar)

**Distinction**: Les codes CINEMA se distinguent des codes standards par l'ordre des composants:
- **Standard**: Pays-Genre-Numéro-Ville (PPGNNNNVVV)
- **CINEMA**: Pays-Ville-Numéro-Genre (PPVVVNNNNNG)

**Rétrocompatibilité**: Le système supporte encore les anciens codes CINEMA à 6 chiffres (13 caractères total).

### Format Projets

**Structure**: `CCIIISSSNNN` (10+ caractères, sans tirets)

| Composant | Description | Exemple |
|-----------|-------------|---------|
| **CC** | Code pays (2 lettres) | `MA` |
| **III** | Initiales de production (2-3 lettres) | `ABC` |
| **SSS** | ID du projet (3 chiffres) | `001` |
| **NNN** | Numéro séquentiel de talent (3 chiffres) | `042` |

**Exemple**: `MAABC001042` (Maroc, ABC Productions, Projet 1, 42ème talent assigné)

**Note**: Aucun tiret n'est utilisé dans les codes projets.

### Génération des Codes

**Utilities**:
- `app/utils/id_generator.py` - Codes utilisateurs standard (PPGNNNNVVV)
- `app/utils/cinema_code_generator.py` - Codes CINEMA (PPVVVNNNNNG)
- `app/utils/project_code_generator.py` - Codes projets (CCIIISSSNNN)

---

## API REST v1

### Authentification

**Type**: Session-based (cookies)

**Login**:
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "identifier": "admin@talento.com",
  "password": "@4dm1n"
}
```

**Réponse**:
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "admin@talento.com",
    "unique_code": "MAN0001RAB",
    "is_admin": true
  }
}
```

### Endpoints Principaux

**Utilisateurs**:
- `GET /api/v1/users` - Liste (admin uniquement)
- `GET /api/v1/users/<id>` - Détails
- `PUT /api/v1/users/<id>` - Mise à jour (admin)
- `DELETE /api/v1/users/<id>` - Suppression (admin)

**CINEMA**:
- `GET /api/v1/cinema/talents` - Liste talents CINEMA
- `GET /api/v1/cinema/talents/<id>` - Détails talent
- `GET /api/v1/cinema/productions` - Liste productions
- `GET /api/v1/cinema/projects` - Liste projets

**Statistiques**:
- `GET /api/v1/stats/overview` - Vue d'ensemble
- `GET /api/v1/stats/users` - Stats utilisateurs
- `GET /api/v1/stats/cinema` - Stats CINEMA

**Exports**:
- `GET /api/v1/exports/users/excel` - Export Excel
- `GET /api/v1/exports/users/csv` - Export CSV
- `GET /api/v1/exports/cinema/excel` - Export CINEMA Excel

### Documentation Complète

Consultez:
- [API Documentation EN](../api_docs/API_DOCUMENTATION_EN.md)
- [API Documentation FR](../api_docs/API_DOCUMENTATION_FR.md)

---

## Migrations et Mises à Jour

### Auto-Migration

Le système utilise `app/utils/auto_migrate.py` pour:
1. Détecter les changements de schéma
2. Créer automatiquement les colonnes manquantes
3. Garantir la cohérence des données

**Exécution**: Automatique au démarrage de l'application

### Historique des Versions

Stocké dans:
- `logs/update_history.json` - Historique JSON
- `CHANGELOG.md` - Changelog détaillé

**Versions majeures**:
- v1.0.0 - Version initiale
- v2.0.0 - Introduction module CINEMA
- v2.16.0 - Ajout champs website, IMDb, Threads
- v2.17.0 - Module Productions
- v2.18.0 - Module Projets

---

## Structure des Fichiers

```
talentsmaroc/
├── app/
│   ├── __init__.py                 # Factory Flask
│   ├── constants.py                # Constantes globales
│   ├── models/                     # Modèles SQLAlchemy
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── talent.py
│   │   ├── cinema_talent.py
│   │   ├── production.py
│   │   ├── project.py
│   │   ├── location.py
│   │   └── settings.py
│   ├── routes/                     # Blueprints/Routes
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── profile.py
│   │   ├── admin.py
│   │   ├── cinema.py
│   │   ├── api.py
│   │   └── api_v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── talents.py
│   │       ├── cinema.py
│   │       ├── stats.py
│   │       └── exports.py
│   ├── services/                   # Logique métier
│   │   ├── __init__.py
│   │   ├── cv_analyzer.py
│   │   ├── email_service.py
│   │   ├── export_service.py
│   │   ├── backup_service.py
│   │   ├── database_service.py
│   │   ├── update_service.py
│   │   └── movie_service.py
│   ├── templates/                  # Templates Jinja2
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   ├── profile/
│   │   ├── admin/
│   │   └── cinema/
│   ├── static/                     # Fichiers statiques
│   │   ├── css/
│   │   ├── js/
│   │   ├── img/
│   │   └── uploads/
│   │       ├── photos/
│   │       ├── cvs/
│   │       └── qrcodes/
│   └── utils/                      # Utilitaires
│       ├── __init__.py
│       ├── encryption.py
│       ├── id_generator.py
│       ├── cinema_code_generator.py
│       ├── project_code_generator.py
│       ├── qr_generator.py
│       ├── file_handler.py
│       ├── email_service.py
│       └── auto_migrate.py
├── migrations_archive/             # Anciennes migrations
├── api_docs/                       # Documentation API
│   ├── API_DOCUMENTATION_EN.md
│   └── API_DOCUMENTATION_FR.md
├── docs/                           # Documentation technique
│   └── TECHNICAL_DOCUMENTATION.md
├── logs/                           # Logs application
│   └── update_history.json
├── app.py                          # Point d'entrée
├── config.py                       # Configuration
├── migrations_init.py              # Initialisation DB
├── requirements.txt                # Dépendances Python
├── README.md                       # Documentation utilisateur
├── README.fr.md                    # Documentation FR
├── CHANGELOG.md                    # Journal des modifications
└── .env                            # Variables d'environnement
```

---

## Tests et Qualité

### Tests Manuels Recommandés

1. **Authentification**:
   - Connexion avec email
   - Connexion avec code unique
   - Logout
   - Gestion des sessions

2. **Profils**:
   - Création compte utilisateur
   - Création talent CINEMA
   - Upload CV avec analyse IA
   - Upload photo
   - Édition des informations

3. **Administration**:
   - Gestion utilisateurs
   - Exports (Excel, CSV, PDF)
   - Paramètres système
   - Sauvegardes/restaurations

4. **CINEMA**:
   - Inscription publique
   - Liste et recherche talents
   - Gestion productions
   - Gestion projets
   - Assignation talents

5. **API**:
   - Authentification API
   - Endpoints principaux
   - Gestion d'erreurs

### Logs

**Emplacement**: `logs/`

**Fichiers**:
- `update_history.json` - Historique des mises à jour
- Logs applicatifs (à configurer)

---

## Support et Contribution

### Problèmes Connus

1. **Tailwind CDN**: Message d'avertissement (non bloquant) sur l'utilisation du CDN en production
2. **Python-magic**: Nécessite `libmagic` système (installé automatiquement sur Linux)

### Améliorations Futures

- Migration Tailwind vers build local (PostCSS)
- Tests automatisés (pytest)
- CI/CD Pipeline
- Containerisation Docker
- Internationalisation (i18n)
- Cache Redis pour performances
- WebSockets pour notifications temps réel

### Contact

Pour questions techniques ou contributions:
- Email: moa@myoneart.com
- Organisation: MOA Digital Agency LLC

---

**© 2024 taalentio.com. Tous droits réservés.**
