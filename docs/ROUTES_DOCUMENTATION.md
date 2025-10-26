# Documentation Complète des Routes et Endpoints
## TalentsMaroc.com

**Dernière mise à jour**: 26 Octobre 2025

---

## Table des Matières

1. [Routes Principales (`main.py`)](#1-routes-principales)
2. [Authentification (`auth.py`)](#2-authentification)
3. [Profil Utilisateur (`profile.py`)](#3-profil-utilisateur)
4. [Administration (`admin.py`)](#4-administration)
5. [Module CINEMA (`cinema.py`)](#5-module-cinema)
6. [Présence/Pointage (`presence.py`)](#6-présencepointage)
7. [API Legacy (`api.py`)](#7-api-legacy)
8. [API REST v1 (`api_v1/`)](#8-api-rest-v1)

---

## 1. Routes Principales

**Blueprint**: `main` (Préfixe: `/`)

### `GET /`
**Description**: Page d'accueil - Redirige vers le tableau de bord approprié selon le rôle
**Authentification**: Requise (`@login_required`)
**Comportement**:
- Si admin → Dashboard admin avec statistiques et filtres
- Si utilisateur normal → Dashboard utilisateur personnel

**Dashboard Admin** affiche:
- Statistiques globales (utilisateurs, talents, etc.)
- Filtres avancés de recherche
- Graphiques et métriques
- Accès rapide aux fonctionnalités

**Filtres disponibles**:
- `search` (query string) - Recherche par nom/email/code
- `search_code` - Recherche par code unique
- `talent` (liste) - Filtrer par talents
- `country` - Filtrer par pays
- `city` - Filtrer par ville
- `gender` - Filtrer par genre (M/F/N)
- `availability` - Filtrer par disponibilité
- `work_mode` - Filtrer par mode de travail
- `has_cv` - A un CV uploadé
- `has_portfolio` - A un URL portfolio
- `date_from` / `date_to` - Période de création

---

### `GET /about`
**Description**: Page "À propos" avec informations sur la plateforme
**Authentification**: Requise
**Template**: `about.html`

---

### `GET /contrats`
**Description**: Page de gestion des contrats (en développement)
**Authentification**: Requise
**Template**: `contrats.html`
**Statut**: 🚧 En cours de développement

---

### `GET /talents`
**Description**: Catalogue public des talents avec système de filtrage avancé
**Authentification**: Requise
**Template**: `talents.html`

**Fonctionnalités**:
- Affichage sous forme de cartes (grid)
- Filtrage par catégorie de talent
- Recherche par nom/compétences
- Pagination
- Vue détaillée avec modal

---

## 2. Authentification

**Blueprint**: `auth` (Préfixe: `/auth`)

### `GET/POST /auth/login`
**Description**: Page de connexion
**Méthodes**: GET (affichage), POST (traitement)
**Template**: `auth/login.html`

**POST Data**:
- `email` (ou `unique_code`) - Identifiant
- `password` - Mot de passe

**Comportement**:
- Accepte connexion par email OU code unique
- Hash du mot de passe vérifié avec bcrypt
- Session créée avec Flask-Login
- Redirection vers dashboard approprié
- Support du paramètre `?next=` pour retour après login

---

### `GET /auth/logout`
**Description**: Déconnexion de l'utilisateur
**Authentification**: Requise
**Redirection**: Vers `/auth/login`

---

### `GET/POST /auth/register`
**Description**: Inscription d'un nouvel utilisateur
**Template**: `auth/register.html`

**POST Data** (informations personnelles):
- `first_name`, `last_name` - Nom complet
- `email` - Email unique
- `password`, `confirm_password` - Mots de passe
- `date_of_birth` - Date de naissance
- `gender` - Genre (M/F/N)
- `phone`, `whatsapp` - Numéros (seront chiffrés)
- `country_id`, `city_id` - Localisation
- `talents[]` - Liste des talents sélectionnés
- `bio` - Biographie professionnelle
- `years_experience` - Années d'expérience
- `availability`, `work_mode`, `rate_range` - Info professionnelle

**Processus**:
1. Validation des données
2. Génération du code unique (format PPGNNNNVVV)
3. Chiffrement des données sensibles (phone, whatsapp, réseaux sociaux)
4. Hash du mot de passe (bcrypt)
5. Création du compte
6. Génération du QR code
7. Envoi email de bienvenue (si configuré)
8. Connexion automatique

---

## 3. Profil Utilisateur

**Blueprint**: `profile` (Préfixe: `/profile`)

### `GET /profile/`
**Description**: Redirection vers la page de profil
**Redirection**: Vers `/profile/view/<unique_code>`

---

### `GET /profile/dashboard`
**Description**: Tableau de bord personnel de l'utilisateur
**Authentification**: Requise
**Template**: `profile/dashboard.html`

**Affiche**:
- Informations du profil
- Score de complétude
- Statistiques personnelles
- Actions rapides

---

### `GET /profile/view/<unique_code>`
**Description**: Vue publique du profil utilisateur
**Paramètres**: `unique_code` - Code unique de l'utilisateur
**Template**: `profile/view.html`

**Fonctionnalités**:
- Affichage de toutes les informations publiques
- QR code du profil
- Talents et compétences
- Coordonnées (déchiffrées à la volée)
- Analyse CV si disponible
- Détection automatique si l'utilisateur est aussi un talent CINEMA

---

### `GET/POST /profile/edit`
**Description**: Édition du profil utilisateur
**Authentification**: Requise
**Template**: `profile/edit.html`

**Champs MODIFIABLES** (sécurité):
- Contact: `phone`, `whatsapp`, `address`
- Localisation: `country_id`, `city_id`
- Professionnel: `availability`, `work_mode`, `rate_range`, `years_experience`, `bio`
- Portfolio: `portfolio_url`, `website`
- Réseaux sociaux: LinkedIn, Instagram, Twitter, Facebook, GitHub, Behance, Dribbble, IMDb, Threads
- Talents: Ajout/suppression de talents

**Champs VERROUILLÉS** (non modifiables pour sécurité):
- Identité: `first_name`, `last_name`, `email`
- Informations sensibles: `date_of_birth`, `gender`
- Documents: `passport_number`, `residence_card`
- Système: `unique_code`, `is_admin`

**Upload de fichiers**:
- Photo de profil (PNG, JPG, JPEG - max 5MB)
- CV (PDF, DOC, DOCX - max 10MB)

**Processus**:
1. Validation des données
2. Chiffrement des données sensibles modifiées
3. Traitement des uploads (UUID pour noms de fichiers)
4. Validation MIME des fichiers
5. Mise à jour en base de données
6. Recalcul du score de profil

---

## 4. Administration

**Blueprint**: `admin` (Préfixe: `/admin`)  
**Authentification**: Requise + Vérification admin (`@admin_required`)

### Gestion des Utilisateurs

#### `GET /admin/users`
**Description**: Liste complète de tous les utilisateurs (non-admins)
**Template**: `admin/users.html`
**Tri**: Par date de création (desc)

---

#### `POST /admin/user/<int:user_id>/toggle-active`
**Description**: Active/Désactive un compte utilisateur
**Paramètres**: `user_id` - ID de l'utilisateur
**Redirection**: Vers la page précédente ou `/`

---

#### `POST /admin/user/<int:user_id>/delete`
**Description**: Supprime un utilisateur
**Paramètres**: `user_id`
**Sécurité**: Impossible de supprimer un compte admin
**Redirection**: Vers la page précédente

---

#### `GET/POST /admin/user/<int:user_id>/edit`
**Description**: Édition complète d'un profil utilisateur
**Template**: `admin/user_edit.html`
**Permissions**: Toutes modifications possibles (y compris champs verrouillés pour utilisateurs)

---

#### `POST /admin/user/<int:user_id>/promote-admin`
**Description**: Promouvoir un utilisateur en administrateur
**Action**: Définit `is_admin=True`

---

#### `POST /admin/user/<int:user_id>/demote-admin`
**Description**: Rétrograder un admin en utilisateur normal
**Action**: Définit `is_admin=False`

---

### Exports de Données

#### `GET /admin/export/excel`
**Description**: Export de tous les utilisateurs en Excel (.xlsx)
**Format**: Multi-feuilles avec formatage professionnel
**Contenu**:
- Informations personnelles
- Contact (déchiffré)
- Talents associés
- Statistiques

---

#### `GET /admin/export/csv`
**Description**: Export CSV des utilisateurs
**Encodage**: UTF-8 avec BOM
**Délimiteur**: Virgule

---

#### `GET /admin/export/pdf`
**Description**: Export PDF formaté des utilisateurs
**Librairie**: ReportLab
**Contenu**: Cartes talents professionnelles

---

### Gestion des Talents

#### `GET /admin/talents`
**Description**: Liste de toutes les catégories de talents
**Template**: `admin/talents_list.html`

---

#### `POST /admin/talent/new`
**Description**: Création d'une nouvelle catégorie de talent
**POST Data**:
- `name` - Nom du talent
- `emoji` - Emoji représentatif
- `category` - Catégorie

---

#### `POST /admin/talent/<int:talent_id>/delete`
**Description**: Suppression d'une catégorie de talent
**Attention**: Supprime aussi les associations UserTalent

---

### Paramètres Système

#### `GET /admin/settings`
**Description**: Page principale des paramètres
**Template**: `admin/settings.html`
**Sections**:
- Clés API (SendGrid, OpenRouter, TMDb)
- Configuration email
- Informations base de données
- Système de mises à jour

---

#### `GET /admin/settings/api-keys`
**Description**: Gestion des clés API
**Template**: `admin/settings/api_keys.html`

---

#### `GET /admin/settings/email-templates`
**Description**: Gestion des templates d'emails
**Template**: `admin/settings/email_templates.html`

---

#### `GET /admin/settings/backups`
**Description**: Gestion des sauvegardes
**Template**: `admin/settings/backups.html`

---

#### `POST /admin/save-settings`
**Description**: Sauvegarde des paramètres
**POST Data**: Paramètres variés selon la section

---

#### `POST /admin/test-email`
**Description**: Test d'envoi d'email via SendGrid
**POST Data**:
- `test_email` - Email de destination

---

### Sauvegardes

#### `POST /admin/backup/create`
**Description**: Création d'une sauvegarde complète
**Contenu**:
- Dump PostgreSQL/SQLite
- Tous les fichiers uploads
- Configuration (sans secrets)
**Format**: Archive .tar.gz chiffrée
**Stockage**: `/backups/`

---

#### `POST /admin/backup/restore`
**Description**: Restauration depuis une sauvegarde
**Upload**: Fichier .tar.gz
**Avertissement**: Écrase les données existantes

---

### Actions en Masse

#### `POST /admin/bulk/export`
**Description**: Export groupé d'utilisateurs sélectionnés
**POST Data**: `user_ids[]` - Liste d'IDs

---

#### `POST /admin/bulk/delete`
**Description**: Suppression groupée d'utilisateurs
**POST Data**: `user_ids[]`
**Sécurité**: Confirmation requise

---

### Système de Mises à Jour

#### `GET /admin/check-updates`
**Description**: Vérification des mises à jour disponibles (via Git)
**Response**: JSON avec informations de version

---

#### `POST /admin/perform-update`
**Description**: Application d'une mise à jour
**Actions**:
1. `git pull`
2. Installation des nouvelles dépendances
3. Migrations de base de données
4. Redémarrage de l'application

---

#### `POST /admin/git/pull`
**Description**: Pull manuel depuis Git
**Authentification**: Admin requis

---

#### `GET /admin/git/status`
**Description**: Statut Git du projet
**Response**: JSON avec état du repository

---

## 5. Module CINEMA

**Blueprint**: `cinema` (Préfixe: `/cinema`)  
**Authentification**: Requise

### Dashboard CINEMA

#### `GET /cinema/` ou `/cinema/dashboard`
**Description**: Dashboard principal du module CINEMA
**Template**: `cinema/dashboard.html`

**Statistiques affichées**:
- Nombre total de productions actives
- Nombre total de talents CINEMA
- Nombre total de projets
- Nombre de membres de l'équipe (admins + rôle presence)

---

### Gestion des Talents CINEMA

#### `GET /cinema/talents`
**Description**: Liste tous les talents CINEMA avec filtres avancés
**Template**: `cinema/talents.html`

**Filtres disponibles** (12 critères):
- Nom
- Type de talent (13 types)
- Genre (M/F)
- Tranche d'âge (18-25, 26-35, 36-50, 51+)
- Ethnicité
- Couleur des yeux
- Couleur des cheveux
- Teint de peau
- Taille (plage)
- Pays de résidence
- Langues parlées
- Niveau d'expérience

---

#### `GET/POST /cinema/register`
**Description**: Formulaire d'inscription publique pour talents CINEMA
**Template**: `cinema/register_talent.html`
**Accès**: PUBLIC (pas d'authentification requise)

**Sections du formulaire** (9 parties):

1. **Informations Personnelles**:
   - `first_name`, `last_name`
   - `gender` (M/F)
   - `date_of_birth`

2. **Document d'Identité**:
   - `id_document_type` (Passeport, CNI, etc.)
   - `id_document_number` (chiffré)

3. **Origines**:
   - `country_of_origin`, `nationality`
   - `ethnicities[]` (choix multiples)

4. **Résidence**:
   - `country_of_residence`, `city_of_residence`

5. **Langues & Expérience**:
   - `languages_spoken[]` (choix multiples avec drapeaux)
   - `years_of_experience`

6. **Types de Talents Cinématographiques** (13 types):
   - Acteur Principal
   - Acteur Secondaire
   - Figurant
   - Silhouette
   - Doublure
   - Doublure Lumière
   - Cascadeur
   - Mannequin
   - Voix Off
   - Figurant Spécialisé
   - Choriste
   - Danseur de fond
   - Autre

7. **Caractéristiques Physiques**:
   - `eye_color` (19 couleurs)
   - `hair_color` (16 couleurs)
   - `hair_type` (10 types)
   - `height` (cm)
   - `skin_tone` (11 teintes)
   - `build` (6 morphologies)

8. **Autres Talents** (30+ compétences):
   - Chant, Danse, Instruments de musique
   - Arts martiaux, Sports, Acrobatie
   - Conduite spéciale, Équitation
   - Langues des signes, Imitations
   - Compétences techniques, etc.

9. **Contact & Médias**:
   - `email` (unique, non chiffré)
   - `phone`, `whatsapp` (chiffrés)
   - `website`
   - Réseaux sociaux (tous chiffrés): Facebook, Instagram, TikTok, Telegram, LinkedIn, YouTube, Snapchat, Twitter, IMDb, Threads
   - Photos: Profil, ID, Galerie (optionnel)
   - `previous_productions` - Historique de productions

**Processus d'inscription**:
1. Validation complète des données
2. Génération du code unique CINEMA (format PPVVVNNNNNG)
3. Chiffrement des données sensibles (Fernet AES-128)
4. Upload et validation des photos
5. Génération du QR code
6. Sauvegarde en base de données
7. Email de confirmation (si configuré)

---

#### `GET /cinema/profile/<unique_code>`
**Description**: Vue publique d'un profil talent CINEMA
**Paramètres**: `unique_code` - Code CINEMA
**Template**: `cinema/profile_view.html`
**Accès**: PUBLIC

**Affichage**:
- Informations personnelles
- Photo de profil
- QR code
- Caractéristiques physiques
- Compétences et talents
- Coordonnées (déchiffrées)
- Historique de productions

---

#### `GET /cinema/export/pdf/<code>`
**Description**: Export PDF professionnel du profil talent
**Paramètres**: `code` - Code unique CINEMA
**Format**: PDF avec logo, QR code, toutes les informations
**Librairie**: ReportLab

---

### Gestion des Productions

#### `GET /cinema/productions`
**Description**: Liste des boîtes de production
**Template**: `cinema/productions.html`
**Tri**: Par date de création (desc)

---

#### `GET/POST /cinema/productions/new`
**Description**: Création d'une nouvelle boîte de production
**Template**: `cinema/production_form.html`

**POST Data** (informations complètes):
- Identité: `name`, `description`, `specialization`, `logo_url`
- Coordonnées: `address`, `city`, `country`, `postal_code`
- Contact: `phone`, `email`, `website`
- Réseaux sociaux: `facebook`, `instagram`, `linkedin`, `twitter`
- Détails: `founded_year`, `ceo`, `employees_count`, `productions_count`
- Données JSON:
  - `notable_productions[]` - Productions notables
  - `services[]` - Services offerts
  - `certifications[]` - Certifications
  - `memberships[]` - Affiliations
  - `awards[]` - Prix et distinctions
- Infrastructure: `equipment`, `studios`
- Statut: `is_verified`

---

#### `GET /cinema/productions/<int:id>`
**Description**: Détails d'une boîte de production
**Template**: `cinema/production_detail.html`

---

#### `GET/POST /cinema/productions/<int:id>/edit`
**Description**: Édition d'une boîte de production
**Template**: `cinema/production_form.html`

---

#### `POST /cinema/productions/<int:id>/delete`
**Description**: Suppression d'une boîte de production
**Cascade**: Supprime aussi les projets associés

---

### Gestion des Projets

#### `GET /cinema/projects`
**Description**: Liste de tous les projets
**Template**: `cinema/projects.html`
**Filtres**: Par production, statut, dates

---

#### `GET/POST /cinema/projects/new`
**Description**: Création d'un nouveau projet
**Template**: `cinema/project_form.html`

**POST Data**:
- `name` - Nom du projet/film
- `production_type` - Type (Film, Série, Publicité, Documentaire, Court-métrage, Clip musical, Émission TV)
- `production_company_id` - Boîte de production associée
- `origin_country` - Pays d'origine
- `shooting_locations` - Lieux de tournage
- `start_date`, `end_date` - Dates
- `status` - Statut (En préparation, En tournage, Post-production, Terminé)

---

#### `GET /cinema/projects/<int:id>`
**Description**: Détails d'un projet
**Template**: `cinema/project_detail.html`

**Affichage**:
- Informations du projet
- Boîte de production
- Liste des talents assignés
- Actions: Assigner talents, générer badges

---

#### `GET/POST /cinema/projects/<int:id>/edit`
**Description**: Édition d'un projet
**Template**: `cinema/project_form.html`

---

#### `POST /cinema/projects/<int:id>/delete`
**Description**: Suppression d'un projet
**Cascade**: Supprime les assignations de talents

---

### Assignation de Talents aux Projets

#### `POST /cinema/projects/<int:id>/assign-talent`
**Description**: Assigner un talent CINEMA à un projet
**POST Data**:
- `cinema_talent_id` - ID du talent
- `talent_type` - Type de rôle
- `role_description` - Description du rôle

**Processus**:
1. Génération du code projet unique (format PRJXXXYYY)
2. Création de l'assignation ProjectTalent
3. Email de notification (si configuré)

---

#### `POST /cinema/projects/<int:id>/remove-talent/<int:pt_id>`
**Description**: Retirer un talent d'un projet
**Paramètres**:
- `id` - ID du projet
- `pt_id` - ID de l'assignation ProjectTalent

---

#### `GET /cinema/projects/talent/<int:pt_id>/generate-badge`
**Description**: Génération d'un badge PDF pour un talent assigné
**Paramètres**: `pt_id` - ID ProjectTalent
**Format**: PDF personnalisé avec QR code, photo, infos projet
**Librairie**: ReportLab

**Contenu du badge**:
- Photo du talent
- Nom complet
- Code projet unique
- Nom du projet
- Rôle/Type de talent
- QR code du profil
- Logo de la production

---

#### `GET /cinema/projects/<int:id>/print-talents-list`
**Description**: Liste imprimable des talents d'un projet
**Format**: PDF formaté
**Contenu**: Tableau avec tous les talents assignés, leurs rôles, contacts

---

### Gestion de l'Équipe CINEMA

#### `GET /cinema/team`
**Description**: Liste des membres de l'équipe CINEMA
**Template**: `cinema/team.html`
**Membres**: Admins + utilisateurs avec rôle "presence"

---

#### `POST /cinema/team/add`
**Description**: Ajouter un membre à l'équipe
**POST Data**: `user_id`
**Action**: Définit `role='presence'`

---

#### `POST /cinema/team/<int:member_id>/edit`
**Description**: Modifier le rôle d'un membre

---

### API CINEMA (internes)

#### `GET /cinema/api/search_movies`
**Description**: Recherche de films via OMDB API (proxy)
**Paramètres**: `q` - Terme de recherche
**Response**: JSON avec résultats de films
**Utilisation**: Autocomplete dans les formulaires

---

#### `GET /cinema/api/cities/<country_code>`
**Description**: Récupérer les villes d'un pays
**Paramètres**: `country_code` - Code ISO-2 du pays
**Response**: JSON avec liste des villes
**Utilisation**: Chargement dynamique des villes

---

## 6. Présence/Pointage

**Blueprint**: `presence` (Préfixe: `/presence`)  
**Description**: Système de pointage pour les projets CINEMA

### `GET /presence/`
**Description**: Page principale de gestion de présence
**Template**: `presence/index.html`
**Affichage**: Liste des projets actifs

---

### `GET /presence/project/<int:project_id>`
**Description**: Gestion de présence pour un projet spécifique
**Template**: `presence/project_attendance.html`
**Paramètres**: `project_id` - ID du projet

**Fonctionnalités**:
- Liste des talents assignés
- Statut de présence (Absent, Présent, Pointé sortie)
- Pointage entrée/sortie individuel
- Pointage groupé
- Historique de présence

---

### `POST /presence/record`
**Description**: Enregistrer un pointage (entrée ou sortie)
**POST Data**:
- `project_id` - ID du projet
- `cinema_talent_code` - Code du talent
- `action` - "check_in" ou "check_out"

**Processus**:
1. Vérification que le talent est assigné au projet
2. Enregistrement du timestamp
3. Mise à jour du statut

---

### `POST /presence/check_in_all/<int:project_id>`
**Description**: Pointer l'entrée de tous les talents assignés
**Paramètres**: `project_id`
**Action**: Crée des enregistrements de présence pour tous

---

### `POST /presence/check_out_all/<int:project_id>`
**Description**: Pointer la sortie de tous les talents présents
**Paramètres**: `project_id`

---

### `GET /presence/history/<cinema_talent_code>`
**Description**: Historique de présence d'un talent
**Template**: `presence/talent_history.html`
**Paramètres**: `cinema_talent_code` - Code du talent

**Affichage**:
- Tous les projets du talent
- Dates et heures de présence
- Statistiques (jours de présence, absences)

---

### `GET /presence/export/<int:project_id>`
**Description**: Export Excel des présences d'un projet
**Format**: .xlsx avec tableau formaté
**Contenu**:
- Nom du talent
- Dates
- Heure d'arrivée
- Heure de départ
- Temps total

---

## 7. API Legacy

**Blueprint**: `api` (Préfixe: `/api`)  
**Note**: API de base, utilisez `/api/v1` pour l'API moderne

### `GET /api/countries`
**Description**: Liste de tous les pays
**Response**: JSON
```json
[
  {
    "id": 1,
    "name": "Maroc",
    "code": "MA"
  }
]
```

---

### `GET /api/cities`
**Description**: Liste de toutes les villes
**Paramètres optionnels**: `country_id` - Filtrer par pays
**Response**: JSON
```json
[
  {
    "id": 1,
    "name": "Rabat",
    "code": "RAB"
  }
]
```

---

### `GET /api/talents`
**Description**: Liste de tous les talents actifs
**Response**: JSON
```json
[
  {
    "id": 1,
    "name": "Développeur Web",
    "emoji": "💻",
    "category": "Technologie"
  }
]
```

---

## 8. API REST v1

**Blueprint**: `api_v1` (Préfixe: `/api/v1`)  
**Authentification**: Session-based (cookies)  
**CSRF**: Désactivé pour toutes les routes API v1

### Authentification API

#### `POST /api/v1/auth/login`
**Description**: Connexion API
**Content-Type**: `application/json`

**Request Body**:
```json
{
  "identifier": "email@example.com",
  "password": "password123"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "unique_code": "MAM0001RAB",
    "first_name": "John",
    "last_name": "Doe",
    "is_admin": false
  }
}
```

**Response** (401 Unauthorized):
```json
{
  "success": false,
  "error": "Invalid credentials"
}
```

---

#### `POST /api/v1/auth/logout`
**Description**: Déconnexion API
**Authentification**: Requise

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

#### `GET /api/v1/auth/me`
**Description**: Informations de l'utilisateur connecté
**Authentification**: Requise

**Response** (200 OK):
```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "unique_code": "MAM0001RAB",
    "first_name": "John",
    "last_name": "Doe",
    "is_admin": false,
    "account_active": true,
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

### Gestion des Utilisateurs

#### `GET /api/v1/users`
**Description**: Liste des utilisateurs avec filtres
**Authentification**: Requise + Admin
**Pagination**: Oui

**Query Parameters**:
- `search` - Recherche par nom/email/code
- `country_id` - Filtrer par pays
- `city_id` - Filtrer par ville
- `gender` - Filtrer par genre
- `availability` - Filtrer par disponibilité
- `page` - Numéro de page (défaut: 1)
- `limit` - Résultats par page (max 100, défaut: 20)

**Response** (200 OK):
```json
{
  "success": true,
  "total": 150,
  "page": 1,
  "limit": 20,
  "users": [
    {
      "id": 1,
      "unique_code": "MAM0001RAB",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "gender": "M",
      "availability": "disponible_maintenant",
      "country": "Maroc",
      "city": "Rabat",
      "account_active": true,
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

---

#### `GET /api/v1/users/<int:id>`
**Description**: Détails d'un utilisateur spécifique
**Authentification**: Requise + Admin
**Paramètres**: `id` - ID de l'utilisateur

**Response** (200 OK):
```json
{
  "success": true,
  "user": {
    "id": 1,
    "unique_code": "MAM0001RAB",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+212600000000",
    "whatsapp": "+212600000000",
    "bio": "Développeur passionné...",
    "talents": [
      {"id": 1, "name": "Développeur Web", "category": "Technologie"}
    ],
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

#### `DELETE /api/v1/users/<int:id>`
**Description**: Supprimer un utilisateur
**Authentification**: Requise + Admin

**Response** (200 OK):
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

---

#### `POST /api/v1/users/<int:id>/toggle-active`
**Description**: Activer/Désactiver un compte
**Authentification**: Requise + Admin

**Response** (200 OK):
```json
{
  "success": true,
  "message": "User account activated",
  "account_active": true
}
```

---

### Talents

#### `GET /api/v1/talents`
**Description**: Liste de tous les talents

**Response** (200 OK):
```json
{
  "success": true,
  "total": 73,
  "talents": [
    {
      "id": 1,
      "name": "Développeur Web",
      "emoji": "💻",
      "category": "Technologie",
      "is_active": true
    }
  ]
}
```

---

#### `GET /api/v1/countries`
**Description**: Liste de tous les pays

**Response** (200 OK):
```json
{
  "success": true,
  "total": 54,
  "countries": [
    {
      "id": 1,
      "name": "Maroc",
      "code": "MA",
      "flag": "🇲🇦"
    }
  ]
}
```

---

#### `GET /api/v1/cities`
**Description**: Liste des villes
**Query Parameters**: `country_code` - Filtrer par code pays

**Response** (200 OK):
```json
{
  "success": true,
  "total": 12,
  "cities": [
    {
      "id": 1,
      "name": "Rabat",
      "code": "RAB"
    }
  ]
}
```

---

### Module CINEMA API

#### `GET /api/v1/cinema/talents`
**Description**: Liste des talents CINEMA avec filtres avancés

**Query Parameters** (tous optionnels):
- `name` - Recherche par nom
- `talent_type` - Type de talent
- `gender` - Genre (M/F)
- `age_min` / `age_max` - Tranche d'âge
- `ethnicity` - Ethnicité
- `eye_color` - Couleur des yeux
- `hair_color` - Couleur des cheveux
- `skin_tone` - Teint
- `height_min` / `height_max` - Taille (cm)
- `country` - Pays de résidence
- `language` - Langue parlée
- `experience_level` - Niveau d'expérience
- `page` - Numéro de page
- `limit` - Résultats par page (max 100)

**Response** (200 OK):
```json
{
  "success": true,
  "total": 45,
  "page": 1,
  "limit": 20,
  "talents": [
    {
      "id": 1,
      "unique_code": "MACAS0001F",
      "first_name": "Sophia",
      "last_name": "Martinez",
      "gender": "F",
      "age": 28,
      "height": 170,
      "eye_color": "Marron",
      "hair_color": "Noir",
      "skin_tone": "Medium",
      "talent_types": ["Acteur Principal", "Mannequin"],
      "languages": ["Français", "Arabe", "Anglais"],
      "country_of_residence": "Maroc",
      "city_of_residence": "Casablanca",
      "has_photo": true,
      "created_at": "2024-02-10T14:20:00"
    }
  ]
}
```

---

#### `GET /api/v1/cinema/talents/<int:id>`
**Description**: Détails complets d'un talent CINEMA

**Response** (200 OK):
```json
{
  "success": true,
  "talent": {
    "id": 1,
    "unique_code": "MACAS0001F",
    "first_name": "Sophia",
    "last_name": "Martinez",
    "email": "sophia@demo.cinema",
    "phone": "+212600111222",
    "date_of_birth": "1996-03-15",
    "gender": "F",
    "talent_types": ["Acteur Principal", "Mannequin"],
    "physical_characteristics": {
      "height": 170,
      "eye_color": "Marron",
      "hair_color": "Noir",
      "hair_type": "Ondulé",
      "skin_tone": "Medium",
      "build": "Athlétique"
    },
    "languages": ["Français", "Arabe", "Anglais"],
    "experience": {
      "years": 8,
      "level": "Confirmé",
      "previous_productions": [
        "Casablanca Nights (2022)",
        "Desert Dreams (2021)"
      ]
    },
    "location": {
      "country_of_origin": "Maroc",
      "nationality": "Marocaine",
      "country_of_residence": "Maroc",
      "city_of_residence": "Casablanca"
    },
    "social_media": {
      "facebook": "sophiamartinez",
      "instagram": "@sophiamartinez",
      "tiktok": "@sophiamartinez"
    },
    "has_photo": true,
    "qr_code_path": "uploads/qrcodes/...",
    "created_at": "2024-02-10T14:20:00"
  }
}
```

---

#### `GET /api/v1/cinema/stats`
**Description**: Statistiques du module CINEMA

**Response** (200 OK):
```json
{
  "success": true,
  "stats": {
    "total_talents": 45,
    "by_type": {
      "Acteur Principal": 12,
      "Acteur Secondaire": 8,
      "Figurant": 15,
      "Mannequin": 6
    },
    "by_gender": {
      "M": 23,
      "F": 22
    },
    "by_country": {
      "Maroc": 35,
      "Sénégal": 6,
      "Côte d'Ivoire": 4
    },
    "with_photos": 40,
    "without_photos": 5
  }
}
```

---

### Statistiques Globales

#### `GET /api/v1/stats/overview`
**Description**: Vue d'ensemble des statistiques
**Authentification**: Requise + Admin

**Response** (200 OK):
```json
{
  "success": true,
  "stats": {
    "total_users": 250,
    "active_users": 230,
    "inactive_users": 20,
    "total_cinema_talents": 45,
    "total_productions": 12,
    "total_projects": 8,
    "new_users_last_7_days": 15,
    "profile_completion_avg": 75.5
  }
}
```

---

#### `GET /api/v1/stats/talents`
**Description**: Statistiques détaillées des talents
**Authentification**: Requise + Admin

**Response** (200 OK):
```json
{
  "success": true,
  "stats": {
    "total_talents": 73,
    "top_talents": [
      {"name": "Développeur Web", "count": 45},
      {"name": "Designer", "count": 32}
    ],
    "by_category": {
      "Technologie": 120,
      "Créatif": 89,
      "Business": 56
    }
  }
}
```

---

### Exports API

#### `GET /api/v1/export/users/excel`
**Description**: Export Excel des utilisateurs
**Authentification**: Requise + Admin
**Response**: Fichier .xlsx

---

#### `GET /api/v1/export/users/csv`
**Description**: Export CSV des utilisateurs
**Authentification**: Requise + Admin
**Response**: Fichier .csv

---

#### `GET /api/v1/export/users/pdf`
**Description**: Export PDF des utilisateurs
**Authentification**: Requise + Admin
**Response**: Fichier .pdf

---

## Codes d'État HTTP

| Code | Signification | Utilisation |
|------|---------------|-------------|
| 200 | OK | Requête réussie |
| 201 | Created | Ressource créée avec succès |
| 204 | No Content | Succès sans contenu de retour |
| 400 | Bad Request | Données invalides |
| 401 | Unauthorized | Authentification requise ou échouée |
| 403 | Forbidden | Accès interdit (droits insuffisants) |
| 404 | Not Found | Ressource introuvable |
| 409 | Conflict | Conflit (ex: email déjà existant) |
| 500 | Internal Server Error | Erreur serveur |

---

## Sécurité des Routes

### Niveaux d'Authentification

1. **PUBLIC** - Accès sans authentification
   - `/auth/login`, `/auth/register`
   - `/cinema/register`
   - `/cinema/profile/<code>`

2. **AUTHENTICATED** - Utilisateur connecté requis (`@login_required`)
   - Toutes les routes `/profile/*`
   - Routes `/cinema/*` (sauf register et profile)
   - Route `/`

3. **ADMIN** - Administrateur requis (`@login_required` + `@admin_required`)
   - Toutes les routes `/admin/*`
   - Routes API `/api/v1/users/*` (lecture/modification)
   - Exports et statistiques

### Protection CSRF

- **Activée** : Toutes les routes web (formulaires HTML)
- **Désactivée** : Routes `/api/v1/*` (utilise session-based auth)

### Chiffrement des Données

**Données chiffrées** (Fernet AES-128):
- Numéros de téléphone et WhatsApp
- Adresses postales
- Tous les réseaux sociaux
- Numéros de documents d'identité (CINEMA)

**Données hashées** (bcrypt):
- Mots de passe utilisateurs

---

## Limites et Quotas

### Upload de Fichiers

| Type | Formats | Taille Max | Validation |
|------|---------|------------|------------|
| Photos | PNG, JPG, JPEG | 5 MB | MIME + Extension |
| CVs | PDF, DOC, DOCX | 10 MB | MIME + Extension |
| Global | - | 10 MB | Config Flask |

### API Pagination

- **Défaut**: 20 résultats par page
- **Maximum**: 100 résultats par page
- **Paramètres**: `page` (numéro), `limit` (taille)

---

## Notes de Développement

### Ajout de Nouvelles Routes

1. Créer la route dans le blueprint approprié
2. Ajouter les décorateurs d'authentification si nécessaire
3. Créer le template Jinja2 correspondant
4. Tester avec différents rôles (public, user, admin)
5. Mettre à jour cette documentation

### Conventions de Nommage

- **Routes web**: Kebab-case (`/user-profile/edit`)
- **Routes API**: Snake_case ou camelCase selon le standard
- **Templates**: Snake_case (`user_profile.html`)
- **Fonctions Python**: Snake_case (`def get_user_profile()`)

---

**Dernière mise à jour**: 26 Octobre 2025  
**Version de l'application**: 1.0.0  
**Auteur**: MOA Digital Agency LLC - Aisance KALONJI
