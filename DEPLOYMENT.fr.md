# 🚀 Guide de Déploiement - Talento Web Application

## 📋 Table des matières

1. [Prérequis](#prérequis)
2. [Déploiement sur VPS Ubuntu avec Gunicorn](#déploiement-sur-vps-ubuntu-avec-gunicorn)
3. [Configuration de la base de données](#configuration-de-la-base-de-données)
4. [Scripts de migration et mise à jour](#scripts-de-migration-et-mise-à-jour)
5. [Mises à jour de l'application](#mises-à-jour-de-lapplication)
6. [Résolution des problèmes](#résolution-des-problèmes)

---

## Prérequis

### Système
- **OS**: Ubuntu 20.04 LTS ou supérieur
- **RAM**: Minimum 2GB (4GB recommandé)
- **Espace disque**: Minimum 10GB
- **Python**: 3.9 ou supérieur
- **PostgreSQL**: 12 ou supérieur

### Accès requis
- Accès SSH root ou sudo
- Nom de domaine configuré (optionnel)
- Accès à un repository GitHub (pour les mises à jour automatiques)

---

## Déploiement sur VPS Ubuntu avec Gunicorn

### 1. Préparation du serveur

```bash
# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installation des dépendances système
sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib git supervisor

# Créer un utilisateur pour l'application (recommandé)
sudo adduser talento
sudo usermod -aG sudo talento
```

### 2. Configuration de PostgreSQL

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Créer la base de données et l'utilisateur
CREATE DATABASE talento_db;
CREATE USER talento_user WITH PASSWORD 'votre_mot_de_passe_sécurisé';
ALTER ROLE talento_user SET client_encoding TO 'utf8';
ALTER ROLE talento_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE talento_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE talento_db TO talento_user;

# Quitter PostgreSQL
\q
```

### 3. Clonage et configuration de l'application

```bash
# Se connecter en tant qu'utilisateur talento
su - talento

# Cloner le repository
cd /home/talento
git clone https://github.com/votre-username/talentsmaroc.git
cd talentsmaroc

# Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

### 4. Configuration des variables d'environnement

```bash
# Créer le fichier .env
nano .env
```

Ajouter le contenu suivant :

```env
# Configuration de la base de données
DATABASE_URL=postgresql://talento_user:votre_mot_de_passe_sécurisé@localhost/talento_db

# Clés de sécurité (générer des valeurs uniques)
SECRET_KEY=votre_secret_key_unique_et_securisee
ENCRYPTION_KEY=votre_encryption_key_base64

# Configuration de l'application
FLASK_ENV=production
SKIP_AUTO_MIGRATION=0
BASE_URL=https://votre-domaine.com

# Configuration email (optionnel)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=votre_email@gmail.com
MAIL_PASSWORD=votre_app_password

# SendGrid (recommandé pour production)
SENDGRID_API_KEY=votre_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@votre-domaine.com

# IA et Services externes (optionnel)
OPENROUTER_API_KEY=votre_openrouter_api_key
OMDB_API_KEY=votre_omdb_api_key
```

Pour générer les clés de sécurité :

```python
# Générer SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# Générer ENCRYPTION_KEY (base64)
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 5. Initialisation de la base de données

**⚠️ IMPORTANT : Utiliser le script de migration intelligent**

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Exécuter le script de migration
python3 migrations_init.py
```

**Ce script va automatiquement :**
- ✅ Créer toutes les tables manquantes
- ✅ Ajouter les colonnes manquantes
- ✅ Préserver toutes les données existantes
- ✅ Initialiser les pays et villes
- ✅ Créer l'utilisateur admin par défaut

**Tables créées :**
- `users` - Utilisateurs de la plateforme
- `talents` - Types de talents disponibles
- `user_talents` - Association utilisateurs-talents
- `countries` - Pays
- `cities` - Villes
- `productions` - Sociétés de production
- `projects` - Projets de production
- `project_talents` - Assignation talents aux projets
- `cinema_talents` - Talents cinéma
- `attendances` - Gestion des présences
- `activity_logs` - Journal d'activité
- `security_logs` - Journal de sécurité
- `email_logs` - Journal des emails
- `app_settings` - Paramètres de l'application
- `name_tracking` - Suivi des noms (doublons)
- `name_tracking_matches` - Correspondances de doublons

### 6. Configuration de Gunicorn

```bash
# Tester Gunicorn
gunicorn --bind 0.0.0.0:8000 --reuse-port app:app

# Si ça fonctionne, créer le fichier de service systemd
sudo nano /etc/systemd/system/talento.service
```

Contenu du fichier :

```ini
[Unit]
Description=Talento Web Application
After=network.target

[Service]
User=talento
Group=www-data
WorkingDirectory=/home/talento/talentsmaroc
Environment="PATH=/home/talento/talentsmaroc/venv/bin"
EnvironmentFile=/home/talento/talentsmaroc/.env
ExecStart=/home/talento/talentsmaroc/venv/bin/gunicorn \
    --workers 4 \
    --bind 0.0.0.0:8000 \
    --reuse-port \
    --access-logfile /home/talento/logs/access.log \
    --error-logfile /home/talento/logs/error.log \
    app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Créer le dossier logs
mkdir -p /home/talento/logs

# Activer et démarrer le service
sudo systemctl daemon-reload
sudo systemctl enable talento
sudo systemctl start talento
sudo systemctl status talento
```

### 7. Configuration de Nginx

```bash
sudo nano /etc/nginx/sites-available/talento
```

Contenu :

```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (si nécessaire)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /static {
        alias /home/talento/talentsmaroc/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /uploads {
        alias /home/talento/talentsmaroc/app/static/uploads;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/talento /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Configuration SSL avec Let's Encrypt (recommandé)

```bash
# Installer Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtenir le certificat SSL
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com

# Renouvellement automatique (déjà configuré par Certbot)
sudo certbot renew --dry-run
```

---

## Scripts de migration et mise à jour

### Script principal (RECOMMANDÉ) : `init_full_database.py`

**🎯 Script complet et intelligent d'initialisation et migration de la base de données**

Le script `init_full_database.py` est le **script recommandé** pour toutes les opérations de base de données. Il offre des fonctionnalités avancées de migration, backup et rollback automatique.

#### Fonctionnalités

- ✅ **Création automatique** de toutes les tables manquantes
- ✅ **Ajout intelligent** des colonnes manquantes (sans perte de données)
- ✅ **Seeding** des données essentielles (pays, villes, talents, admin)
- ✅ **Backup automatique** avant modifications critiques
- ✅ **Rollback automatique** en cas d'erreur
- ✅ **Logging détaillé** de toutes les opérations
- ✅ **Mode dry-run** pour prévisualiser les changements
- ✅ **Compatible** PostgreSQL et SQLite

#### Usage

```bash
# Mode interactif (recommandé pour première utilisation)
python init_full_database.py

# Mode automatique (sans confirmation) - PRODUCTION
python init_full_database.py --force

# Mode dry-run (voir les changements sans les appliquer)
python init_full_database.py --dry-run

# Avec backup forcé avant toute opération
python init_full_database.py --backup-first

# Combinaison d'options (mode production sécurisé)
python init_full_database.py --backup-first --force
```

#### Options disponibles

| Option | Description |
|--------|-------------|
| `--force` | Passer les confirmations (mode non-interactif) |
| `--backup-first` | Créer un backup avant toute opération |
| `--dry-run` | Afficher les modifications sans les appliquer |
| `--verbose, -v` | Afficher les logs détaillés |
| `--help, -h` | Afficher l'aide complète |

#### Exemples d'utilisation sur VPS

```bash
# Exécution sur VPS Ubuntu/Gunicorn
cd /home/talento/talentsmaroc
source venv/bin/activate

# Premier déploiement - Mode automatique avec backup
python init_full_database.py --backup-first --force

# Migration après mise à jour - Vérifier d'abord
python init_full_database.py --dry-run

# Si tout est OK, appliquer les migrations
python init_full_database.py --force

# Redémarrer Gunicorn après les migrations
sudo systemctl restart talento
```

#### Tables créées/gérées par le script

Le script gère automatiquement **16 tables** :

| Table | Description |
|-------|-------------|
| `users` | Utilisateurs de la plateforme |
| `talents` | Types de talents disponibles |
| `user_talents` | Association utilisateurs-talents |
| `countries` | Pays (54 pays africains + monde) |
| `cities` | Villes principales par pays |
| `productions` | Sociétés de production cinéma |
| `projects` | Projets de production |
| `project_talents` | Assignation talents aux projets |
| `cinema_talents` | Talents cinéma avec caractéristiques |
| `attendances` | Gestion des présences |
| `activity_logs` | **Journal d'activité** (nouveau) |
| `security_logs` | **Journal de sécurité** (nouveau) |
| `email_logs` | **Journal des emails** (nouveau) |
| `app_settings` | **Paramètres système** (nouveau) |
| `name_tracking` | **Suivi des noms** (doublons) |
| `name_tracking_matches` | **Correspondances de doublons** |

#### Sécurité et backups

- Les **backups sont créés automatiquement** avant toute opération destructive
- **Rollback automatique** en cas d'erreur pendant la migration
- Données sensibles **chiffrées** (Fernet encryption)
- **Confirmations** pour les opérations critiques (sauf mode `--force`)
- **Logs détaillés** de toutes les opérations dans `operations_log`

#### Script de migration pour VPS (Gunicorn)

Créer un script de mise à jour complet pour VPS :

```bash
#!/bin/bash
# update_database_vps.sh - Script de mise à jour base de données sur VPS

set -e  # Arrêter en cas d'erreur

echo "🔄 Mise à jour de la base de données Talento..."

# Se placer dans le répertoire de l'application
cd /home/talento/talentsmaroc

# Activer l'environnement virtuel
source venv/bin/activate

# Sauvegarder la base de données PostgreSQL
echo "💾 Sauvegarde de la base de données..."
sudo -u postgres pg_dump talento_db > "backups/manual_backup_$(date +%Y%m%d_%H%M%S).sql"

# Exécuter le script de migration avec backup automatique
echo "🚀 Exécution des migrations..."
python init_full_database.py --backup-first --force

# Redémarrer Gunicorn
echo "♻️ Redémarrage de Gunicorn..."
sudo systemctl restart talento

# Vérifier le statut
echo "✅ Vérification du service..."
sudo systemctl status talento --no-pager

echo "✅ Mise à jour terminée avec succès !"
```

Rendre le script exécutable :

```bash
chmod +x update_database_vps.sh
./update_database_vps.sh
```

### Script alternatif : `migrations_init.py`

**🎯 Script legacy (utilisé avant init_full_database.py) :**
- ✅ Première installation de l'application
- ✅ Mise à jour de la structure de la base de données
- ✅ Ajout de nouvelles tables sans écraser les données existantes

**⚠️ Recommandation :** Utiliser `init_full_database.py` à la place.

```bash
cd /home/talento/talentsmaroc
source venv/bin/activate
python3 migrations_init.py
```

### Script : `init_essential_data.py`

**🎯 Utilisation :**
- ✅ Réinitialiser uniquement les données essentielles
- ✅ Ajouter de nouveaux pays/villes
- ✅ Réinitialiser les talents par défaut

```bash
cd /home/talento/talentsmaroc
source venv/bin/activate
python3 init_essential_data.py
```

### Mises à jour automatiques depuis GitHub

L'application dispose d'un système de mise à jour automatique intégré accessible depuis l'interface admin :

**Via l'interface admin :**
1. Se connecter en tant qu'admin
2. Aller dans **Paramètres → Mises à jour GitHub**
3. Configurer le repository GitHub
4. Cliquer sur "Récupérer les mises à jour"

**Le système va automatiquement :**
- ✅ Pull le code depuis GitHub
- ✅ Installer les nouvelles dépendances Python
- ✅ Exécuter les migrations de base de données (si activé)
- ✅ Préserver toutes les données existantes

**Configuration du repository GitHub :**
```
URL du repository : https://github.com/votre-username/talentsmaroc.git
Branche : main
Migration automatique : ✓ Activée
```

---

## Mises à jour de l'application

### Mise à jour manuelle depuis GitHub

```bash
# Se connecter au serveur
ssh talento@votre-serveur.com

# Aller dans le dossier de l'application
cd /home/talento/talentsmaroc

# Sauvegarder la base de données (recommandé)
sudo -u postgres pg_dump talento_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Pull les mises à jour
git pull origin main

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les nouvelles dépendances
pip install -r requirements.txt

# Exécuter les migrations (IMPORTANT)
python3 migrations_init.py

# Redémarrer Gunicorn
sudo systemctl restart talento

# Vérifier que tout fonctionne
sudo systemctl status talento
tail -f /home/talento/logs/error.log
```

### Mise à jour automatique via interface admin

**Plus simple et plus sûr :**
1. Connexion admin : https://votre-domaine.com/admin/login
2. **Paramètres → Mises à jour GitHub**
3. Cliquer sur **"⬇️ Récupérer les mises à jour"**

Le système gère automatiquement :
- Pull du code
- Installation des dépendances
- Migrations de base de données
- Points de restauration en cas d'erreur

---

## Résolution des problèmes

### Problème : Tables manquantes après une mise à jour

```bash
# Solution : Exécuter le script de migration
cd /home/talento/talentsmaroc
source venv/bin/activate
python3 migrations_init.py
sudo systemctl restart talento
```

### Problème : Erreur "column does not exist"

```bash
# Solution : Le script de migration ajoute les colonnes manquantes
python3 migrations_init.py
```

### Problème : Gunicorn ne démarre pas

```bash
# Vérifier les logs
sudo journalctl -u talento -n 50

# Vérifier les permissions
sudo chown -R talento:www-data /home/talento/talentsmaroc
```

### Problème : Base de données inaccessible

```bash
# Vérifier que PostgreSQL fonctionne
sudo systemctl status postgresql

# Tester la connexion
psql -U talento_user -d talento_db -h localhost
```

### Sauvegarde de la base de données

```bash
# Sauvegarde complète
sudo -u postgres pg_dump talento_db > backup_$(date +%Y%m%d).sql

# Sauvegarde compressée
sudo -u postgres pg_dump talento_db | gzip > backup_$(date +%Y%m%d).sql.gz

# Restauration
sudo -u postgres psql talento_db < backup_20250101.sql
```

### Automatiser les sauvegardes (cron)

```bash
# Éditer le crontab
crontab -e

# Ajouter une sauvegarde quotidienne à 2h du matin
0 2 * * * sudo -u postgres pg_dump talento_db | gzip > /home/talento/backups/db_$(date +\%Y\%m\%d).sql.gz
```

---

## Contacts et support

**Développé par :**
- **MOA Digital Agency LLC**
- **Par :** Aisance KALONJI
- **Email :** moa@myoneart.com
- **Website :** www.myoneart.com

**Application :**
- **Site :** taalentio.com
- **Support :** admin@talento.com

---

## Changelog

### Version actuelle
- ✅ Système de customization complet (footer, logo, réseaux sociaux, pages légales)
- ✅ Gestion intelligente des mises à jour GitHub
- ✅ Migrations automatiques sans perte de données
- ✅ Scripts d'initialisation complets avec toutes les tables
- ✅ Documentation de déploiement complète

---

**📝 Note importante :** Toujours sauvegarder la base de données avant une mise à jour majeure !
