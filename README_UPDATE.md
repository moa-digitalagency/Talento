# 🔄 Guide de Mise à Jour - TalentsMaroc.com

## Mise à Jour Sécurisée de l'Application

Ce guide explique comment mettre à jour TalentsMaroc.com **sans perdre vos données**.

---

## 🛡️ Protection Automatique des Données

Le script `update_app.sh` protège automatiquement:

- ✅ **Configuration**: `.env` et toutes les variables d'environnement
- ✅ **Base de données**: SQLite (`.db`) et PostgreSQL
- ✅ **Fichiers uploadés**: Photos, CVs, QR codes
- ✅ **Logs**: Tous les fichiers de log
- ✅ **Sauvegardes**: Backups existants

---

## 🚀 Méthode Simple (Recommandée)

### 1. Mise à jour avec le script automatique

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

---

## 📋 Mise à Jour Manuelle (Avancée)

### Étape 1: Sauvegarde

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

### Étape 2: Mettre à jour le code

**Option A: Depuis Git (VPS)**
```bash
# Protéger les fichiers locaux
git stash save "Backup avant mise à jour"

# Récupérer les mises à jour
git pull origin main

# Les fichiers dans .gitignore ne seront PAS écrasés (.env, *.db, uploads/)
```

**Option B: Upload manuel (Replit)**
1. Télécharger les nouveaux fichiers
2. Uploader dans le projet
3. **Ne pas** remplacer: `.env`, `*.db`, `app/static/uploads/`

### Étape 3: Mettre à jour les dépendances

```bash
pip install -r requirements.txt --upgrade
```

### Étape 4: Migrer la base de données

**Méthode 1: Script automatique**
```bash
python migrations_init.py
```

**Méthode 2: Flask-Migrate**
```bash
# Générer la migration
flask db migrate -m "Update schema"

# Appliquer la migration
flask db upgrade
```

### Étape 5: Redémarrer l'application

**Sur Replit:**
```bash
# Redémarrage automatique
```

**Sur VPS avec systemd:**
```bash
sudo systemctl restart talento
```

**Sur VPS avec PM2:**
```bash
pm2 restart talento
```

---

## 🔒 Fichiers Protégés par .gitignore

Ces fichiers ne seront **JAMAIS** modifiés lors d'un `git pull`:

```
.env                          # Configuration (clés API, secrets)
*.db                          # Base de données SQLite
app/static/uploads/           # Tous les fichiers uploadés
backups/                      # Sauvegardes
*.tar.gz, *.sql              # Archives et dumps
```

---

## ⚠️ En Cas de Problème

### Restaurer depuis une sauvegarde

```bash
# Lister les sauvegardes
ls -lh backups/

# Restaurer une sauvegarde spécifique
tar -xzf backups/backup_20251029_103000.tar.gz

# Ou restaurer la base de données uniquement
cp backups/talento_20251029.db talento.db
```

### Vérifier l'intégrité de l'application

```bash
# Tester l'import Python
python -c "from app import create_app; app = create_app(); print('OK')"

# Vérifier la base de données
python -c "from app import db; db.create_all(); print('OK')"
```

---

## 🔄 Migrations de Base de Données

### Créer une nouvelle migration

```bash
# Après avoir modifié les modèles (app/models/*)
flask db migrate -m "Description de la modification"

# Vérifier la migration générée
cat migrations/versions/xxxx_description.py

# Appliquer la migration
flask db upgrade
```

### Annuler une migration

```bash
# Revenir à la version précédente
flask db downgrade

# Revenir à une version spécifique
flask db downgrade <revision>
```

---

## 📚 Workflow Recommandé

### Mise à jour hebdomadaire (VPS)

```bash
# 1. Sauvegarde automatique
./update_app.sh

# Le script fait tout automatiquement!
```

### Avant une grosse mise à jour

```bash
# 1. Sauvegarde manuelle complète
tar -czf backups/full_backup_$(date +%Y%m%d).tar.gz \
    --exclude='venv' \
    --exclude='node_modules' \
    .

# 2. Sauvegarder la base de données
pg_dump $DATABASE_URL > backups/db_$(date +%Y%m%d).sql

# 3. Tester la mise à jour
./update_app.sh

# 4. Vérifier que tout fonctionne
# Si problème: restaurer depuis backups/
```

---

## 🆘 Support

**Problèmes courants:**

### "Erreur de migration de base de données"
```bash
# Forcer la création des tables
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### "Fichiers manquants après mise à jour"
```bash
# Vérifier .gitignore
cat .gitignore | grep -E "\.env|\.db|uploads"

# Si manquant, restaurer depuis backup
tar -xzf backups/backup_YYYYMMDD_HHMMSS.tar.gz
```

### "Base de données corrompue"
```bash
# Restaurer depuis sauvegarde
cp backups/talento_YYYYMMDD.db talento.db

# Ou depuis dump PostgreSQL
psql $DATABASE_URL < backups/db_YYYYMMDD.sql
```

---

## ✅ Checklist de Mise à Jour

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

**Dernière mise à jour**: 29 Octobre 2025
