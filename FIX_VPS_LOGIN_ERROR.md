# 🔧 Guide de Résolution: Erreur de Connexion sur VPS

## 🔍 Problème Identifié

L'erreur "Internal Server Error" lors de la connexion sur votre serveur VPS (talentsmaroc.com) est causée par:

### ❌ Cause Principale: **Clé de Chiffrement Manquante ou Incorrecte**

Lorsqu'un utilisateur se connecte, l'application essaie de lire ses données personnelles (téléphone, adresse, WhatsApp) qui sont **chiffrées** dans la base de données. Si la clé de chiffrement (`ENCRYPTION_KEY`) n'est pas définie ou est différente de celle utilisée pour chiffrer les données, le déchiffrement échoue et provoque une erreur 500.

### 🔐 Problèmes de Sécurité Corrigés

Le code contenait des valeurs par défaut pour des secrets sensibles :
- ❌ `ENCRYPTION_KEY` avec une valeur par défaut
- ❌ `ADMIN_PASSWORD` avec `@4dm1n` par défaut  
- ❌ `SECRET_KEY` avec une valeur par défaut

**Ces problèmes ont été corrigés** - maintenant l'application **exige** que ces valeurs soient définies dans le fichier `.env`.

---

## ✅ Solution Complète

### Étape 1: Créer le fichier `.env` sur votre VPS

Connectez-vous à votre VPS et créez un fichier `.env` dans le répertoire de l'application:

```bash
cd /chemin/vers/votre/application
nano .env
```

### Étape 2: Générer les Clés de Sécurité

**Sur votre VPS**, exécutez ces commandes pour générer des clés sécurisées:

```bash
# Générer SECRET_KEY
python3 -c 'import secrets; print("SECRET_KEY=" + secrets.token_hex(32))'

# Générer ENCRYPTION_KEY
python3 -c 'from cryptography.fernet import Fernet; print("ENCRYPTION_KEY=" + Fernet.generate_key().decode())'
```

### Étape 3: Remplir le fichier `.env`

Copiez le contenu généré ci-dessus et complétez votre fichier `.env`:

```bash
# CLÉS DE SÉCURITÉ (OBLIGATOIRES)
SECRET_KEY=<votre-clé-générée-étape-2>
ENCRYPTION_KEY=<votre-clé-de-chiffrement-générée-étape-2>
ADMIN_PASSWORD=<votre-mot-de-passe-admin-sécurisé>

# BASE DE DONNÉES
DATABASE_URL=postgresql://votre_user:votre_password@localhost:5432/talento_db

# URL DE BASE (Important pour nginx)
BASE_URL=https://talentsmaroc.com

# ENVIRONNEMENT
FLASK_ENV=production
```

### Étape 4: ⚠️ IMPORTANT - Que faire si vous avez déjà des utilisateurs ?

Si vous avez **déjà créé des utilisateurs** avec une ancienne `ENCRYPTION_KEY`:

#### Option A: Vous connaissez l'ancienne clé
✅ **Utilisez l'ancienne clé** dans votre nouveau fichier `.env`
```bash
ENCRYPTION_KEY=<votre-ancienne-clé>
```

#### Option B: Vous ne connaissez pas l'ancienne clé
❌ **Problème**: Les données chiffrées (téléphones, adresses) sont perdues

**Solutions possibles**:
1. **Réinitialiser la base de données** (⚠️ perte de toutes les données)
   ```bash
   # Sauvegarder d'abord
   pg_dump talento_db > backup_$(date +%Y%m%d).sql
   
   # Réinitialiser
   dropdb talento_db
   createdb talento_db
   python3 migrations_init.py
   ```

2. **Migrer partiellement**: Créer un script pour copier les données **non chiffrées** (noms, emails) vers une nouvelle base

3. **Contacter les utilisateurs**: Leur demander de se réinscrire

### Étape 5: Redémarrer l'Application

```bash
# Si vous utilisez systemd
sudo systemctl restart talento

# Si vous utilisez gunicorn directement
pkill gunicorn
gunicorn --bind 0.0.0.0:5004 --reuse-port --workers 4 app:app

# Redémarrer nginx
sudo systemctl restart nginx
```

### Étape 6: Vérifier les Logs

```bash
# Logs de l'application
tail -f /var/log/talento/app.log

# Logs nginx
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

# Logs systemd (si applicable)
sudo journalctl -u talento -f
```

### Étape 7: Tester la Connexion

1. Allez sur https://talentsmaroc.com/auth/login
2. Connectez-vous avec:
   - **Email**: `admin@talento.com`
   - **Code**: `MAN0001RAB`  
   - **Mot de passe**: `<votre-ADMIN_PASSWORD-du-.env>`

---

## 🛡️ Bonnes Pratiques de Sécurité

### 1. Protéger le fichier `.env`

```bash
# Rendre le fichier lisible uniquement par le propriétaire
chmod 600 .env

# Vérifier les permissions
ls -la .env
# Résultat attendu: -rw------- 1 user user ... .env
```

### 2. Ne Jamais Committer `.env` dans Git

Vérifiez que `.env` est dans `.gitignore`:

```bash
cat .gitignore | grep "^\.env$"
# Doit afficher: .env
```

### 3. Sauvegarder la clé ENCRYPTION_KEY

⚠️ **CRITIQUE**: Sauvegardez votre `ENCRYPTION_KEY` dans un endroit sûr (gestionnaire de mots de passe, coffre-fort physique, etc.).

**Si vous la perdez, toutes les données chiffrées sont irrécupérables !**

### 4. Utiliser HTTPS en Production

Assurez-vous que nginx est configuré pour HTTPS:

```nginx
server {
    listen 443 ssl http2;
    server_name talentsmaroc.com;
    
    ssl_certificate /etc/letsencrypt/live/talentsmaroc.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/talentsmaroc.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:5004;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🔍 Diagnostic des Erreurs

### Vérifier si `.env` est chargé

```bash
# Dans l'application Python, ajoutez temporairement:
import os
print("SECRET_KEY exists:", bool(os.environ.get('SECRET_KEY')))
print("ENCRYPTION_KEY exists:", bool(os.environ.get('ENCRYPTION_KEY')))
```

### Tester la connexion à la base de données

```bash
python3 -c "
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.environ['DATABASE_URL'])
with engine.connect() as conn:
    result = conn.execute('SELECT 1')
    print('✅ Connexion DB OK')
"
```

### Vérifier les logs d'erreur Python

```python
# Dans app/__init__.py, les logs montreront:
# "⚠️ Échec du déchiffrement (clé incorrecte?): ..."
# Si vous voyez ce message, c'est que ENCRYPTION_KEY est incorrecte
```

---

## 📞 Support

Si vous rencontrez toujours des problèmes:

1. Vérifiez les logs (étape 6)
2. Assurez-vous que le fichier `.env` est dans le bon répertoire
3. Vérifiez que les variables d'environnement sont chargées (commande `env | grep -E "SECRET_KEY|ENCRYPTION_KEY|DATABASE_URL"`)
4. Redémarrez complètement le serveur si nécessaire

---

## 📝 Checklist de Déploiement

- [ ] Fichier `.env` créé avec toutes les variables requises
- [ ] `SECRET_KEY` générée et définie
- [ ] `ENCRYPTION_KEY` générée et **sauvegardée en lieu sûr**
- [ ] `ADMIN_PASSWORD` défini avec un mot de passe fort
- [ ] `DATABASE_URL` configurée correctement
- [ ] `BASE_URL` pointant vers `https://talentsmaroc.com`
- [ ] Permissions du fichier `.env` réglées sur `600`
- [ ] Application redémarrée
- [ ] Nginx redémarré
- [ ] Test de connexion admin réussi
- [ ] HTTPS activé avec certificat SSL valide

---

**Date de création**: 28 Octobre 2025  
**Version**: 1.0
