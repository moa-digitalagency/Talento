# Changelog - Talento

Toutes les modifications notables du projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-19

### 🚀 Ajouts Majeurs

#### Analyse Intelligente de CV
- **Service d'analyse IA** (`app/services/cv_analyzer.py`)
  - Intégration avec OpenRouter AI pour analyse automatique des CV
  - Extraction de texte depuis PDF et DOCX
  - Génération de score de profil (0-100)
  - Détection automatique des compétences
  - Recommandations personnalisées
  - Analyse des points forts et faibl esses

#### Système d'Export Complet
- **Service d'export** (`app/services/export_service.py`)
  - Export Excel (XLSX) avec mise en forme automatique
  - Export CSV pour analyse de données
  - Export PDF liste complète avec mise en page professionnelle
  - Fiche talent individuelle PDF avec photo et détails complets

#### Dashboard Admin Amélioré
- **Filtres croisés avancés**:
  - Recherche textuelle (nom, prénom, email, code unique)
  - Recherche par code alphanumérique ou QR code
  - Filtre par talents (sélection multiple)
  - Filtre par pays d'origine
  - Filtre par ville au Maroc
  - Filtre par genre
  - Filtre par disponibilité
  - Filtre par présence de CV
  - Filtre par présence de portfolio
  - Filtre par plage de dates d'inscription
  
- **Nouvelles fonctionnalités**:
  - Page de détail talent complète
  - Statistiques en temps réel
  - Boutons d'export direct (Excel, CSV, PDF)
  - Analyse IA du CV en un clic
  - Recherche par QR code

### 🔐 Sécurité

#### Système de Migration Robuste
- **Script d'initialisation** (`migrations_init.py`)
  - Vérification automatique de la structure de la base
  - Création des tables manquantes
  - Ajout des colonnes manquantes
  - Correction automatique de la structure
  - Seeding idempotent des données
  - Création automatique du super admin

#### Chiffrement des Données
- Toutes les données sensibles chiffrées avec Fernet (chiffrement symétrique)
- Clé de chiffrement configurée via variable d'environnement `ENCRYPTION_KEY`
- Protection des numéros de téléphone, adresses et réseaux sociaux

#### Compte Admin Sécurisé
- Email: `admin@talento.com` (changé depuis admin@talento.app)
- Mot de passe: configurable via `ADMIN_PASSWORD` (défaut: `@4dm1n`)
- Code unique: `MARAB0001N`
- Hashage bcrypt pour tous les mots de passe

### 📊 Modèle de Données

#### Nouveaux Champs User
- `cv_analysis` (TEXT) - Stockage de l'analyse IA au format JSON
- `cv_analyzed_at` (DATETIME) - Date de la dernière analyse
- Champs déjà présents utilisés:
  - `availability` - Disponibilité du talent
  - `work_mode` - Mode de travail préféré
  - `rate_range` - Fourchette tarifaire
  - `profile_score` - Score du profil (0-100)

### 🛠️ Infrastructure

#### Dépendances Ajoutées
- `PyPDF2==3.0.1` - Extraction de texte depuis PDF
- `python-docx==1.1.0` - Lecture de documents Word
- `requests==2.31.0` - Appels API vers OpenRouter

#### Intégrations API
- **OpenRouter** - Analyse IA des CV et profils
- **SendGrid** - Envoi d'emails transactionnels

### 📝 Templates

#### Nouveaux Templates
- `app/templates/admin/user_detail.html` - Fiche talent détaillée
  - Affichage complet du profil
  - Export PDF individuel
  - Bouton d'analyse IA
  - Visualisation des réseaux sociaux
  - Affichage des résultats d'analyse

### 🔧 Routes Admin Étendues

#### Nouvelles Routes
- `GET /admin/dashboard` - Dashboard avec filtres avancés
- `GET /admin/user/<id>` - Détail d'un talent
- `GET /admin/export/excel` - Export Excel de tous les talents
- `GET /admin/export/csv` - Export CSV de tous les talents
- `GET /admin/export/pdf` - Export PDF liste des talents
- `GET /admin/user/<id>/export_pdf` - Export PDF fiche individuelle
- `POST /admin/user/<id>/analyze_cv` - Analyse IA du CV
- `GET /admin/search_by_qr` - Recherche par QR code

### ⚙️ Configuration

#### Variables d'Environnement
**Nouvelles (requises)**:
- `ENCRYPTION_KEY` - Clé de chiffrement des données sensibles
- `OPENROUTER_API_KEY` - Clé API pour analyse IA
- `SENDGRID_API_KEY` - Clé API pour emails

**Existantes (mises à jour)**:
- `ADMIN_PASSWORD` - Mot de passe admin (défaut changé à `@4dm1n`)
- `SECRET_KEY` - Clé secrète Flask
- `DATABASE_URL` - URL PostgreSQL (Helium)

### 📚 Documentation

#### Fichiers Mis à Jour
- `replit.md` - Documentation projet complète et à jour
- `CHANGELOG.md` - Nouveau fichier de suivi des changements
- `README.md` - Guide utilisateur mis à jour

### 🔄 Migrations

#### Processus de Déploiement
1. Le script `migrations_init.py` s'exécute automatiquement au démarrage
2. Vérifie et corrige la structure de la base de données
3. Ajoute les données manquantes (pays, villes, talents)
4. Crée le compte super admin si absent
5. Garantit la cohérence des données

### 🎯 Améliorations de Performance

- **Requêtes optimisées** avec filtres et indexes
- **Export en streaming** pour fichiers volumineux
- **Analyse IA asynchrone** avec feedback utilisateur
- **Calcul de score intelligent** basé sur la complétude du profil

### 🐛 Corrections

- Email admin changé de `admin@talento.app` à `admin@talento.com`
- Mot de passe admin plus sécurisé par défaut
- Structure de base de données auto-réparable
- Meilleure gestion des données chiffrées

---

## [1.0.0] - 2025-10-18

### Version Initiale

- Système d'inscription complet
- Génération de codes uniques (format: PP-VVV-NNNN-G)
- Génération de QR codes
- Upload photo et CV
- 54 pays africains
- 74 talents en 14 catégories
- Dashboard admin basique
- Authentification avec Flask-Login
- Interface Tailwind CSS responsive
- Base de données PostgreSQL

---

## Format des Versions

- **Version Majeure** (X.0.0) : Changements incompatibles
- **Version Mineure** (1.X.0) : Nouvelles fonctionnalités compatibles
- **Version Patch** (1.0.X) : Corrections de bugs
