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
- **Mot de passe**: admin123
- **Code unique**: MARAB0001N

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

## 🌐 Configuration Email

Pour activer les emails de confirmation:
1. Configurer les variables d'environnement:
   - MAIL_SERVER
   - MAIL_PORT
   - MAIL_USERNAME
   - MAIL_PASSWORD
2. Utiliser un service SMTP (Gmail, SendGrid, etc.)

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

## 🎯 État actuel

Le projet est fonctionnel avec les fonctionnalités de base :
- ✅ Inscription utilisateur complète
- ✅ Authentification
- ✅ Génération codes/QR
- ✅ Dashboard utilisateur
- ✅ Dashboard admin
- ✅ Base de données seedée

**Prêt pour**: Inscription de nouveaux talents et consultation des profils.
