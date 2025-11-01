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

---

## Système de Notifications Email

### Architecture EmailService

**Classe** : `EmailService` (app/services/email_service.py)

**Powered by** : SendGrid API

#### Configuration

```python
class EmailService:
    def __init__(self, api_key=None, from_email=None):
        # Priorise AppSettings puis variables d'environnement
        self.api_key = api_key or AppSettings.get('sendgrid_api_key') or os.environ.get('SENDGRID_API_KEY')
        self.from_email = from_email or AppSettings.get('sender_email') or os.environ.get('SENDGRID_FROM_EMAIL')
```

**Variables d'Environnement** :
- `SENDGRID_API_KEY` : Clé API SendGrid
- `SENDGRID_FROM_EMAIL` : Email expéditeur (ex: noreply@talento.com)

**Configuration Alternative** :
- Table `app_settings` avec clés `sendgrid_api_key` et `sender_email`
- Mise à jour en temps réel sans redémarrage

#### Modèle EmailLog

**Table** : `email_logs`

```python
class EmailLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_email = db.Column(db.String(255), nullable=False, index=True)
    recipient_name = db.Column(db.String(255))
    subject = db.Column(db.String(500), nullable=False)
    template_type = db.Column(db.String(100), nullable=False, index=True)
    html_content = db.Column(db.Text)
    status = db.Column(db.String(50), default='sent', index=True)
    error_message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    sent_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relations optionnelles
    related_talent_code = db.Column(db.String(50))
    related_project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    related_cinema_talent_id = db.Column(db.Integer, db.ForeignKey('cinema_talents.id'))
```

**Indexes** :
- `recipient_email` : Recherche par destinataire
- `template_type` : Filtrage par type
- `status` : Filtrage par statut
- `sent_at` : Tri chronologique

#### Méthodes du Service

**1. Envoi d'Email avec Logging**

```python
def send_email(self, to_email, subject, html_content, attachments=None, 
               template_type='generic', recipient_name=None, sent_by_user_id=None,
               related_talent_code=None, related_project_id=None, 
               related_cinema_talent_id=None):
    """
    Envoie un email via SendGrid avec logging automatique
    Vérifie si le template est activé avant envoi
    """
```

**Fonctionnalités** :
- Vérification de l'activation du template
- Gestion des attachments (PDF, images)
- Logging automatique en base
- Gestion d'erreurs robuste
- Retry en cas d'échec temporaire

**2. Notification de Match IA - Talents**

```python
def send_ai_match_notification(self, user, job_description, match_score, 
                                match_reason, sent_by_user_id=None):
    """
    Envoie une notification quand un profil match une recherche IA
    
    Args:
        user: Objet User
        job_description: Description du poste
        match_score: Score (0-100)
        match_reason: Raison du match
        sent_by_user_id: ID de l'utilisateur ayant lancé la recherche
    """
```

**Template** : `ai_talent_match`

**Contenu** :
- Score de correspondance avec badge coloré
- Description de l'opportunité (max 500 chars)
- Raisons détaillées du match
- Lien direct vers profil public
- Logo en base64 intégré

**3. Notification de Match IA - Cinéma**

```python
def send_cinema_ai_match_notification(self, cinema_talent, role_description, 
                                       match_score, match_reason, sent_by_user_id=None):
    """
    Notification pour profils cinéma matchés
    """
```

**Template** : `ai_cinema_match`

**Spécificités** :
- Design rouge/cinéma
- Lien vers profil cinéma complet
- Mention du score de casting

**4. Confirmation de Sélection Projet**

```python
def send_project_selection_confirmation(self, project_talent, sent_by_user_id=None):
    """
    Email de félicitations pour sélection dans un projet
    
    Args:
        project_talent: Objet ProjectTalent avec relations
        sent_by_user_id: ID de l'envoyeur
    """
```

**Template** : `project_selection`

**Contenu** :
- Détails du projet (nom, production, statut)
- Rôle assigné et description
- Coordonnées de la production (téléphone, email, adresse)
- Liens vers profil et badge téléchargeable
- Message de félicitations

#### Intégrations avec Routes

**1. Recherche IA de Talents** (`/ai-search`)

```python
# Après AIMatchingService.analyze_job_description()
for candidate in results.get('candidates', []):
    user = User.query.filter_by(unique_code=candidate.get('code')).first()
    if user and user.email:
        email_service.send_ai_match_notification(
            user=user,
            job_description=job_description,
            match_score=candidate.get('score', 0),
            match_reason=candidate.get('reason', ''),
            sent_by_user_id=current_user.id
        )
```

**2. Recherche IA Cinéma** (`/cinema/ai-search`)

```python
# Après AIMatchingService.analyze_cinema_talents()
for candidate in results.get('candidates', []):
    cinema_talent = CinemaTalent.query.filter_by(unique_code=candidate.get('code')).first()
    if cinema_talent and cinema_talent.email:
        email_service.send_cinema_ai_match_notification(
            cinema_talent=cinema_talent,
            role_description=job_description,
            match_score=candidate.get('score', 0),
            match_reason=candidate.get('reason', ''),
            sent_by_user_id=current_user.id
        )
```

**3. Envoi Emails Projet** (`/cinema/projects/<id>/send-selection-emails`)

```python
@bp.route('/projects/<int:project_id>/send-selection-emails', methods=['POST'])
@login_required
def send_project_selection_emails(project_id):
    """Envoie emails de confirmation à tous les talents du projet"""
    project_talents = ProjectTalent.query.filter_by(project_id=project_id).all()
    
    for project_talent in project_talents:
        email_service.send_project_selection_confirmation(
            project_talent=project_talent,
            sent_by_user_id=current_user.id
        )
```

#### Templates Email Additionnels

**5. Inscription Talent Standard**

```python
def send_application_confirmation(self, user, profile_pdf_path=None):
    """
    Envoie un email de confirmation d'inscription talent standard
    
    Args:
        user: Objet User
        profile_pdf_path: Chemin du PDF de profil (optionnel)
    """
```

**Template** : `talent_registration`

**Contenu** :
- Message de bienvenue personnalisé
- Code unique attribué
- Lien vers le profil public
- Instructions de prochaines étapes

**6. Inscription Talent Cinéma**

**Template** : `cinema_talent_registration`

**Contenu** :
- Confirmation d'enregistrement CINEMA
- Code unique CINEMA (format: PPVVVNNNNNG)
- Lien vers profil cinéma public
- Accès aux fonctionnalités CINEMA

**7. Identifiants de Connexion**

```python
def send_login_credentials(self, user, password):
    """
    Envoie les identifiants de connexion pour un nouveau compte
    
    Args:
        user: Objet User
        password: Mot de passe temporaire en clair
    """
```

**Template** : `login_credentials`

**Contenu** :
- Code unique d'identification
- Mot de passe temporaire
- Lien de connexion direct
- Recommandations de sécurité
- Alerte pour changer le mot de passe

**8. Récapitulatif Hebdomadaire - Talents**

```python
def send_weekly_admin_recap(self, admin_email, sent_by_user_id=None):
    """
    Envoie le récapitulatif hebdomadaire des nouvelles inscriptions
    Envoie 2 emails séparés : un pour les talents, un pour les talents cinéma
    
    Args:
        admin_email: Email de l'admin
        sent_by_user_id: ID de l'utilisateur (optionnel)
    
    Returns:
        dict avec les résultats des envois
    """
```

**Template** : `weekly_recap_talents`

**Déclenchement** : Automatique chaque dimanche à 12:59 PM via APScheduler

**Contenu** :
- Nombre de nouveaux talents inscrits (7 derniers jours)
- Tableau détaillé avec nom, code, ville, pays, date
- Liens directs vers chaque profil
- Design bleu avec bordures pointillées

**9. Récapitulatif Hebdomadaire - Talents Cinéma**

**Template** : `weekly_recap_cinema`

**Déclenchement** : Automatique chaque dimanche à 12:59 PM via APScheduler

**Contenu** :
- Nombre de nouveaux talents cinéma inscrits (7 derniers jours)
- Tableau détaillé avec nom, code, ville, pays, date
- Liens directs vers chaque profil CINEMA
- Design rouge/rose avec bordures pointillées

**9. Détection de Nom Surveillé**

```python
def send_name_detection_notification(self, notification_email, tracked_name, 
                                      match_data, sent_by_user_id=None):
    """
    Envoie une notification lors de la détection d'un nom surveillé
    
    Args:
        notification_email: Email où envoyer la notification
        tracked_name: Nom qui était surveillé
        match_data: Dictionnaire avec informations de la correspondance
            - registered_name: Nom tel qu'enregistré
            - unique_code: Code unique du talent
            - talent_type: 'talent' ou 'cinema'
            - email: Email du talent
            - city: Ville
            - country: Pays
            - tracking_description: Note de surveillance
        sent_by_user_id: ID de l'utilisateur (optionnel)
    """
```

**Template** : `name_detection`

**Contenu** :
- Alerte de correspondance avec nom surveillé
- Nom surveillé vs nom enregistré
- Informations complètes (code, type, email, localisation)
- Note de surveillance associée
- Lien direct vers le profil
- Design rouge avec alerte visuelle

---

#### Planificateur de Tâches (APScheduler)

**Fichier** : `app/scheduler.py`

**Configuration** :

```python
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = BackgroundScheduler({
    'apscheduler.timezone': 'Africa/Casablanca'
})
```

**Tâches Planifiées** :

```python
# Récapitulatif hebdomadaire - Tous les dimanches à 12:59 PM
scheduler.add_job(
    func=send_weekly_recap,
    trigger=CronTrigger(day_of_week='sun', hour=12, minute=59),
    id='weekly_recap',
    name='Récapitulatif Hebdomadaire Admin',
    replace_existing=True
)
```

**Fonction send_weekly_recap** :

```python
def send_weekly_recap():
    """
    Envoie le récapitulatif hebdomadaire à l'admin
    Appelé tous les dimanches à 12:59 PM
    """
    from app.models.settings import AppSettings
    from app.services.email_service import email_service
    
    # Récupère l'email admin depuis app_settings.admin_notification_email
    admin_email = AppSettings.get('admin_notification_email')
    
    # Envoie 2 emails séparés (talents + cinema)
    results = email_service.send_weekly_admin_recap(admin_email)
```

**Statut du Scheduler** :

```python
def get_scheduler_status():
    """Retourne le statut du scheduler et ses tâches"""
    return {
        'running': scheduler.running,
        'jobs': [
            {
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time,
                'trigger': str(job.trigger)
            }
            for job in scheduler.get_jobs()
        ]
    }
```

**Déclenchement Manuel** :

```python
def trigger_weekly_recap_now():
    """Déclenche manuellement le récapitulatif (pour test)"""
    send_weekly_recap()
    return {'success': True, 'message': 'Récapitulatif déclenché'}
```

#### Configuration des Templates

**Table** : `app_settings`
**Clé** : `email_notifications_config`

**Liste Complète des Templates** :

```json
{
  "talent_registration": {
    "enabled": true,
    "name": "Inscription Talent",
    "description": "Email envoyé après l'inscription d'un nouveau talent"
  },
  "cinema_talent_registration": {
    "enabled": true,
    "name": "Inscription Talent Cinéma",
    "description": "Email envoyé après l'inscription d'un nouveau talent cinéma"
  },
  "ai_talent_match": {
    "enabled": true,
    "name": "Match IA - Talents",
    "description": "Notification envoyée aux talents lorsque leur profil correspond à une recherche IA"
  },
  "ai_cinema_match": {
    "enabled": true,
    "name": "Match IA - Cinéma",
    "description": "Notification envoyée aux talents cinéma lorsque leur profil correspond à un rôle"
  },
  "project_selection": {
    "enabled": true,
    "name": "Sélection Projet",
    "description": "Email de confirmation envoyé aux talents sélectionnés pour un projet"
  },
  "login_credentials": {
    "enabled": true,
    "name": "Identifiants de Connexion",
    "description": "Email contenant les identifiants de connexion"
  },
  "weekly_recap_talents": {
    "enabled": true,
    "name": "Récapitulatif Hebdomadaire - Talents",
    "description": "Email récapitulatif des nouvelles inscriptions de talents envoyé chaque dimanche"
  },
  "weekly_recap_cinema": {
    "enabled": true,
    "name": "Récapitulatif Hebdomadaire - Talents Cinéma",
    "description": "Email récapitulatif des nouvelles inscriptions de talents cinéma envoyé chaque dimanche"
  },
  "name_detection": {
    "enabled": true,
    "name": "Détection de Nom",
    "description": "Email de notification lors de la détection d'un nom existant dans le système"
  }
}
```

**Vérification avant Envoi** :

```python
def is_template_enabled(template_type):
    """Vérifie si un type de template est activé"""
    email_config = AppSettings.get('email_notifications_config', {})
    return email_config.get(template_type, {}).get('enabled', True)
```

**Interface Admin** : `/admin/settings/email-notifications`

**Fonctionnalités** :
- Statistiques en temps réel (total, succès, échecs)
- Activation/désactivation par template (toggle)
- Historique complet avec pagination
- Filtrage par type et statut
- Visualisation du contenu HTML de chaque email

#### Interface Admin

**Route** : `/admin/settings/email-notifications`

**Fonctionnalités** :

1. **Statistiques** :
   - Total emails envoyés
   - Emails en succès
   - Emails en échec
   - Taux de succès (%)

2. **Configuration Templates** :
   - Toggle activation/désactivation par template
   - Application immédiate (sans redémarrage)

3. **Historique Paginé** :
   - 50 emails par page
   - Filtrage par template_type
   - Filtrage par status (sent/failed)

4. **Visualisation Email** :
   - Route : `/admin/settings/email-notifications/<log_id>/view`
   - Affichage HTML complet
   - Détails techniques (date, destinataire, erreurs)

#### Optimisations Techniques

**1. Templates HTML** :
- Responsive design
- Logo encodé en base64 (pas de lien externe)
- Gradients CSS inline
- Compatibilité multi-clients email

**2. Détection Domaine** :

```python
def get_application_domain():
    """Détecte le domaine selon l'environnement"""
    domain = os.environ.get('APP_DOMAIN')
    if domain:
        return domain
    domain = os.environ.get('REPLIT_DEV_DOMAIN')
    if domain:
        return domain
    domains = os.environ.get('REPLIT_DOMAINS')
    if domains:
        return domains.split(',')[0].strip()
    return 'localhost:5000'
```

**3. Gestion d'Erreurs** :
- Logging détaillé de chaque échec
- Messages utilisateur conviviaux
- Stockage des erreurs SendGrid
- Pas de crash en cas d'échec email

**4. Performance** :
- Envoi asynchrone possible (background jobs)
- Batch processing pour projets avec beaucoup de talents
- Indexes optimisés pour requêtes fréquentes

#### Sécurité et Conformité

**RGPD** :
- Consentement implicite (notifications de service)
- Opt-out possible via admin
- Stockage sécurisé des logs
- Pas de partage de données

**Chiffrement** :
- Communications HTTPS avec SendGrid
- Clés API stockées en variables d'environnement
- Logs accessibles uniquement aux admins

**Validation** :
- Vérification format email
- Sanitization du contenu HTML
- Protection contre injection
- Rate limiting possible (SendGrid)

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
| **PP** | Code pays d'origine ISO-2 | `MA` (Maroc) |
| **G** | Genre | `M`, `F`, ou `N` |
| **NNNN** | 4 chiffres **séquentiels par pays d'origine** | `0001` |
| **VVV** | 3 premières lettres de la ville de résidence | `RAB` (Rabat) |

**Exemple**: `MAM0001RAB` (Origine Maroc, Masculin, 1ère personne originaire du Maroc, résidant à Rabat)

**Important**: Le numéro est **séquentiel et incrémenté par pays d'origine**, pas par ville de résidence:
- `MAM0001RAB` = 1ère personne originaire du Maroc (résidant à Rabat), genre masculin
- `MAF0002CAS` = 2ème personne originaire du Maroc (résidant à Casablanca), genre féminin
- `SNM0001DAK` = 1ère personne originaire du Sénégal (résidant à Dakar), genre masculin

**Note**: Le code utilise le pays d'origine (nationality/country_id) et la ville de résidence (residence_city_id) pour permettre une traçabilité géographique tout en respectant la mobilité des talents.

### Format CINEMA (Talents Cinématographiques)

**Structure**: `PPVVVNNNNNG` (11 caractères)

| Composant | Description | Exemple |
|-----------|-------------|---------|
| **PP** | Code pays d'origine ISO-2 | `MA` (Maroc) |
| **VVV** | 3 premières lettres de la ville de résidence | `CAS` (Casablanca) |
| **NNNN** | 4 chiffres **séquentiels par pays d'origine** | `0001` |
| **G** | Genre | `M`, `F` |

**Exemple**: `MACAS0001F` (Origine Maroc, résidant à Casablanca, 1ère personne CINEMA originaire du Maroc, Femme)

**Important**: Le numéro est **séquentiel par pays d'origine**, identique au système standard:
- `MACAS0001F` = 1ère personne CINEMA originaire du Maroc (résidant à Casablanca)
- `MARAB0002M` = 2ème personne CINEMA originaire du Maroc (résidant à Rabat)
- `SNDAG0001F` = 1ère personne CINEMA originaire du Sénégal (résidant à Dakar)

**Note**: Comme pour les talents standards, le code CINEMA utilise le pays d'origine (country_of_origin) et la ville de résidence (city_of_residence).

**Distinction**: Les codes CINEMA se distinguent des codes standards par l'ordre des composants et la longueur:
- **Standard** (10 caractères): Pays d'origine-Genre-Numéro-Ville de résidence (PPGNNNNVVV)
- **CINEMA** (11 caractères): Pays d'origine-Ville de résidence-Numéro-Genre (PPVVVNNNNNG)

**Filtrage**: Les talents CINEMA (codes de 11 caractères) sont automatiquement filtrés et n'apparaissent que dans le module `/cinema/talents`. Ils sont exclus de `/` et `/admin/users`.

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

## Système de Logs d'Activité Amélioré

### Vue d'Ensemble

Le système enregistre **automatiquement** toutes les actions des utilisateurs avec des informations détaillées pour l'audit, l'analyse et le débogage.

### Table `activity_logs`

**Modèle** : `app/models/activity_log.py`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | Integer | Clé primaire |
| `user_id` | Integer | ID utilisateur (FK) |
| `username` | String(200) | Nom complet |
| `user_email` | String(150) | Email |
| `user_code` | String(50) | Code unique |
| `action_type` | String(50) | Type (create, update, delete, view, login, etc.) |
| `action_category` | String(50) | Catégorie (auth, cinema, production, etc.) |
| `action_description` | Text | Description détaillée |
| `resource_type` | String(100) | Type de ressource |
| `resource_id` | String(100) | ID de la ressource |
| `status` | String(20) | Statut (success, error, warning) |
| `ip_address` | String(45) | Adresse IP client |
| `user_agent` | Text | User-Agent navigateur |
| `browser` | String(50) | Navigateur |
| `browser_version` | String(20) | Version navigateur |
| `device_type` | String(20) | Type (desktop, mobile, tablet) |
| `device_brand` | String(50) | Marque appareil |
| `device_model` | String(50) | Modèle appareil |
| `operating_system` | String(50) | Système d'exploitation |
| `os_version` | String(20) | Version OS |
| `request_method` | String(10) | Méthode HTTP |
| `request_url` | Text | URL requête |
| `request_referrer` | Text | URL provenance |
| `created_at` | DateTime | Date création |

### Consultation via Interface Admin

**Route** : `/admin/settings/activity-logs`

Fonctionnalités :
- ✅ Consultation tous les logs
- ✅ Filtres (utilisateur, type, catégorie, statut)
- ✅ Recherche par mot-clé
- ✅ Détails complets (IP, device, browser)
- ✅ Export CSV/Excel
- ✅ Statistiques et graphiques

---

## Middleware de Logging Automatique

### Vue d'Ensemble

Le **middleware** enregistre automatiquement toutes les consultations de pages et actions **sans intervention du développeur**.

**Fichier** : `app/utils/activity_logger.py`

### Fonctionnalités

- ✅ Enregistrement automatique requêtes HTTP
- ✅ Extraction informations client (IP, browser, device, OS)
- ✅ Détection type d'appareil (desktop, mobile, tablet)
- ✅ Gestion gracieuse erreurs (ne bloque jamais l'application)
- ✅ Filtrage intelligent (ignore fichiers statiques)
- ✅ Decorator personnalisé pour actions spécifiques

### Initialisation

Automatique au démarrage dans `app/__init__.py` :

```python
from app.utils.activity_logger import ActivityLogger

@app.before_request
def log_request():
    if ActivityLogger._should_log_request():
        try:
            ActivityLogger._create_log_entry(
                user=current_user if current_user.is_authenticated else None,
                action_type='view',
                action_category='page_view',
                description=f"Consultation de {request.path}",
                status='success'
            )
        except:
            pass  # Ne jamais bloquer
```

### Decorator `@log_activity`

Pour enregistrer actions spécifiques :

```python
from app.utils.activity_logger import log_activity

@bp.route('/cinema/talents/new', methods=['POST'])
@login_required
@log_activity('create', 'cinema', 'CinemaTalent')
def create_cinema_talent():
    # Logique métier
    talent = CinemaTalent(...)
    db.session.add(talent)
    db.session.commit()
    
    # Log créé automatiquement !
    return redirect(url_for('cinema.talents'))
```

**Paramètres** :
- `action_type` : Type d'action (`'create'`, `'update'`, `'delete'`, `'view'`)
- `action_category` : Catégorie (`'cinema'`, `'production'`, `'project'`)
- `resource_type` : Type de ressource (optionnel)

### Extraction Informations Client

Le middleware extrait automatiquement :

```json
{
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "browser": "Chrome",
    "browser_version": "118.0.5993.88",
    "device_type": "desktop",
    "device_brand": "Apple",
    "device_model": "Macintosh",
    "operating_system": "Mac OS X",
    "os_version": "10.15.7",
    "request_method": "GET",
    "request_url": "https://taalentio.com/cinema/talents",
    "request_referrer": "https://taalentio.com/dashboard"
}
```

---

## Pages Légales Personnalisables

### Vue d'Ensemble

Système permettant de configurer et activer/désactiver les pages légales depuis l'interface admin.

### Pages Disponibles

| Page | Route | Description |
|------|-------|-------------|
| **CGU** | `/legal/terms` | Conditions Générales d'Utilisation |
| **Confidentialité** | `/legal/privacy` | Politique de protection des données |
| **À Propos** | `/about` | Présentation de la plateforme |
| **Cookies** | `/legal/cookies` | Politique cookies |
| **Mentions Légales** | `/legal/mentions` | Mentions légales obligatoires |

### Configuration via AppSettings

**Modèle** : `app/models/settings.py`

Deux clés stockées :
1. **`legal_pages_enabled`** (JSON) : Active/désactive chaque page
2. **`legal_pages`** (JSON) : Contenu de chaque page

#### Exemple `legal_pages_enabled`

```json
{
    "terms": true,
    "privacy": true,
    "about": false,
    "cookies": true,
    "mentions": false
}
```

### Routes et Logique

**Fichier** : `app/routes/legal.py`

Chaque route vérifie si la page est activée :

```python
@bp.route('/legal/terms')
def terms():
    """Conditions Générales d'Utilisation"""
    legal_pages_enabled = AppSettings.get('legal_pages_enabled', {})
    
    # Si page non activée, retourner 404
    if not legal_pages_enabled.get('terms', False):
        abort(404)
    
    legal_pages = AppSettings.get('legal_pages', {})
    content = legal_pages.get('terms_page', '')
    
    return render_template('legal/terms.html', content=content)
```

### Interface Admin

**Route** : `/admin/settings/customization`

Permet de :
- ✅ Activer/Désactiver chaque page (checkbox)
- ✅ Éditer le contenu (HTML/Markdown)
- ✅ Prévisualiser avant publication
- ✅ Sauvegarder modifications

---

## Système de Personnalisation du Footer

### Vue d'Ensemble

Personnalisation complète du footer incluant :
- ✅ Texte personnalisé
- ✅ Email et téléphone de contact
- ✅ Liens vers 8 réseaux sociaux
- ✅ Logo, favicon, image hero

**Route Admin** : `/admin/settings/customization`

### Configuration via AppSettings

| Clé | Type | Description |
|-----|------|-------------|
| `footer_text` | String | Texte personnalisé du footer |
| `footer_contact_email` | String | Email de contact |
| `footer_contact_phone` | String | Téléphone de contact |
| `social_links` | JSON | Liens réseaux sociaux |
| `logo_url` | String | URL logo principal |
| `favicon_url` | String | URL favicon |
| `hero_image_url` | String | URL image hero |

### Réseaux Sociaux Supportés

```json
{
    "facebook": "https://facebook.com/votreprofil",
    "instagram": "https://instagram.com/votreprofil",
    "twitter": "https://twitter.com/votreprofil",
    "linkedin": "https://linkedin.com/company/votreentreprise",
    "tiktok": "https://tiktok.com/@votreprofil",
    "youtube": "https://youtube.com/@votrechaine",
    "whatsapp": "+212XXXXXXXXX",
    "telegram": "https://t.me/votregroupe"
}
```

### Sauvegarde

**Routes** :
- `/admin/settings/customization/save-footer` - Footer
- `/admin/settings/customization/save-social-links` - Réseaux sociaux
- `/admin/settings/customization/save-logo-images` - Images

```python
@bp.route('/settings/customization/save-footer', methods=['POST'])
@login_required
@admin_required
def save_site_footer():
    footer_text = request.form.get('footer_text', '').strip()
    footer_contact_email = request.form.get('footer_contact_email', '').strip()
    footer_contact_phone = request.form.get('footer_contact_phone', '').strip()
    
    AppSettings.set('footer_text', footer_text)
    AppSettings.set('footer_contact_email', footer_contact_email)
    AppSettings.set('footer_contact_phone', footer_contact_phone)
    
    flash('✅ Pied de page mis à jour', 'success')
    return redirect(url_for('admin.settings_customization'))
```

---

## Nouvelles Tables et Modèles

### 1. AppSettings (`app/models/settings.py`)

**Table** : `app_settings`

Stocke tous les paramètres configurables de l'application.

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | Integer | Clé primaire |
| `key` | String(100) | Clé unique du paramètre |
| `value` | Text (JSON) | Valeur (JSON pour objets/listes) |
| `updated_at` | DateTime | Date dernière modification |

**Méthodes** :

```python
# Récupérer
value = AppSettings.get('key', default=None)

# Définir
AppSettings.set('key', value)

# Supprimer
AppSettings.delete('key')
```

### 2. SecurityLog (`app/models/security_log.py`)

**Table** : `security_logs`

Journal de sécurité pour événements sensibles.

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | Integer | Clé primaire |
| `user_id` | Integer | ID utilisateur (nullable) |
| `event_type` | String(50) | Type (`login_failed`, `unauthorized_access`, etc.) |
| `ip_address` | String(45) | Adresse IP |
| `user_agent` | Text | User-Agent |
| `details` | Text (JSON) | Détails supplémentaires |
| `severity` | String(20) | Sévérité (`low`, `medium`, `high`, `critical`) |
| `created_at` | DateTime | Date création |

### 3. EmailLog (`app/models/email_log.py`)

**Table** : `email_logs`

Journal de tous les emails envoyés.

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | Integer | Clé primaire |
| `recipient` | String(150) | Email destinataire |
| `subject` | String(200) | Sujet |
| `template_type` | String(50) | Type template |
| `status` | String(20) | Statut (`sent`, `failed`, `queued`) |
| `error_message` | Text | Message d'erreur (si échec) |
| `html_content` | Text | Contenu HTML |
| `sent_at` | DateTime | Date envoi |

**Types de templates** :
- `talent_registration` - Inscription talent standard
- `cinema_talent_registration` - Inscription talent cinéma
- `ai_talent_match` - Résultats matching IA
- `weekly_recap` - Récapitulatif hebdomadaire admin
- `name_detection` - Détection de nom existant

### 4. NameTracking (`app/models/name_tracking.py`)

**Table** : `name_tracking`

Suivi des noms pour détection de doublons.

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | Integer | Clé primaire |
| `first_name` | String(100) | Prénom normalisé |
| `last_name` | String(100) | Nom normalisé |
| `full_name` | String(200) | Nom complet normalisé |
| `original_user_id` | Integer | ID premier utilisateur avec ce nom |
| `count` | Integer | Nombre d'occurrences |
| `created_at` | DateTime | Date première occurrence |
| `updated_at` | DateTime | Date dernière mise à jour |

### 5. NameTrackingMatch (`app/models/name_tracking.py`)

**Table** : `name_tracking_matches`

Correspondances de doublons de noms.

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | Integer | Clé primaire |
| `tracking_id` | Integer | FK vers `name_tracking` |
| `user_id` | Integer | FK vers `users` |
| `similarity_score` | Float | Score similarité (0-1) |
| `status` | String(20) | Statut (`pending`, `reviewed`, `ignored`) |
| `created_at` | DateTime | Date détection |

---

## Service Email - Footer Personnalisé et Notification Admin

### Footer Personnalisé des Emails

**Service** : `app/services/email_service.py`

Le footer des emails peut être configuré via AppSettings :

```python
footer_text = """
© 2024 taalentio.com - Plateforme de valorisation des talents
Ceci est un email automatique, merci de ne pas y répondre.

Pour toute question : contact@taalentio.com
"""

AppSettings.set('email_footer', footer_text)
```

Le footer est automatiquement ajouté à tous les emails :

```python
def _get_email_footer(self):
    """Récupère le pied de page configuré pour tous les emails"""
    try:
        from app.models.settings import AppSettings
        footer_text = AppSettings.get('email_footer', 
            '© 2024 taalentio.com\nCeci est un email automatique.')
        
        footer_html = footer_text.replace('\n', '<br>')
        
        return f"""
        <div class="footer">
            <p>{footer_html}</p>
        </div>
        """
    except Exception as e:
        # Fallback
        return "<div class=\"footer\"><p>© 2024 taalentio.com</p></div>"
```

### Notification Admin

Les emails de notification admin (récapitulatifs hebdomadaires, détections de doublons) sont envoyés à l'adresse configurée :

```python
# Récupérer l'email admin
admin_email = AppSettings.get('admin_notification_email')

# Si pas configuré, chercher le premier admin
if not admin_email:
    admin = User.query.filter_by(role='admin').first()
    if admin:
        admin_email = admin.email
```

**Configuration via Interface Admin** : `/admin/settings/email-notifications`

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
