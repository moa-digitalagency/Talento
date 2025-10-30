# 🎭 taalentio.com

**La plateforme de centralisation des talents africains avec un focus sur l'industrie cinématographique**

taalentio.com est une application web professionnelle conçue pour centraliser et mettre en valeur les profils de talents à travers l'Afrique. La plateforme permet aux professionnels de créer des profils détaillés, de valoriser leurs compétences et de se connecter à des opportunités - avec un module dédié CINEMA pour l'industrie audiovisuelle.

---

## ✨ Fonctionnalités Principales

### 🎬 Module CINEMA (Industrie Audiovisuelle)

**Le cœur de TalentsMaroc** - Un système complet dédié aux professionnels du cinéma et de l'audiovisuel:

#### Pour les Talents
- **Inscription Publique Complète** : Formulaire en 9 sections pour un profil détaillé
  - Identité et contact avec chiffrement des données sensibles
  - Origines et résidence (pays, ville, ethnicités multiples)
  - Langues parlées avec drapeaux visuels
  - Caractéristiques physiques détaillées (taille, yeux, cheveux, teint, morphologie)
  - **13 types de talents** : Acteur Principal, Acteur Secondaire, Figurant, Silhouette, Doublure, Doublure Lumière, Cascadeur, Mannequin, Voix Off, Figurant Spécialisé, Choriste, Danseur de fond, Autre
  - Compétences cinématographiques catégorisées
  - Réseaux sociaux (Facebook, Instagram, TikTok, Telegram - tous chiffrés)
  - Photos et historique de productions
- **Profil Public avec QR Code** : Chaque talent dispose d'une page publique accessible via QR code
- **Carte PDF Professionnelle** : Génération automatique d'une carte talent imprimable
- **Code Unique 12 Caractères** : Format PPVVVNNNNNNNG (ex: MACAS000001F)

#### Pour les Productions
- **Gestion des Boîtes de Production** :
  - Profils complets avec coordonnées, équipements, studios
  - Historique de productions notables
  - Services offerts et certifications
  - Réseaux sociaux et sites web
  - Statut de vérification

#### Pour les Projets
- **Système de Gestion de Projets** :
  - Création de projets (films, séries, publicités, documentaires)
  - Lien avec les boîtes de production
  - Assignation de talents aux projets
  - **Codes Projet Uniques** : Format PRJ-XXX-YYY pour chaque assignation
  - **Génération de Badges PDF** : Badges personnalisés pour chaque talent assigné
  - Suivi de statut (Préparation, Tournage, Post-production, Terminé)
  - Gestion des lieux de tournage et dates

#### Recherche Avancée CINEMA
Filtrage par 12 critères :
- Nom, type de talent, genre
- Tranche d'âge (18-25, 26-35, 36-50, 51+)
- Ethnicité, couleur des yeux, couleur de cheveux
- Teint, taille, pays, langues
- Niveau d'expérience

#### Statistiques CINEMA
- Nombre total de talents par type
- Répartition par genre et pays
- Analyse des compétences
- Talents avec/sans photo

### 👤 Profils Utilisateurs Standards

#### Inscription et Authentification
- **Inscription Multi-Étapes** : Formulaire guidé en plusieurs étapes
- **Connexion Flexible** : Email OU code unique
- **Sécurité Renforcée** : Mots de passe hachés (bcrypt), données sensibles chiffrées (Fernet)

#### Profils Complets
- **Informations Personnelles** : Nom, prénom, date de naissance, genre
- **Contact Chiffré** : Téléphone, WhatsApp, adresse (tous chiffrés)
- **Localisation** : 54 pays africains + villes principales
- **Informations Professionnelles** :
  - Biographie professionnelle
  - Disponibilité (Immédiate, Prochainement, Non disponible, Projet actuel)
  - Mode de travail (Sur site, À distance, Hybride, Flexible)
  - Fourchette tarifaire
  - Années d'expérience
  - Domaine d'expertise
- **Portfolio** :
  - CV uploadable (PDF, DOC, DOCX)
  - Photo de profil
  - URL portfolio
  - Site web personnel
- **Réseaux Sociaux** (tous chiffrés) :
  - LinkedIn, Instagram, Twitter/X, Facebook
  - GitHub, Behance, Dribbble
  - IMDb, Threads

#### Talents Multiples
Sélection parmi des dizaines de catégories :
- Technologies (Développeur, Data Scientist, DevOps, etc.)
- Créatif (Designer, Photographe, Vidéaste, etc.)
- Business (Marketing, Commercial, Gestionnaire, etc.)
- Éducation & Santé
- Et bien d'autres...

#### QR Code Personnel
Chaque profil génère automatiquement un QR code unique pour partage facile

### 🤖 Intelligence Artificielle - Fonctionnalités IA Complètes

**Powered by OpenRouter AI** utilisant les modèles **Google Gemini Flash**

taalentio.com intègre des fonctionnalités d'intelligence artificielle avancées pour automatiser et optimiser le processus de recrutement et de casting.

**Modèles IA Utilisés**:
- **CV Analyzer**: `google/gemini-2.5-flash` (30s timeout)
- **AI Matching (Standard & CINEMA)**: `google/gemini-2.0-flash-001:free` (60s timeout)

#### 1. Analyse IA de CV (CVAnalyzerService)

**Extraction et Analyse Automatique** :
- **Formats Supportés** : PDF, DOC, DOCX (max 10 MB)
- **Extraction Intelligente** :
  - Texte depuis PDF (PyPDF2)
  - Contenu depuis DOCX (python-docx)
  - Traitement automatique de fichiers texte
- **Analyse Sémantique** :
  - Compréhension du contenu par IA
  - Identification des compétences techniques et soft skills
  - Détection de l'expérience professionnelle
  - Extraction des formations et certifications
  - Analyse des projets et réalisations

**Score de Profil** (0-100) :

L'IA évalue les CV selon ces critères:
- **20 points** - Clarté et structure du CV
- **25 points** - Expérience pertinente
- **25 points** - Compétences techniques
- **15 points** - Formation et certifications
- **15 points** - Réalisations mesurables

Le système calcule aussi un score de complétude du profil basé sur:
- Informations personnelles (nom, email, téléphone, date de naissance, localisation)
- Fichiers (photo, CV, portfolio)
- Biographie et talents déclarés
- Réseaux sociaux professionnels

**Recommandations Personnalisées** :
- Suggestions d'amélioration du profil
- Identification des sections manquantes
- Conseils pour maximiser la visibilité
- Points forts à mettre en avant

**Déclenchement** :
- Manuel via l'interface administrateur
- Endpoint: `POST /admin/analyze-cv/<user_id>`

#### 2. Matching IA Intelligent (AIMatchingService)

**Pour Talents Standards** :

**Analyse de Descriptions de Poste** :
- **Upload de Fichiers** : PDF, DOCX, TXT ou saisie directe
- **Extraction Automatique** : Analyse des exigences, compétences requises, expérience
- **Matching Multi-Critères** :
  - Analyse des compétences techniques du CV
  - Comparaison avec les talents déclarés
  - Vérification de la disponibilité et mode de travail
  - Analyse de la localisation géographique
  - Évaluation de l'expérience professionnelle

**Scoring Intelligent** (0-100) :
- Score de compatibilité pour chaque candidat
- **Explication Détaillée** : Justification IA du score
- **Points Forts** : Liste des atouts du candidat pour le poste
- **Points Faibles** : Identification des manques ou écarts
- Classement automatique par pertinence

**Résultats Structurés** :
```json
{
  "success": true,
  "candidates": [
    {
      "user": {...},
      "score": 85,
      "explication": "Candidat hautement qualifié...",
      "points_forts": ["5 ans d'expérience", "Maîtrise React/Node"],
      "points_faibles": ["Localisation distante"]
    }
  ],
  "total_analyzed": 50,
  "total_matched": 12
}
```

**API Endpoint** : `POST /ai-search`

#### 3. Casting IA pour Talents CINEMA

**Analyse de Rôles Cinématographiques** :
- **Description de Rôle** : Upload ou saisie directe
- **Critères Physiques** : Âge, genre, taille, poids, teint, yeux, cheveux
- **Critères Artistiques** : Types de talents, compétences, expérience
- **Critères Linguistiques** : Langues parlées, accents
- **Critères Géographiques** : Localisation, disponibilité

**Matching Spécialisé CINEMA** :
- Analyse des caractéristiques physiques détaillées
- Évaluation de l'expérience cinématographique
- Vérification des compétences spéciales (cascades, danse, équitation, etc.)
- Analyse des productions précédentes
- Compatibilité avec le type de production

**Scoring Casting** (0-100) :
- Compatibilité physique avec le rôle
- Adéquation des compétences artistiques
- Expérience pertinente
- Disponibilité et localisation
- Justifications détaillées par l'IA

**Résultats Personnalisés** :
- Top candidats classés par score
- Profils détaillés avec photos
- Liens directs vers profils publics et QR codes
- Exportation PDF des résultats

**API Endpoint** : `POST /cinema/ai-search`

#### Configuration OpenRouter

**Clé API** :
- Variable d'environnement : `OPENROUTER_API_KEY` (prioritaire pour CV Analyzer)
- Configuration admin : `Paramètres → Clés API` (pour AI Matching)
- Support des clés gratuites OpenRouter

**Modèles et Configuration** :

**CV Analyzer Service**:
- Modèle: `google/gemini-2.5-flash`
- Timeout: 30 secondes
- Température: 0.3
- Max tokens: 1000

**AI Matching Services** (Standard & CINEMA):
- Modèle: `google/gemini-2.0-flash-001:free`
- Timeout: 60 secondes
- Température: 0.3
- Headers additionnels pour référence

**Optimisations** :
- Température 0.3 pour des résultats cohérents
- Gestion d'erreurs avec messages clairs
- Extraction CV limitée à 3000 caractères
- Support du français natif
- Format JSON structuré

#### Sécurité et Confidentialité IA

- **Données Non Stockées** : Les prompts ne sont pas conservés par OpenRouter
- **Anonymisation** : Seules les données nécessaires sont envoyées
- **Chiffrement** : Communications HTTPS avec OpenRouter
- **Conformité RGPD** : Données personnelles protégées

### 🛠️ Administration Puissante

#### Dashboard Administrateur
- **Vue d'Ensemble** :
  - Nombre total d'utilisateurs
  - Nouveaux inscrits (7 derniers jours)
  - Talents CINEMA enregistrés
  - Taux de complétion moyen des profils
  - Répartition par pays (top 5)
- **Accès Rapide** : Gestion utilisateurs, talents, CINEMA, exports, paramètres

#### Gestion des Utilisateurs
- **Liste Complète** : Tous les utilisateurs avec statut et actions
- **Activation/Désactivation** : Contrôle des comptes
- **Édition Complète** : Modification de tous les champs
- **Suppression** : Avec confirmation
- **Promotion Admin** : Élévation des privilèges
- **Analyse IA Manuelle** : Lancement de l'analyse de CV pour n'importe quel utilisateur

#### Gestion des Talents
- **Catalogue Complet** : Visualisation de tous les talents disponibles
- **Création** : Ajout de nouveaux types de talents
- **Édition & Suppression** : Gestion complète

#### Exports de Données
- **Format Excel (.xlsx)** :
  - Feuilles formatées avec colonnes ajustées
  - Toutes les informations utilisateur
  - Talents associés
  - Données de contact déchiffrées
- **Format CSV** :
  - Compatible avec tous les tableurs
  - Encodage UTF-8
- **Format PDF** :
  - Documents formatés professionnellement
  - Logo et en-têtes
  - Cartes talents individuelles

#### Paramètres Système
- **Clés API** :
  - SendGrid (envoi d'emails)
  - OpenRouter (analyse IA)
  - OMDB (recherche de films - optionnel)
- **Configuration Email** :
  - Email expéditeur
  - Test d'envoi
- **Informations Base de Données** :
  - Statistiques de connexion
  - Nombre de tables et d'enregistrements
- **Historique des Mises à Jour** : Journal complet des versions

#### Sauvegarde & Restauration
- **Création de Sauvegardes** :
  - Archive ZIP chiffrée
  - Dump PostgreSQL complet
  - Tous les fichiers uploads (photos, CVs, QR codes)
  - Horodatage automatique
- **Restauration** :
  - Upload d'archive de sauvegarde
  - Restauration complète de la base et des fichiers

#### Mises à Jour
- **Vérification Automatique** : Détection des mises à jour disponibles via Git
- **Application en Un Clic** : Mise à jour de l'application
- **Historique** : Journal de toutes les mises à jour

### 📊 Système de Statistiques

#### Statistiques Globales
- Utilisateurs totaux, actifs, inactifs
- Nouveaux inscrits par période
- Répartition géographique (pays, villes)
- Talents les plus populaires
- Taux de complétion des profils

#### Statistiques CINEMA
- Talents par type (13 catégories)
- Répartition par genre (M/F)
- Distribution par pays
- Langues parlées
- Niveau d'expérience
- Talents avec photos vs sans photos

### 🔐 Sécurité & Confidentialité

#### Chiffrement des Données
**Algorithme** : Fernet (AES 128-bit CBC)

**Données chiffrées** :
- Numéros de téléphone (fixe et WhatsApp)
- Adresses postales
- Tous les réseaux sociaux (LinkedIn, Instagram, Twitter, Facebook, GitHub, Behance, Dribbble, IMDb, Threads, Telegram, TikTok)
- Numéros de documents d'identité (CINEMA)

#### Authentification Sécurisée
- Hachage bcrypt (12 rounds) pour les mots de passe
- Sessions sécurisées avec Flask-Login
- Protection CSRF (Flask-WTF)
- Contrôle d'accès basé sur les rôles (Admin vs Utilisateur)

#### Upload Sécurisé
- **Photos** : PNG, JPG, JPEG uniquement (max 5 MB)
- **CVs** : PDF, DOC, DOCX uniquement (max 10 MB)
- Validation des types MIME avec python-magic
- Noms de fichiers UUID pour éviter les conflisions et expositions
- Stockage organisé (`uploads/photos/`, `uploads/cvs/`, `uploads/qrcodes/`)

### 🌍 Couverture Africaine

#### 54 Pays Africains
Support complet de tous les pays africains avec codes ISO-2 :
- Maroc (MA), Sénégal (SN), Nigeria (NG), Égypte (EG), Afrique du Sud (ZA)
- Kenya (KE), Ghana (GH), Côte d'Ivoire (CI), Cameroun (CM), etc.

#### Villes Principales
Base de données pré-remplie avec les principales villes de chaque pays :
- Maroc : Rabat, Casablanca, Marrakech, Fès, Tanger, etc.
- Chargement dynamique des villes selon le pays sélectionné

### 🎨 Interface Utilisateur Moderne

#### Design Professionnel
- **Framework CSS** : Tailwind CSS
- **Responsive** : Compatible mobile, tablette, desktop
- **Navigation Intuitive** :
  - Menu adaptatif selon le rôle (admin vs utilisateur)
  - Hamburger menu pour mobile
  - Fil d'Ariane (breadcrumb)
- **Feedback Visuel** :
  - Messages flash colorés (succès, erreur, info)
  - Indicateurs de chargement
  - Validation de formulaires en temps réel

#### Dashboard Adaptatif
- **Vue Administrateur** : Statistiques complètes, gestion, exports
- **Vue Utilisateur** : Profil personnel, complétion, suggestions
- **Vue CINEMA** : Talents, productions, projets

### 📧 Système d'Emails Automatisés

**Provider** : SendGrid API

#### Emails de Confirmation
- **Inscription Utilisateur** :
  - Bienvenue personnalisée
  - Code unique attribué
  - Lien vers le profil
- **Inscription CINEMA** :
  - Confirmation d'enregistrement
  - Code CINEMA unique
  - Prochaines étapes

#### Emails de Gestion
- Envoi des identifiants de connexion
- Notifications de statut de compte
- Alertes administrateurs (configurables)

### 🔗 API REST v1

#### Authentification API
- Session-based (cookies)
- Login via `/api/v1/auth/login`
- Logout via `/api/v1/auth/logout`
- Vérification utilisateur via `/api/v1/auth/me`

#### Endpoints Principaux
**Utilisateurs** (`/api/v1/users`):
- Liste avec pagination et filtres (search, pays, ville, genre, disponibilité)
- Détails utilisateur
- Mise à jour (admin)
- Suppression (admin)

**Talents** (`/api/v1/talents`):
- Liste complète
- Détails talent
- Utilisateurs par talent

**CINEMA** (`/api/v1/cinema`):
- Liste talents CINEMA (filtres avancés)
- Détails talent CINEMA
- Liste productions
- Liste projets

**Statistiques** (`/api/v1/stats`):
- Vue d'ensemble (`/overview`)
- Stats utilisateurs (`/users`)
- Stats CINEMA (`/cinema`)

**Exports** (`/api/v1/exports`):
- Export Excel utilisateurs (`/users/excel`)
- Export CSV utilisateurs (`/users/csv`)
- Export Excel CINEMA (`/cinema/excel`)

#### Documentation API Complète
- [Documentation EN](api_docs/API_DOCUMENTATION_EN.md)
- [Documentation FR](api_docs/API_DOCUMENTATION_FR.md)

### 🎯 Système de Codification Unique

#### Codes Utilisateurs Standards
**Format** : `PPGNNNNVVV` (10 caractères)
- **PP** : Code pays ISO-2 (ex: MA pour Maroc)
- **G** : Genre (M, F, ou N)
- **NNNN** : 4 chiffres séquentiels **par pays** (incrémentation globale par pays)
- **VVV** : 3 premières lettres de la ville (ex: RAB pour Rabat)

**Exemple** : `MAM0001RAB`

**Important** : Le numéro est séquentiel et incrémenté **par pays**, pas par ville:
- `MAM0001RAB` = 1ère personne au Maroc (de Rabat), genre masculin
- `MAF0002CAS` = 2ème personne au Maroc (de Casablanca), genre féminin
- `SNM0001DAK` = 1ère personne au Sénégal (de Dakar), genre masculin

#### Codes CINEMA
**Format** : `PPVVVNNNNNG` (11 caractères)
- **PP** : Code pays ISO-2 (ex: MA pour Maroc)
- **VVV** : 3 premières lettres de la ville (ex: CAS pour Casablanca)
- **NNNN** : 4 chiffres séquentiels **par pays** (incrémentation globale par pays)
- **G** : Genre (M ou F)

**Exemple** : `MACAS0001F`

**Important** : Le compteur est global par pays (identique aux codes standards):
- `MACAS0001F` = 1ère personne CINEMA au Maroc (de Casablanca)
- `MARAB0002M` = 2ème personne CINEMA au Maroc (de Rabat)
- `SNDAG0001F` = 1ère personne CINEMA au Sénégal (de Dakar)

**Distinction** : Les codes CINEMA se distinguent des codes standards par l'ordre des composants (Ville avant Numéro pour CINEMA, Genre avant Numéro pour standards).

#### Codes Projets
**Format** : `PRJXXXYYY` (9 caractères, pas de tirets)
- **XXX** : ID du projet (3 chiffres)
- **YYY** : Numéro d'assignation du talent (3 chiffres)

**Exemple** : `PRJ001042` (Projet 1, 42ème talent assigné)

---

## 🚀 Installation et Démarrage

### Prérequis

- Python 3.11 ou supérieur
- PostgreSQL 14+ (ou SQLite pour développement)
- Git

### Installation Rapide

```bash
# 1. Cloner le repository
git clone <repository-url>
cd talentsmaroc

# 2. Installer les dépendances Python
pip install -r requirements.txt

# 3. Configurer les variables d'environnement
# Créer un fichier .env à la racine
```

### Configuration

Créer un fichier `.env` avec les variables suivantes :

```bash
# Obligatoires
SECRET_KEY=votre-cle-secrete-super-longue-et-aleatoire
DATABASE_URL=postgresql://user:password@localhost:5432/talentsmaroc
ENCRYPTION_KEY=votre-cle-de-chiffrement-32-bytes-base64

# Optionnelles (configurables via l'interface admin)
SENDGRID_API_KEY=SG.votre-cle-sendgrid
SENDGRID_FROM_EMAIL=noreply@talentsmaroc.com
OPENROUTER_API_KEY=sk-or-votre-cle-openrouter
OMDB_API_KEY=votre-cle-omdb
ADMIN_PASSWORD=@4dm1n
```

**Génération de la clé de chiffrement** :
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### Initialisation de la Base de Données

```bash
# Créer les tables et insérer les données de démonstration
python migrations_init.py
```

**Cette commande** :
1. Crée toutes les tables
2. Charge les 54 pays africains
3. Charge les villes principales
4. Crée le compte administrateur
5. Crée 5 comptes utilisateurs de démonstration
6. Crée 3 talents CINEMA de démonstration
7. Crée 2 boîtes de production de démonstration

### Lancement de l'Application

```bash
# Mode développement
python app.py

# L'application sera accessible sur http://localhost:5004
```

**Mode production** (avec Gunicorn) :
```bash
gunicorn --bind 0.0.0.0:5004 --reuse-port --workers 4 app:app
```

---

## 🔧 Dépannage et Correction de Problèmes

### Problème : Les listes déroulantes (pays, villes, talents) sont vides

**Symptômes** :
- Les formulaires d'inscription (utilisateur ou CINEMA) ne montrent aucun pays
- Les listes de villes sont vides
- La liste des talents ne se charge pas

**Cause** :
Les données essentielles (pays, villes, talents) ne sont pas chargées dans la base de données.

**Solution Rapide** :

Exécutez le script d'initialisation des données :

```bash
# Avec les variables d'environnement nécessaires
SECRET_KEY=votre-cle python init_essential_data.py

# OU si vous utilisez un fichier .env
python init_essential_data.py
```

**Ce que fait le script** :
- ✅ Charge **194 pays du monde** (pas seulement l'Afrique)
- ✅ Charge **1711 villes** réparties dans le monde entier
- ✅ Charge **70 talents** pour l'industrie cinématographique
- ⚡ Exécution rapide (< 30 secondes)
- 🔄 Idempotent (peut être exécuté plusieurs fois sans doublon)

**Sortie attendue** :
```
======================================================================
🚀 INITIALISATION DES DONNÉES ESSENTIELLES
======================================================================
✅ Tables de base de données vérifiées

🌍 Chargement de tous les pays du monde...
✅ 194 nouveaux pays ajoutés (Total: 194 pays)

🏙️  Chargement des villes du monde...
✅ 1711 nouvelles villes ajoutées (Total: 1711 villes)

⭐ Chargement de tous les talents...
✅ 70 nouveaux talents ajoutés (Total: 70 talents)

======================================================================
✅ INITIALISATION TERMINÉE AVEC SUCCÈS!
======================================================================
```

**Vérification Automatique au Démarrage** :

L'application vérifie automatiquement au démarrage si les données sont présentes :
- Si < 100 pays : chargement automatique
- Si < 1000 villes : chargement automatique  
- Si < 50 talents : chargement automatique

Le script `init_essential_data.py` sera exécuté automatiquement si nécessaire.

**Note** : Ce script peut être lancé à tout moment pour corriger les données manquantes, même avec l'application en cours d'exécution.

---

## 👨‍💼 Comptes par Défaut

### Administrateur

| Champ | Valeur |
|-------|--------|
| Email | `admin@talento.com` |
| Code Unique | `MAN0001RAB` |
| Mot de passe | `@4dm1n` |

⚠️ **IMPORTANT** : Changez le mot de passe admin après la première connexion !

### Comptes de Démonstration

**Utilisateurs Standards** :
- `demo1@talento.com` à `demo5@talento.com`
- Mot de passe : `demo123`

**Talents CINEMA** :
- 3 comptes avec emails se terminant par `@demo.cinema`
- Profils complets avec photos et caractéristiques

**Productions** :
- Morocco Films Production (Casablanca)
- Atlas Studios Production (Ouarzazate)

---

## 📂 Structure du Projet

```
talentsmaroc/
├── app/                          # Application principale
│   ├── models/                   # Modèles de données (SQLAlchemy)
│   │   ├── user.py              # Utilisateurs standards
│   │   ├── cinema_talent.py     # Talents CINEMA
│   │   ├── production.py        # Boîtes de production
│   │   ├── project.py           # Projets et assignations
│   │   ├── talent.py            # Catalogue talents
│   │   ├── location.py          # Pays et villes
│   │   └── settings.py          # Paramètres application
│   ├── routes/                   # Routes/Blueprints
│   │   ├── main.py              # Pages principales
│   │   ├── auth.py              # Authentification
│   │   ├── profile.py           # Profils utilisateurs
│   │   ├── admin.py             # Administration
│   │   ├── cinema.py            # Module CINEMA
│   │   └── api_v1/              # API REST v1
│   ├── services/                 # Logique métier
│   │   ├── cv_analyzer.py       # Analyse IA de CV
│   │   ├── email_service.py     # Envoi d'emails
│   │   ├── export_service.py    # Exports Excel/CSV/PDF
│   │   ├── backup_service.py    # Sauvegardes
│   │   └── movie_service.py     # Proxy OMDB API
│   ├── templates/                # Templates Jinja2
│   │   ├── base.html            # Template de base
│   │   ├── auth/                # Connexion/inscription
│   │   ├── profile/             # Profils utilisateurs
│   │   ├── admin/               # Pages admin
│   │   └── cinema/              # Module CINEMA
│   ├── static/                   # Fichiers statiques
│   │   ├── css/                 # Styles CSS
│   │   ├── js/                  # JavaScript
│   │   ├── img/                 # Images, logos
│   │   └── uploads/             # Fichiers uploadés
│   │       ├── photos/          # Photos de profil
│   │       ├── cvs/             # CVs uploadés
│   │       └── qrcodes/         # QR codes générés
│   └── utils/                    # Utilitaires
│       ├── encryption.py        # Chiffrement Fernet
│       ├── id_generator.py      # Codes utilisateurs
│       ├── cinema_code_generator.py  # Codes CINEMA
│       ├── project_code_generator.py # Codes projets
│       ├── qr_generator.py      # Génération QR codes
│       ├── file_handler.py      # Gestion fichiers
│       └── auto_migrate.py      # Migrations automatiques
├── api_docs/                     # Documentation API
│   ├── API_DOCUMENTATION_EN.md
│   └── API_DOCUMENTATION_FR.md
├── docs/                         # Documentation technique
│   └── TECHNICAL_DOCUMENTATION.md
├── migrations_archive/           # Anciennes migrations
├── logs/                         # Logs application
├── app.py                        # Point d'entrée
├── config.py                     # Configuration Flask
├── migrations_init.py            # Script d'initialisation DB
├── requirements.txt              # Dépendances Python
├── README.md                     # Ce fichier
├── README.fr.md                  # Version française
└── CHANGELOG.md                  # Journal des modifications
```

---

## 🛠️ Technologies Utilisées

### Backend
- **Flask 3.0.0** - Framework web Python
- **SQLAlchemy** - ORM pour PostgreSQL/SQLite
- **Flask-Login** - Gestion d'authentification
- **Flask-Migrate** - Migrations de base de données
- **bcrypt** - Hachage de mots de passe
- **cryptography (Fernet)** - Chiffrement des données sensibles

### Frontend
- **Jinja2** - Moteur de templates
- **Tailwind CSS** - Framework CSS moderne
- **JavaScript** - Interactions dynamiques

### Services Externes
- **SendGrid** - Envoi d'emails transactionnels
- **OpenRouter AI** - Analyse de CV et matching intelligent (Google Gemini 2.5 Flash)
- **OMDB API** - Recherche de films (optionnel)

### Traitement de Données
- **pandas** - Manipulation de données pour exports
- **openpyxl** - Génération de fichiers Excel
- **ReportLab** - Génération de PDF
- **Pillow** - Traitement d'images
- **PyPDF2** - Extraction de texte PDF
- **python-docx** - Extraction de texte DOCX
- **qrcode** - Génération de QR codes

---

## 📚 Documentation

### Pour les Utilisateurs
- **README.md** (ce fichier) - Vue d'ensemble et guide de démarrage
- **README.fr.md** - Version française
- **CHANGELOG.md** - Historique des versions et modifications

### Pour les Développeurs
- **[Documentation Technique](docs/TECHNICAL_DOCUMENTATION.md)** - Architecture, modèles, services, sécurité
- **[API Documentation EN](api_docs/API_DOCUMENTATION_EN.md)** - Documentation complète de l'API REST v1
- **[API Documentation FR](api_docs/API_DOCUMENTATION_FR.md)** - Version française de l'API

### Fichiers Techniques
- **config.py** - Configuration Flask
- **app/__init__.py** - Factory Flask et initialisation
- **app/constants.py** - Constantes globales

---

## 🔄 Mises à Jour et Maintenance

### Système de Mises à Jour Intégré

L'application inclut un système de mise à jour automatique :

1. **Vérification** : Depuis le dashboard admin → Paramètres → Section "Mises à jour"
2. **Application** : Clic sur "Appliquer la mise à jour"
3. **Historique** : Journal complet dans `logs/update_history.json`

### Migrations Automatiques

Le système détecte automatiquement les changements de schéma au démarrage :
- Ajout de colonnes manquantes
- Création de tables manquantes
- Conservation des données existantes
- Log des modifications dans la console

### Sauvegardes

**Recommandations** :
1. Effectuer une sauvegarde avant chaque mise à jour majeure
2. Sauvegardes régulières (quotidien/hebdomadaire selon l'activité)
3. Stockage des archives hors serveur
4. Test de restauration périodique

---

## 🌟 Cas d'Utilisation

### Pour les Talents
1. **Créer un profil complet** avec toutes les informations professionnelles
2. **Uploader un CV** pour analyse IA et extraction de compétences
3. **Générer un QR code** pour partager facilement son profil
4. **S'inscrire comme talent CINEMA** pour des opportunités audiovisuelles
5. **Mettre à jour ses informations** et disponibilités

### Pour les Recruteurs/Casteurs
1. **Rechercher des talents** par compétences, localisation, disponibilité
2. **Filtrer les talents CINEMA** par critères physiques et compétences
3. **Exporter des listes** de candidats en Excel/CSV/PDF
4. **Visualiser les profils complets** avec contacts chiffrés
5. **Créer des projets** et assigner des talents

### Pour les Administrateurs
1. **Gérer la base de talents** (activation, édition, suppression)
2. **Exporter des rapports** pour analyses
3. **Configurer les services** (email, IA, APIs)
4. **Créer des sauvegardes** régulières
5. **Mettre à jour l'application** en un clic
6. **Gérer les productions** et projets cinématographiques

---

## 🚀 Déploiement sur VPS

### Script de Déploiement Automatisé

Un script Bash complet (`deploy_vps.sh`) est fourni pour automatiser le déploiement sur VPS.

#### Prérequis VPS
- Ubuntu 20.04/22.04 ou Debian 11/12
- Python 3.11+
- PostgreSQL 14+ (ou utiliser SQLite)
- Git (optionnel, pour mises à jour automatiques)
- Accès sudo pour configuration Nginx/Systemd

#### Utilisation Rapide

```bash
# 1. Rendre le script exécutable
chmod +x deploy_vps.sh

# 2. (Optionnel) Configurer le dépôt Git
export GIT_REPO_URL="https://github.com/votre-compte/talentsmaroc.git"
export GIT_BRANCH="main"  # ou "production"

# 3. Lancer le déploiement
./deploy_vps.sh
```

#### Fonctionnalités du Script

Le script effectue automatiquement :

1. **Sauvegarde Automatique**
   - Dump PostgreSQL complet (inclus dans l'archive)
   - Tous les fichiers uploads (photos, CVs, QR codes)
   - Fichier .env (configuration)
   - Archive compressée avec horodatage

2. **Mise à Jour du Code**
   - Git pull depuis le dépôt distant (si configuré)
   - Ou utilisation des fichiers locaux
   - Gestion intelligente des conflits

3. **Configuration Python**
   - Création/activation de l'environnement virtuel
   - Installation de toutes les dépendances
   - Mise à jour de pip

4. **Base de Données**
   - Exécution des migrations
   - Initialisation des données de démonstration
   - Création des répertoires nécessaires

5. **Service Systemd** (optionnel)
   - Configuration du service auto-démarrage
   - Intégration avec Gunicorn
   - Gestion des logs

6. **Nginx Reverse Proxy** (optionnel)
   - Configuration complète
   - Support SSL/HTTPS (via Certbot)
   - Optimisations de performance

#### Variables d'Environnement

Le script supporte les variables suivantes :

| Variable | Description | Défaut |
|----------|-------------|--------|
| `GIT_REPO_URL` | URL du dépôt Git | (aucun - fichiers locaux) |
| `GIT_BRANCH` | Branche à déployer | `main` |

#### Exemple de Déploiement Complet

```bash
# Configuration
export GIT_REPO_URL="https://github.com/mycompany/talentsmaroc.git"
export GIT_BRANCH="production"

# Lancer le déploiement
./deploy_vps.sh

# Le script vous guidera à travers :
# 1. Sauvegarde de l'existant
# 2. Mise à jour du code
# 3. Installation des dépendances
# 4. Migrations de base de données
# 5. Configuration Systemd (optionnel)
# 6. Configuration Nginx (optionnel)
# 7. Démarrage de l'application
```

#### Commandes Systemd (après installation)

```bash
# Démarrer l'application
sudo systemctl start talentsmaroc

# Arrêter l'application
sudo systemctl stop talentsmaroc

# Redémarrer l'application
sudo systemctl restart talentsmaroc

# Voir le statut
sudo systemctl status talentsmaroc

# Voir les logs en temps réel
sudo journalctl -u talentsmaroc -f
```

#### Configuration SSL avec Let's Encrypt

Après avoir configuré Nginx, installez un certificat SSL gratuit :

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtenir et installer le certificat
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com

# Le renouvellement est automatique
```

#### Sauvegardes et Restauration

**Créer une sauvegarde manuelle** :
```bash
./deploy_vps.sh
# Choisir "Ne pas démarrer" à la fin
# La sauvegarde sera dans backups/backup_YYYYMMDD_HHMMSS.tar.gz
```

**Restaurer une sauvegarde** :
```bash
# 1. Extraire l'archive
cd backups
tar -xzf backup_20241026_143000.tar.gz

# 2. Restaurer la base de données
psql $DATABASE_URL < db_20241026_143000.sql

# 3. Restaurer les fichiers uploads
cp -r app/static/uploads/* ../app/static/uploads/

# 4. Redémarrer l'application
sudo systemctl restart talentsmaroc
```

#### Dépannage

**Le port 5004 est déjà utilisé** :
```bash
# Trouver le processus
lsof -i :5004

# Arrêter le processus
sudo kill -9 <PID>
```

**Erreur de connexion PostgreSQL** :
```bash
# Vérifier le service PostgreSQL
sudo systemctl status postgresql

# Vérifier DATABASE_URL dans .env
cat .env | grep DATABASE_URL
```

**Les modifications ne s'appliquent pas** :
```bash
# Forcer le redémarrage
sudo systemctl stop talentsmaroc
sudo systemctl start talentsmaroc

# Vérifier les logs
sudo journalctl -u talentsmaroc -n 100
```

---

## 🤝 Support et Contact

### Assistance Technique

Pour toute question ou problème :
- **Email** : moa@myoneart.com
- **Organisation** : MOA Digital Agency LLC
- **Site Web** : www.myoneart.com

### Signaler un Bug

Si vous rencontrez un problème :
1. Vérifiez les logs de l'application
2. Consultez la documentation technique
3. Contactez le support avec :
   - Description détaillée du problème
   - Étapes pour reproduire
   - Logs d'erreur (si disponibles)
   - Navigateur et système d'exploitation

### Demandes de Fonctionnalités

Les suggestions d'amélioration sont bienvenues ! Contactez-nous avec :
- Description de la fonctionnalité souhaitée
- Cas d'utilisation
- Bénéfices attendus

---

## 🔄 Guide de Mise à Jour

### Mise à Jour Sécurisée de l'Application

Ce guide explique comment mettre à jour taalentio.com **sans perdre vos données**.

#### 🛡️ Protection Automatique des Données

Le script `update_app.sh` protège automatiquement:

- ✅ **Configuration**: `.env` et toutes les variables d'environnement
- ✅ **Base de données**: SQLite (`.db`) et PostgreSQL
- ✅ **Fichiers uploadés**: Photos, CVs, QR codes
- ✅ **Logs**: Tous les fichiers de log
- ✅ **Sauvegardes**: Backups existants

#### 🚀 Méthode Simple (Recommandée)

**Mise à jour avec le script automatique:**

```bash
./update_app.sh
```

**Ce script va automatiquement:**
1. ✅ Sauvegarder toutes vos données
2. ✅ Mettre à jour le code (depuis Git si disponible)
3. ✅ Installer les nouvelles dépendances
4. ✅ Migrer le schéma de base de données
5. ✅ Vérifier l'intégrité de l'application
6. ✅ Créer une sauvegarde de restauration

#### 📋 Mise à Jour Manuelle (Avancée)

**Étape 1: Sauvegarde**

```bash
# Créer un répertoire de sauvegarde
mkdir -p backups

# Sauvegarder la base de données
cp talento.db backups/talento_$(date +%Y%m%d).db

# Sauvegarder la configuration
cp .env backups/.env_$(date +%Y%m%d)

# Sauvegarder les uploads
tar -czf backups/uploads_$(date +%Y%m%d).tar.gz app/static/uploads/
```

**Étape 2: Mettre à jour le code**

Option A - Depuis Git (VPS):
```bash
git stash save "Backup avant mise à jour"
git pull origin main
```

Option B - Upload manuel (Replit): Uploader les nouveaux fichiers sans remplacer `.env`, `*.db`, `app/static/uploads/`

**Étape 3: Mettre à jour les dépendances**

```bash
pip install -r requirements.txt --upgrade
```

**Étape 4: Migrer la base de données**

```bash
# Méthode automatique
python migrations_init.py

# Ou avec Flask-Migrate
flask db migrate -m "Update schema"
flask db upgrade
```

**Étape 5: Redémarrer l'application**

Sur Replit: Redémarrage automatique
Sur VPS avec systemd: `sudo systemctl restart talento`
Sur VPS avec PM2: `pm2 restart talento`

#### 🔒 Fichiers Protégés par .gitignore

Ces fichiers ne seront **JAMAIS** modifiés lors d'un `git pull`:

```
.env                          # Configuration (clés API, secrets)
*.db                          # Base de données SQLite
app/static/uploads/           # Tous les fichiers uploadés
backups/                      # Sauvegardes
*.tar.gz, *.sql              # Archives et dumps
```

#### ⚠️ En Cas de Problème

**Restaurer depuis une sauvegarde:**

```bash
# Lister les sauvegardes
ls -lh backups/

# Restaurer une sauvegarde spécifique
tar -xzf backups/backup_20251029_103000.tar.gz

# Ou restaurer la base de données uniquement
cp backups/talento_20251029.db talento.db
```

**Vérifier l'intégrité de l'application:**

```bash
# Tester l'import Python
python -c "from app import create_app; app = create_app(); print('OK')"

# Vérifier la base de données
python -c "from app import db; db.create_all(); print('OK')"
```

#### ✅ Checklist de Mise à Jour

Avant de mettre à jour:
- [ ] Sauvegarder la base de données
- [ ] Sauvegarder le fichier .env
- [ ] Vérifier l'espace disque disponible
- [ ] Noter la version actuelle

Après la mise à jour:
- [ ] Vérifier que l'application démarre
- [ ] Tester la connexion admin
- [ ] Vérifier que les uploads sont accessibles
- [ ] Tester une fonctionnalité critique

---

## 📜 Licence et Crédits

### Copyright

© 2024 taalentio.com. Tous droits réservés.

### Développement

**Par** : Aisance KALONJI  
**Pour** : MOA Digital Agency LLC  
**Contact** : moa@myoneart.com

### Remerciements

Merci à tous les contributeurs et utilisateurs qui font de taalentio.com une plateforme de référence pour les talents africains.

---

## 🎯 Vision et Roadmap

### Vision

Devenir **la plateforme de référence** pour la découverte et la gestion des talents africains, en particulier dans l'industrie cinématographique, en offrant des outils professionnels, sécurisés et innovants.

### Fonctionnalités Futures

- 🌐 **Internationalisation** : Support multilingue (Français, Anglais, Arabe)
- 🔔 **Notifications en Temps Réel** : WebSockets pour alertes instantanées
- 💬 **Messagerie Intégrée** : Communication directe entre talents et recruteurs
- 📱 **Application Mobile** : iOS et Android
- 🎥 **Vidéos de Présentation** : Upload et streaming de bandes démo
- 🤖 **IA Avancée** : Matching automatique talents-projets
- 📊 **Analytics Avancés** : Tableaux de bord détaillés
- 🔗 **Intégrations** : LinkedIn, Indeed, autres plateformes professionnelles
- ☁️ **Cloud Storage** : Stockage de fichiers volumineux (vidéos)
- 🏆 **Système de Notation** : Avis et recommandations

---

**taalentio.com - Valorisons les talents africains ensemble ! 🌍✨**
