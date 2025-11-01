# Changelog - taalentio.com

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).

## [Non publié]

### Ajouté
- **Icônes Font Awesome pour les réseaux sociaux** : Remplacement de tous les emojis des réseaux sociaux par de vraies icônes Font Awesome 6.5.1 pour une apparence plus professionnelle
  - Icônes dans le footer du site
  - Icônes dans le formulaire d'administration des réseaux sociaux
  - Icônes dans l'aperçu des réseaux sociaux configurés

### Modifié
- **Mentions légales enrichies** : Ajout de deux nouveaux champs
  - `company_whatsapp` : Contact WhatsApp de l'entreprise (section Coordonnées) avec lien cliquable
  - `director_role` : Rôle/poste du directeur de publication (section Direction)
  - Total de 14 champs organisés en 4 blocs pour les mentions légales

## [1.0.0] - 2025-11-01

### Architecture validée

#### ✅ Formulaires d'inscription
- **Talent classique** (`/auth/register`)
  - Tous les champs correctement enregistrés (identité, localisation, réseaux sociaux, documents)
  - Upload de photo et CV avec analyse automatique par IA
  - Validation email et téléphone avec normalisation E.164
  - Génération automatique code unique (format PPGNNNNVVV) et QR code
  - Envoi d'emails de confirmation et identifiants de connexion

- **Talent CINEMA** (`/cinema/register`)
  - Tous les champs correctement enregistrés (caractéristiques physiques, documents cryptés)
  - Upload photos multiples (profil, ID, galerie)
  - Validation et cryptage des données sensibles (téléphone, WhatsApp, réseaux sociaux)
  - Génération automatique code CINEMA (format PPVVVNNNNNG) et QR code
  - Création automatique compte User associé
  - Envoi d'emails de confirmation et identifiants

#### ✅ Génération de codes uniques
- **Talent classique** : Format PPGNNNNVVV (ex: MAM0001RAB)
  - PP: Code pays ISO-2 (2 lettres)
  - G: Genre (M/F/N)
  - NNNN: Numéro séquentiel par pays (4 chiffres)
  - VVV: Code ville (3 lettres)
  - Vérification d'unicité avec gestion de conflits

- **Talent CINEMA** : Format PPVVVNNNNNG (ex: MACAS0001F)
  - PP: Code pays ISO-2 (2 lettres)
  - VVV: Code ville (3 lettres)
  - NNNN: Numéro séquentiel par pays (4 chiffres)
  - G: Genre (M/F)
  - Rétrocompatibilité avec ancien format

#### ✅ Génération de QR codes
- Support multi-environnement (Replit, VPS, local)
- QR codes pour profils users et CINEMA
- URL dynamiques selon l'environnement
- Génération en mémoire pour les PDFs

#### ✅ Export PDF
- Logo `logo-full.png` correctement intégré en en-tête
- Formats : Liste de talents (paysage), profil individuel
- QR codes générés dynamiquement dans les PDFs
- Support Excel et CSV également

#### ✅ Service d'emails
- **Fonctions disponibles** :
  - Confirmation d'inscription (send_application_confirmation)
  - Envoi identifiants de connexion (send_login_credentials)
  - Notifications matching IA (send_ai_match_notification, send_cinema_ai_match_notification)
  - Confirmation sélection projet (send_project_selection_confirmation)
  - Récapitulatif hebdomadaire admin (send_weekly_admin_recap)
  - Notifications watchlist (send_watchlist_notification, send_name_detection_notification)
  - Email de test (send_test_email)
- Intégration SendGrid avec templates HTML professionnels
- Support des pièces jointes (PDFs, documents)
- Tracking des emails envoyés en base de données

### Fonctionnalités principales

#### Système d'authentification
- Login dual : email OU code unique
- Validation d'email avec vérification de délivrabilité
- Validation de téléphone avec format E.164
- Système de rôles (Admin, Recruteur, Présence, User)

#### Gestion des talents
- Profils complets avec 18+ réseaux sociaux
- Upload et analyse automatique de CV par IA
- Score de profil automatique
- Système de talents multiples assignables
- QR codes uniques pour chaque profil

#### Module CINEMA
- Caractéristiques physiques détaillées
- Système de cryptage des données sensibles
- Galerie de photos
- Types de talents multiples
- Productions précédentes
- Système de projets et castings

#### Intelligence Artificielle
- Analyse automatique de CV
- Matching talent-offre par IA
- Support multi-providers (OpenRouter, Perplexity, OpenAI, Gemini)
- Sélection de modèle par provider

#### Exports et rapports
- Excel (XLSX) avec colonnes auto-ajustées
- CSV
- PDF avec logo et QR codes

#### Communication
- Emails transactionnels automatiques
- Récapitulatif hebdomadaire admin
- Système de watchlist avec notifications
- Détection de noms surveillés

### Technologies

#### Backend
- Flask 3.0.0 (Python 3.11)
- SQLAlchemy (PostgreSQL/SQLite)
- APScheduler pour tâches planifiées
- Cryptography (Fernet) pour données sensibles

#### Frontend
- Tailwind CSS (CDN)
- Font Awesome 6.5.1
- JavaScript vanilla

#### Services externes
- SendGrid (emails)
- Diverses APIs IA
- OMDB (films pour CINEMA)

### Sécurité
- Cryptage Fernet pour données sensibles
- Hashing bcrypt pour mots de passe
- Validation email avec vérification DNS
- Validation téléphone internationale
- Système de logs d'activité et sécurité
- CSRF protection

---

## Légende des symboles

- ✅ **Validé et fonctionnel**
- ➕ **Ajouté**
- ✏️ **Modifié**
- 🗑️ **Supprimé**
- 🔧 **Correction**
- 📝 **Documentation**
- 🔒 **Sécurité**
