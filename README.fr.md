# 🎭 TalentsMaroc.com

**La plateforme de centralisation des talents africains avec un focus sur l'industrie cinématographique**

TalentsMaroc.com est une application web professionnelle conçue pour centraliser et mettre en valeur les profils de talents à travers l'Afrique. La plateforme permet aux professionnels de créer des profils détaillés, de valoriser leurs compétences et de se connecter à des opportunités - avec un module dédié CINEMA pour l'industrie audiovisuelle.

[🇬🇧 English Version](README.md)

---

## ✨ Fonctionnalités Principales

### 🎬 Module CINEMA (Industrie Audiovisuelle)

**Le cœur de TalentsMaroc** - Un système complet dédié aux professionnels du cinéma et de l'audiovisuel:

#### Pour les Talents
- **Inscription Publique Complète** : Formulaire en 9 sections pour un profil détaillé
- **13 types de talents** : Acteur Principal, Acteur Secondaire, Figurant, Silhouette, Doublure, Doublure Lumière, Cascadeur, Mannequin, Voix Off, Figurant Spécialisé, Choriste, Danseur de fond, Autre
- **Profil Public avec QR Code** : Chaque talent dispose d'une page publique accessible via QR code
- **Carte PDF Professionnelle** : Génération automatique d'une carte talent imprimable
- **Recherche Avancée** : Filtrage par 12 critères (nom, type, genre, âge, ethnicité, caractéristiques physiques, langues, expérience)

#### Pour les Productions & Projets
- **Gestion des Boîtes de Production** : Profils complets avec équipements, studios, certifications
- **Système de Gestion de Projets** : Création de projets, assignation de talents, codes uniques PRJ-XXX-YYY
- **Génération de Badges PDF** : Badges personnalisés pour chaque talent assigné

### 👤 Profils Utilisateurs Standards

- **Inscription Multi-Étapes** guidée
- **Connexion Flexible** : Email OU code unique
- **Profils Complets** : Informations personnelles, contact chiffré, localisation (54 pays africains)
- **Talents Multiples** : Sélection parmi des dizaines de catégories
- **QR Code Personnel** généré automatiquement

### 🤖 Analyse IA de CV

**Propulsé par OpenRouter AI** (Llama 3.1 8B Instruct)
- Upload de CV (PDF, DOC, DOCX)
- Extraction automatique des compétences
- Score de profil (0-100)
- Recommandations personnalisées

### 🛠️ Administration Puissante

- **Dashboard Administrateur** : Vue d'ensemble, statistiques en temps réel
- **Gestion Complète** : Utilisateurs, talents, CINEMA, productions, projets
- **Exports** : Excel, CSV, PDF avec données déchiffrées
- **Paramètres Système** : Configuration des APIs (SendGrid, OpenRouter, TMDb)
- **Sauvegarde & Restauration** : Archives ZIP chiffrées complètes
- **Mises à Jour** : Système intégré avec vérification Git

### 📊 Statistiques Détaillées

- Statistiques globales (utilisateurs, répartition géographique, talents populaires)
- Statistiques CINEMA (13 types de talents, genres, pays, langues, expérience)

### 🔐 Sécurité & Confidentialité

- **Chiffrement Fernet** (AES 128-bit CBC) pour toutes les données sensibles
- **Hachage bcrypt** (12 rounds) pour les mots de passe
- **Protection CSRF** (Flask-WTF)
- **Upload Sécurisé** : Validation MIME, noms UUID, limites de taille

### 🌍 Couverture Africaine

- **54 pays africains** avec codes ISO-2
- **Villes principales** pré-remplies
- **Chargement dynamique** des villes selon le pays

### 🎨 Interface Moderne

- **Tailwind CSS** : Design responsive (mobile, tablette, desktop)
- **Navigation Intuitive** : Menu adaptatif selon le rôle
- **Dashboard Adaptatif** : Vue admin, utilisateur, ou CINEMA

### 📧 Emails Automatisés

- **SendGrid API** : Emails de confirmation, identifiants, notifications
- Configuration via interface admin

### 🔗 API REST v1

- **Authentification** : Session-based (cookies)
- **Endpoints Complets** : Utilisateurs, Talents, CINEMA, Statistiques, Exports
- **Documentation** : [API EN](api_docs/API_DOCUMENTATION_EN.md) | [API FR](api_docs/API_DOCUMENTATION_FR.md)

### 🎯 Codification Unique

- **Codes Standards** : PPGNNNNVVV (10 caractères, ex: MAM0001RAB) - Incrémentation par pays
- **Codes CINEMA** : PPVVVNNNNNG (11 caractères, ex: MACAS0001F) - Incrémentation par pays
- **Codes Projets** : CCIIISSSNNN (10+ caractères, ex: MAABC001001) - Sans tirets

**Distinction** : Les codes CINEMA et standards se distinguent par l'ordre des composants (Ville avant Numéro pour CINEMA, Genre avant Numéro pour standards).

---

## 🚀 Installation et Démarrage

### Prérequis

- Python 3.11+
- PostgreSQL 14+ (ou SQLite pour développement)
- Git

### Installation Rapide

```bash
# 1. Cloner le repository
git clone <repository-url>
cd talentsmaroc

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer .env
SECRET_KEY=votre-cle-secrete
DATABASE_URL=postgresql://user:password@localhost:5432/talentsmaroc
ENCRYPTION_KEY=votre-cle-chiffrement-base64

# 4. Initialiser la base de données
python migrations_init.py

# 5. Lancer l'application
python app.py
```

L'application sera accessible sur `http://localhost:5000`

### Comptes par Défaut

**Administrateur** :
- Email: `admin@talento.com`
- Code: `MARAB0001N`
- Mot de passe: `@4dm1n`

**Démonstration** :
- `demo1@talento.com` à `demo5@talento.com` (mot de passe: `demo123`)
- 3 talents CINEMA (emails `@demo.cinema`)
- 2 productions (Morocco Films, Atlas Studios)

---

## 📂 Structure du Projet

```
talentsmaroc/
├── app/
│   ├── models/          # Modèles SQLAlchemy (User, CinemaTalent, Production, Project, etc.)
│   ├── routes/          # Blueprints (auth, profile, admin, cinema, api_v1)
│   ├── services/        # Logique métier (CV analyzer, exports, email, backup)
│   ├── templates/       # Templates Jinja2
│   ├── static/          # CSS, JS, images, uploads
│   └── utils/           # Utilitaires (encryption, ID generators, QR codes)
├── api_docs/            # Documentation API (EN, FR)
├── docs/                # Documentation technique
│   └── TECHNICAL_DOCUMENTATION.md
├── app.py               # Point d'entrée
├── config.py            # Configuration
├── migrations_init.py   # Initialisation DB
├── requirements.txt     # Dépendances
├── README.md            # Documentation anglais
├── README.fr.md         # Ce fichier
└── CHANGELOG.md         # Journal des modifications
```

---

## 🛠️ Technologies

### Backend
- **Flask 3.0.0**, **SQLAlchemy**, **Flask-Login**, **bcrypt**, **cryptography (Fernet)**

### Frontend
- **Jinja2**, **Tailwind CSS**, **JavaScript**

### Services Externes
- **SendGrid** (emails), **OpenRouter AI** (analyse CV), **TMDb API** (films, optionnel)

### Traitement
- **pandas**, **openpyxl** (Excel), **ReportLab** (PDF), **Pillow**, **qrcode**

---

## 📚 Documentation

### Utilisateurs
- **README.fr.md** (ce fichier) - Vue d'ensemble
- **CHANGELOG.md** - Historique des versions

### Développeurs
- **[Documentation Technique](docs/TECHNICAL_DOCUMENTATION.md)** - Architecture complète
- **[API EN](api_docs/API_DOCUMENTATION_EN.md)** | **[API FR](api_docs/API_DOCUMENTATION_FR.md)**

---

## 🌟 Cas d'Utilisation

### Pour les Talents
- Créer un profil complet avec CV et analyse IA
- Générer un QR code pour partage facile
- S'inscrire comme talent CINEMA pour opportunités audiovisuelles

### Pour les Recruteurs
- Rechercher des talents par compétences, localisation, disponibilité
- Filtrer les talents CINEMA par critères physiques et compétences
- Exporter des listes en Excel/CSV/PDF
- Créer des projets et assigner des talents

### Pour les Administrateurs
- Gérer la base complète de talents
- Configurer les services (email, IA, APIs)
- Créer des sauvegardes régulières
- Mettre à jour l'application en un clic

---

## 🤝 Support

**Email** : moa@myoneart.com  
**Organisation** : MOA Digital Agency LLC  
**Site Web** : www.myoneart.com

---

## 📜 Licence

© 2024 TalentsMaroc.com. Tous droits réservés.

**Développement** : Aisance KALONJI | MOA Digital Agency LLC

---

## 🎯 Vision

Devenir **la plateforme de référence** pour la découverte et la gestion des talents africains, en particulier dans l'industrie cinématographique.

### Roadmap Future
- 🌐 Internationalisation (FR, EN, AR)
- 🔔 Notifications temps réel (WebSockets)
- 💬 Messagerie intégrée
- 📱 Application mobile (iOS, Android)
- 🎥 Vidéos de présentation
- 🤖 Matching IA talents-projets
- 🔗 Intégrations LinkedIn, Indeed

---

**TalentsMaroc.com - Valorisons les talents africains ensemble ! 🌍✨**
