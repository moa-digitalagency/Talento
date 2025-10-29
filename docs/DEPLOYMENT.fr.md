# 🚀 Guide de Déploiement - taalentio.com

**Dernière mise à jour**: 29 Octobre 2025

---

## Table des Matières

1. [Prérequis](#prérequis)
2. [Configuration de l'URL de Base](#configuration-de-lurl-de-base)
3. [Configuration SendGrid](#configuration-sendgrid)
4. [Accès Administrateur](#accès-administrateur)
5. [Déploiement sur Replit](#déploiement-sur-replit)
6. [Déploiement sur VPS](#déploiement-sur-vps)
7. [Déploiement avec Docker](#déploiement-avec-docker)
8. [Configuration de Production](#configuration-de-production)
9. [Dépannage](#dépannage)

---

## Prérequis

### Logiciels Requis
- **Python**: 3.11 ou supérieur
- **PostgreSQL**: 12 ou supérieur (pour production)
- **Git**: Pour cloner le projet

### Dépendances Python
Toutes les dépendances sont listées dans `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## Configuration de l'URL de Base

taalentio.com utilise un système intelligent de détection d'URL qui fonctionne automatiquement sur **toutes les plateformes**.

### 📍 Comment ça fonctionne ?

Le système détecte automatiquement l'URL de base dans cet ordre de priorité :

1. **Variable `BASE_URL`** (priorité maximale)
   - Utilisée pour VPS, serveurs dédiés, domaines personnalisés
   - Exemple : `https://talentsmaroc.com`

2. **Variable `REPLIT_DOMAINS`** (détection automatique sur Replit)
   - Détectée automatiquement sur Replit
   - Aucune configuration requise

3. **Fallback local** : `http://localhost:5000`
   - Utilisé en développement local

### Configuration par Plateforme

#### Sur Replit
**Aucune configuration requise !** Le système détecte automatiquement le domaine Replit.

#### Sur VPS ou Serveur Dédié

**Méthode 1 : Fichier `.env`**
```bash
BASE_URL=https://talentsmaroc.com
```

**Méthode 2 : Variables d'environnement système**
```bash
export BASE_URL=https://talentsmaroc.com
```

**Méthode 3 : systemd**
```ini
# Dans /etc/systemd/system/talento.service
[Service]
Environment="BASE_URL=https://talentsmaroc.com"
```

#### Avec Docker
```dockerfile
# Dans docker-compose.yml
environment:
  - BASE_URL=https://talentsmaroc.com
```

### Impact sur les QR Codes

Cette configuration affecte :
- ✅ QR codes des profils utilisateurs
- ✅ QR codes des profils CINEMA
- ✅ Liens publics dans les emails
- ✅ Partages de profils

### Exemples d'URLs

| Environnement | BASE_URL | Résultat QR Code |
|--------------|----------|------------------|
| Replit | *(non défini)* | `https://xxx.replit.dev/profile/view/CODE` |
| VPS avec domaine | `https://talentsmaroc.com` | `https://talentsmaroc.com/profile/view/CODE` |
| VPS avec IP | `http://192.168.1.100:5000` | `http://192.168.1.100:5000/profile/view/CODE` |
| Local (dev) | *(non défini)* | `http://localhost:5000/profile/view/CODE` |

---

## Configuration SendGrid

SendGrid est utilisé pour l'envoi d'emails (confirmations d'inscription, envoi d'identifiants, etc.).

### Obtenir une Clé API SendGrid

1. Créez un compte sur [SendGrid](https://sendgrid.com)
2. Vérifiez votre domaine d'envoi
3. Créez une clé API avec les permissions d'envoi d'emails

### Configuration

#### Option 1: Variables d'Environnement (Recommandé)

**Fichier `.env`**:
```env
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=noreply@talentsmaroc.com
```

**Ou dans Replit Secrets**:
1. Cliquez sur l'icône "Secrets" (🔒)
2. Ajoutez `SENDGRID_API_KEY` et `SENDGRID_FROM_EMAIL`

#### Option 2: Interface Admin

1. Connectez-vous en tant qu'admin
2. Allez dans **Paramètres** > **Clés API** (`/admin/settings/api-keys`)
3. Ajoutez votre clé SendGrid

### Priorité de Chargement

L'application charge les clés dans cet ordre:
1. Base de données `AppSettings` (via interface admin)
2. Variables d'environnement
3. Fichier `.env` (développement local)

### Fonctionnalités Email

- ✅ Email de confirmation après inscription talent
- ✅ Email avec identifiants de connexion
- ✅ Bouton "Renvoyer identifiants" (admin uniquement)
- ✅ Emails pour profils normaux et CINEMA

### Vérification

**Test d'envoi**:
1. Allez dans `/admin/settings/api-keys`
2. Utilisez le bouton "Tester l'email"

**Erreurs courantes**:
- Clé API invalide ou expirée
- Email expéditeur non vérifié dans SendGrid
- Quota SendGrid dépassé

---

## Accès Administrateur

### Identifiants Admin par Défaut

Les identifiants administrateur sont **GARANTIS** de fonctionner à chaque démarrage :

#### Option 1 : Connexion par Email
- **Email**: `admin@talento.com`
- **Mot de passe**: `@4dm1n`

#### Option 2 : Connexion par Code Unique
- **Code Unique**: `MAN0001RAB`
- **Mot de passe**: `@4dm1n`

### Garanties de Fonctionnement

L'application vérifie **automatiquement** à chaque démarrage que :

1. ✅ Le compte admin existe
2. ✅ Le mot de passe est configuré correctement
3. ✅ Les droits administrateur sont activés
4. ✅ Le compte est actif

Si le compte n'existe pas, il est **créé automatiquement** au démarrage.

### Modifier le Mot de Passe Admin

Pour changer le mot de passe administrateur par défaut :

```bash
ADMIN_PASSWORD=VotreNouveauMotDePasse123
```

### Vérification Manuelle

Pour vérifier que le compte admin existe :

```bash
python3 ensure_admin.py
```

### Initialisation de la Base de Données

Pour initialiser complètement la base de données :

```bash
python3 migrations_init.py
```

Ce script va :
- ✅ Créer toutes les tables
- ✅ Ajouter 194 pays du monde
- ✅ Ajouter 79 villes marocaines
- ✅ Créer 73 catégories de talents
- ✅ Créer le compte admin
- ✅ Créer 5 utilisateurs de démonstration
- ✅ Créer 3 profils CINEMA de démonstration
- ✅ Créer 2 boîtes de production de démonstration

---

## Déploiement sur Replit

### Démarrage Rapide

1. **Fork le projet** sur Replit
2. **Aucune configuration requise** - l'app détecte automatiquement l'environnement Replit
3. **Lancez l'application** - elle s'exécute sur le port 5000

### Configuration Optionnelle

Ajoutez les Secrets Replit :
- `SENDGRID_API_KEY` - Pour l'envoi d'emails
- `OPENROUTER_API_KEY` - Pour l'analyse IA de CV
- `ADMIN_PASSWORD` - Pour changer le mot de passe admin

### Workflow Configuré

Le workflow `Talento Web App` est configuré pour :
- Démarrer automatiquement sur le port 5000
- Redémarrer en cas de changement de code
- Afficher les logs en temps réel

---

## Mise à Jour de l'Application

### 🔄 Script de Mise à Jour Sécurisée (Recommandé)

Pour mettre à jour l'application **sans perdre vos données** (base de données, configuration, uploads):

```bash
./update_app.sh
```

**Ce script protège automatiquement:**
- ✅ Base de données (SQLite et PostgreSQL)
- ✅ Configuration (.env)
- ✅ Fichiers uploadés (photos, CVs, QR codes)
- ✅ Sauvegardes automatiques avant mise à jour
- ✅ Migrations de schéma de base de données

Voir le fichier `README_UPDATE.md` pour plus de détails.

---

## Déploiement sur VPS

### Installation Complète

```bash
# 1. Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# 2. Installer Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# 3. Installer PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# 4. Cloner le projet
git clone https://github.com/votre-repo/talentsmaroc.git
cd talentsmaroc

# 5. Créer un environnement virtuel
python3.11 -m venv venv
source venv/bin/activate

# 6. Installer les dépendances
pip install -r requirements.txt

# 7. Configurer PostgreSQL
sudo -u postgres psql
CREATE DATABASE talentsmaroc;
CREATE USER talento WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE talentsmaroc TO talento;
\q

# 8. Configurer les variables d'environnement
cp .env.example .env
nano .env  # Éditer avec vos valeurs
```

### Fichier `.env` pour VPS

```env
# URL de Base
BASE_URL=https://talentsmaroc.com

# Base de Données
DATABASE_URL=postgresql://talento:votre_mot_de_passe@localhost/talentsmaroc

# Sécurité
SECRET_KEY=votre-cle-secrete-tres-longue-et-aleatoire
ENCRYPTION_KEY=votre-cle-de-chiffrement-fernet

# Email
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=noreply@talentsmaroc.com

# IA
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxx

# Admin
ADMIN_PASSWORD=VotreMotDePasseSecurise123!
```

### Initialiser la Base de Données

```bash
python3 migrations_init.py
```

### Démarrage avec Gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --reuse-port app:app
```

### Service systemd

Créez `/etc/systemd/system/talento.service`:

```ini
[Unit]
Description=TalentsMaroc Web Application
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/talentsmaroc
Environment="PATH=/var/www/talentsmaroc/venv/bin"
Environment="BASE_URL=https://talentsmaroc.com"
Environment="DATABASE_URL=postgresql://talento:password@localhost/talentsmaroc"
Environment="SECRET_KEY=votre-cle-secrete"
Environment="SENDGRID_API_KEY=votre-cle"
ExecStart=/var/www/talentsmaroc/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 --reuse-port app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Activez et démarrez le service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable talento
sudo systemctl start talento
sudo systemctl status talento
```

### Configuration Nginx

Créez `/etc/nginx/sites-available/talentsmaroc`:

```nginx
server {
    listen 80;
    server_name talentsmaroc.com www.talentsmaroc.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/talentsmaroc/app/static;
        expires 30d;
    }
}
```

Activez le site:

```bash
sudo ln -s /etc/nginx/sites-available/talentsmaroc /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Certificat SSL (HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d talentsmaroc.com -d www.talentsmaroc.com
```

---

## Déploiement avec Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exposer le port
EXPOSE 5000

# Lancer l'application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--reuse-port", "app:app"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - BASE_URL=https://talentsmaroc.com
      - DATABASE_URL=postgresql://talento:password@db:5432/talentsmaroc
      - SECRET_KEY=votre-cle-secrete
      - SENDGRID_API_KEY=votre-cle
      - SENDGRID_FROM_EMAIL=noreply@talentsmaroc.com
    depends_on:
      - db
    restart: always

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=talentsmaroc
      - POSTGRES_USER=talento
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

volumes:
  postgres_data:
```

### Lancer avec Docker

```bash
docker-compose up -d
```

---

## Configuration de Production

### ⚠️ Checklist de Sécurité

Avant la mise en production :

- [ ] Changer le mot de passe admin (`ADMIN_PASSWORD`)
- [ ] Utiliser PostgreSQL (au lieu de SQLite)
- [ ] Activer HTTPS avec certificat SSL
- [ ] Désactiver le mode debug (`DEBUG=False`)
- [ ] Utiliser une clé secrète longue et aléatoire (`SECRET_KEY`)
- [ ] Configurer une clé de chiffrement unique (`ENCRYPTION_KEY`)
- [ ] Configurer SendGrid avec un domaine vérifié
- [ ] Sauvegarder régulièrement la base de données
- [ ] Configurer des logs de production
- [ ] Limiter les permissions des fichiers
- [ ] Configurer un pare-feu (UFW)

### Variables d'Environnement Production

```bash
BASE_URL=https://talentsmaroc.com
DATABASE_URL=postgresql://user:password@host:5432/talentsmaroc
SECRET_KEY=une-cle-secrete-longue-et-aleatoire-de-au-moins-32-caracteres
ENCRYPTION_KEY=votre-cle-fernet-generee
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=noreply@talentsmaroc.com
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxx
ADMIN_PASSWORD=UnMotDePasseTresSecurise2024!
FLASK_ENV=production
DEBUG=False
```

### Génération de Clés

**SECRET_KEY**:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**ENCRYPTION_KEY** (Fernet):
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## Dépannage

### Problème : Erreur "AmbiguousForeignKeysError" sur le Dashboard Admin

**Symptôme**: Erreur SQLAlchemy lors du chargement du tableau de bord admin:
```
sqlalchemy.exc.AmbiguousForeignKeysError: Can't determine join between 'cities' and 'users'
```

**Cause**: Le modèle User possède deux clés étrangères vers la table City (`city_id` et `residence_city_id`), ce qui rend certaines jointures ambiguës.

**Solution**: Cette erreur a été corrigée dans la version du 29 octobre 2025. Si vous utilisez une version plus ancienne, mettez à jour le fichier `app/routes/main.py` ligne 223:

**Avant (provoquait l'erreur)**:
```python
.join(User).join(Country)
```

**Après (corrigé)**:
```python
.join(User, City.id == User.city_id).join(Country, Country.id == User.country_id)
```

Cette modification spécifie explicitement quelle clé étrangère utiliser pour la jointure, éliminant ainsi l'ambiguïté.

### Problème : "Identifiant ou mot de passe incorrect"

**Solutions**:
1. Vérifiez les identifiants par défaut:
   - Email: `admin@talento.com` OU Code: `MAN0001RAB`
   - Mot de passe: `@4dm1n`

2. Réinitialisez le mot de passe admin:
   ```bash
   python3 ensure_admin.py
   ```

### Problème : Base de données vide

```bash
python3 migrations_init.py
```

### Problème : Les QR codes pointent vers localhost

**Solution**: Définir la variable `BASE_URL` avec votre URL publique
```bash
export BASE_URL=https://talentsmaroc.com
```

### Problème : Les emails ne partent pas

1. Vérifiez les logs pour `🔴 ERREUR SENDGRID`
2. Vérifiez que la clé API SendGrid est valide
3. Vérifiez que l'email expéditeur est vérifié dans SendGrid
4. Testez l'email depuis `/admin/settings/api-keys`

### Problème : Erreur de connexion PostgreSQL

1. Vérifiez que PostgreSQL est démarré:
   ```bash
   sudo systemctl status postgresql
   ```

2. Vérifiez la chaîne de connexion dans `DATABASE_URL`

3. Testez la connexion:
   ```bash
   psql -U talento -d talentsmaroc -h localhost
   ```

### Problème : Port 5000 déjà utilisé

**Solution**: Changez le port dans `app.py` ou utilisez une variable d'environnement:
```bash
PORT=8000 python app.py
```

---

## Support

Pour plus d'informations :
- **Documentation Technique**: `docs/TECHNICAL_DOCUMENTATION.md`
- **Changelog**: `CHANGELOG.md`
- **README**: `README.md` et `README.fr.md`

---

**Dernière mise à jour**: 29 Octobre 2025
