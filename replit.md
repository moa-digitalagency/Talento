# Talento - Plateforme de Centralisation des Talents

## 📋 Vue d'ensemble

Talento est une application web de gestion de profils de talents permettant aux utilisateurs de centraliser leurs compétences, CV, portfolios et informations de contact en un seul endroit. Chaque profil génère automatiquement un code unique et un QR code pour faciliter le partage.

## 🏗️ Architecture

### Backend
- **Framework**: Flask (Python 3.11)
- **ORM**: SQLAlchemy avec Flask-SQLAlchemy
- **Base de données**: PostgreSQL (Helium - Replit)
- **Authentification**: Flask-Login
- **Migrations**: Flask-Migrate (Alembic)
- **Email**: Flask-Mail

### Frontend
- **Templates**: Jinja2 (HTML)
- **CSS**: Tailwind CSS 3.4
- **Build**: npm/Tailwind CLI

## 📁 Structure du projet

```
talento/
├── app/
│   ├── __init__.py           # Application factory
│   ├── models/               # Modèles de base de données
│   │   ├── user.py          # Modèle User
│   │   ├── talent.py        # Modèles Talent et UserTalent
│   │   └── location.py      # Modèles Country et City
│   ├── routes/              # Routes/Controllers
│   │   ├── main.py          # Routes principales
│   │   ├── auth.py          # Authentification
│   │   ├── profile.py       # Profils utilisateur
│   │   ├── admin.py         # Administration
│   │   └── api.py           # API endpoints
│   ├── templates/           # Templates HTML
│   ├── static/              # Fichiers statiques
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/         # Fichiers uploadés
│   └── utils/               # Utilitaires
│       ├── id_generator.py  # Génération codes uniques
│       ├── qr_generator.py  # Génération QR codes
│       ├── email_service.py # Service email
│       └── file_handler.py  # Gestion fichiers
├── app.py                    # Point d'entrée
├── config.py                 # Configuration
├── seed_data.py             # Données initiales
└── requirements.txt         # Dépendances Python
```

## 🚀 Fonctionnalités

### Utilisateur
- ✅ Inscription avec formulaire complet
- ✅ Upload photo de profil et CV
- ✅ Sélection multiple de talents (avec emojis)
- ✅ Génération code unique (format: PP-VVV-NNNN-G)
- ✅ Génération QR code personnel
- ✅ Email de confirmation avec mot de passe
- ✅ Espace personnel pour consulter le profil
- 🚧 Modification du profil (en cours)

### Admin
- ✅ Dashboard administrateur
- ✅ Liste de tous les talents
- ✅ Recherche et filtres basiques
- 🚧 Exports (Excel, CSV, PDF) - à implémenter
- 🚧 Filtres avancés - à implémenter

## 🔑 Informations importantes

### Compte Admin par défaut
- **Email**: admin@talento.app
- **Mot de passe**: Configurable via variable d'environnement `ADMIN_PASSWORD` (défaut: admin123 en développement)
- **Code unique**: MARAB0001N
- **⚠️ IMPORTANT**: En production, définir la variable d'environnement `ADMIN_PASSWORD` avec un mot de passe sécurisé

### Format du code unique
```
PP-VVV-NNNN-G
PP    : 2 lettres du pays (ex: MA, FR, SN)
VVV   : 3 lettres de la ville au Maroc (ex: RAB, CAS, TNG)
NNNN  : 4 chiffres aléatoires
G     : Genre (M/F/N)
Exemple: MA-CAS-4821-F
```

### Base de données
- PostgreSQL sur Replit (Helium)
- Tables: users, talents, user_talents, countries, cities
- Migrations gérées via Flask-Migrate

## 🛠️ Développement

### Démarrer l'application
L'application démarre automatiquement via le workflow "Talento Web App".
Port: 5000 (0.0.0.0:5000)

### Rebuild CSS
```bash
npm run build:css
```

### Migrations
```bash
flask db init        # Initialiser (fait)
flask db migrate     # Créer migration
flask db upgrade     # Appliquer migration
```

### Seed data
La base de données est automatiquement initialisée au démarrage de l'application avec:
- 54 pays africains
- 12 villes marocaines
- 74 talents organisés en 14 catégories
- Compte administrateur (si ADMIN_PASSWORD est défini)

Le seeding est **idempotent** : il ne duplique pas les données existantes.

Pour réinitialiser manuellement:
```bash
python seed_data.py
```

## 📊 Modèle de données

### User
- Informations personnelles (nom, prénom, email, etc.)
- Coordonnées (téléphone, WhatsApp, adresse)
- Origine (pays, ville au Maroc)
- Médias (photo, CV, portfolio)
- Réseaux sociaux
- Code unique et QR code
- Relations: talents (many-to-many)

### Talent
- Nom et emoji
- Catégorie
- Relation: users (many-to-many via user_talents)

### Country & City
- Codes et noms pour la génération des codes uniques

## 🔒 Sécurité

- ✅ Hashage mots de passe (bcrypt)
- ✅ Validation formats fichiers
- ✅ Limites taille fichiers (photo: 5MB, CV: 10MB)
- ✅ Emails uniques
- ✅ Protection routes admin
- 🚧 CAPTCHA - à implémenter
- 🚧 Scan antivirus - à implémenter

## 📝 TODO / Améliorations futures

1. **Haute priorité**
   - Implémentation modification de profil
   - Exports admin (Excel, CSV, PDF)
   - CAPTCHA à l'inscription
   - Validation avancée des fichiers
   - Changement de mot de passe

2. **Moyenne priorité**
   - Filtres avancés admin
   - Recherche par QR code
   - Notifications email admin
   - Gestion des disponibilités
   - Upload portfolio files

3. **Basse priorité**
   - Dashboard statistiques
   - API REST pour mobile
   - Multi-langue
   - Thème sombre
   - Export profil individuel PDF

## 🌐 Configuration

### Variables d'environnement

**Production (obligatoire):**
- `ADMIN_PASSWORD`: Mot de passe sécurisé pour le compte admin (⚠️ Ne jamais utiliser le défaut 'admin123' en production)

**Email (optionnel):**
- `MAIL_SERVER`: Serveur SMTP
- `MAIL_PORT`: Port SMTP
- `MAIL_USERNAME`: Nom d'utilisateur SMTP
- `MAIL_PASSWORD`: Mot de passe SMTP

Utiliser un service SMTP (Gmail, SendGrid, etc.) pour les emails de confirmation.

## 📦 Technologies utilisées

**Backend**:
- Flask 3.0
- SQLAlchemy 2.0
- Flask-Login, Flask-Mail, Flask-Migrate
- Pillow (images)
- qrcode (QR codes)
- pandas, openpyxl, reportlab (exports)

**Frontend**:
- Tailwind CSS 3.4
- Vanilla JavaScript
- Jinja2 templates

## 🔧 Configuration Replit

- Port: 5000
- Host: 0.0.0.0 (requis pour Replit proxy)
- Database: PostgreSQL (Helium)
- Workflow: "Talento Web App" (python app.py)

## 📅 Historique

- **18/10/2025**: Création initiale du projet
  - Setup Flask + PostgreSQL
  - Modèles de base de données
  - Système d'inscription
  - Génération codes et QR codes
  - Interface admin basique
  - Tailwind CSS intégré
  - **AMÉLIORATION**: Design coloré avec sections (Identité, Contact, Localisation, Talents, Documents, Réseaux sociaux)
  - **AMÉLIORATION**: 54 pays africains avec drapeaux emoji
  - **AMÉLIORATION**: 90+ talents organisés par 11 catégories
  - **AMÉLIORATION**: Limite de 5 talents maximum
  - **AMÉLIORATION**: Redirection automatique vers inscription depuis page d'accueil
  - **AMÉLIORATION**: Seeding automatique de la base de données au démarrage (idempotent)
  - **AMÉLIORATION**: Style outline pour les icônes de sections (bordures colorées au lieu de fonds pleins)
  - **AMÉLIORATION**: Support de la variable d'environnement ADMIN_PASSWORD pour sécuriser le compte admin

## 🎯 État actuel

Le projet est fonctionnel avec les fonctionnalités de base :
- ✅ Inscription utilisateur complète avec design coloré et sections organisées
- ✅ Style outline pour les icônes de sections (bordures colorées)
- ✅ 54 pays africains avec drapeaux
- ✅ 74 talents organisés en 14 catégories (Construction, Restauration, Technologie, Créatif, Médias, Marketing, Artistique, Services, Transport, Éducation, Santé, Commerce, Événementiel, Bureautique)
- ✅ Limite de 5 talents maximum avec compteur en temps réel
- ✅ Authentification
- ✅ Génération codes/QR
- ✅ Dashboard utilisateur
- ✅ Dashboard admin
- ✅ Base de données seedée automatiquement au démarrage
- ✅ Configuration sécurisée via variables d'environnement

**Prêt pour**: Inscription de nouveaux talents et consultation des profils.

## 🌍 Pays africains disponibles

54 pays africains sont disponibles dans la liste avec leurs drapeaux emoji :
Maroc 🇲🇦, Algérie 🇩🇿, Tunisie 🇹🇳, Libye 🇱🇾, Égypte 🇪🇬, Mauritanie 🇲🇷, Mali 🇲🇱, Sénégal 🇸🇳, Gambie 🇬🇲, Guinée-Bissau 🇬🇼, Guinée 🇬🇳, Sierra Leone 🇸🇱, Liberia 🇱🇷, Côte d'Ivoire 🇨🇮, Ghana 🇬🇭, Togo 🇹🇬, Bénin 🇧🇯, Nigéria 🇳🇬, Niger 🇳🇪, Burkina Faso 🇧🇫, Cameroun 🇨🇲, Tchad 🇹🇩, République Centrafricaine 🇨🇫, Guinée Équatoriale 🇬🇶, Gabon 🇬🇦, Congo 🇨🇬, RD Congo 🇨🇩, Angola 🇦🇴, Soudan 🇸🇩, Soudan du Sud 🇸🇸, Éthiopie 🇪🇹, Érythrée 🇪🇷, Djibouti 🇩🇯, Somalie 🇸🇴, Kenya 🇰🇪, Ouganda 🇺🇬, Rwanda 🇷🇼, Burundi 🇧🇮, Tanzanie 🇹🇿, Malawi 🇲🇼, Mozambique 🇲🇿, Zimbabwe 🇿🇼, Zambie 🇿🇲, Botswana 🇧🇼, Namibie 🇳🇦, Afrique du Sud 🇿🇦, Lesotho 🇱🇸, Eswatini 🇸🇿, Madagascar 🇲🇬, Maurice 🇲🇺, Comores 🇰🇲, Seychelles 🇸🇨, Cap-Vert 🇨🇻, São Tomé-et-Príncipe 🇸🇹

## ⭐ Catégories de talents

11 catégories avec 90+ talents :
1. **Construction** (12 talents) : Maçonnerie, Carrelage, Plomberie, Électricité, Menuiserie, Peinture, Soudure, Ferronnerie, Charpenterie, Toiture, Isolation, Climatisation
2. **Restauration** (6 talents) : Cuisine, Pâtisserie, Boulangerie, Serveur, Barista, Chef cuisine
3. **Technologie** (8 talents) : Développement Web, Développement Mobile, Data Science, IA/ML, Cybersécurité, DevOps, Maintenance IT, Réseaux
4. **Créatif** (5 talents) : Graphisme, UI/UX Design, Illustration, Animation 3D, Motion Design
5. **Médias** (5 talents) : Photographie, Vidéographie, Montage vidéo, Rédaction, Journalisme
6. **Marketing** (5 talents) : Community Management, SEO/SEA, Marketing digital, Content Marketing, Email Marketing
7. **Artistique** (6 talents) : Musique, Chant, Danse, Théâtre, Mannequinat, Comédie
8. **Services** (6 talents) : Ménage, Jardinage, Garde d'enfants, Aide à domicile, Coiffure, Esthétique
9. **Transport** (3 talents) : Chauffeur, Livreur, Taxi
10. **Éducation** (4 talents) : Enseignant, Formation professionnelle, Cours particuliers, Coaching
11. **Santé** (3 talents) : Infirmier, Aide-soignant, Pharmacien
12. **Commerce** (3 talents) : Vente, Commerce, Caissier
13. **Événementiel** (3 talents) : Organisation événements, Animation, DJ
14. **Bureautique** (4 talents) : Secrétariat, Comptabilité, Ressources Humaines, Gestion de projet
