# 🚀 Configuration de Déploiement - TalentsMaroc.com

## Configuration de l'URL de Base pour les QR Codes

TalentsMaroc.com utilise un système intelligent de détection d'URL qui fonctionne automatiquement sur **toutes les plateformes** (Replit, VPS, serveurs dédiés, etc.).

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

---

## 🔧 Configuration pour Déploiement

### Sur Replit
**Aucune configuration requise !** Le système détecte automatiquement le domaine Replit.

### Sur VPS ou Serveur Dédié

Ajoutez la variable d'environnement `BASE_URL` :

#### Méthode 1 : Fichier `.env`
```bash
# Dans le fichier .env
BASE_URL=https://talentsmaroc.com
```

#### Méthode 2 : Variables d'environnement système
```bash
export BASE_URL=https://talentsmaroc.com
```

#### Méthode 3 : Configuration Nginx/Apache
```nginx
# Dans votre configuration Nginx
location / {
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host $host;
    # ... autres configurations
}
```

### Avec Docker
```dockerfile
# Dans docker-compose.yml
environment:
  - BASE_URL=https://talentsmaroc.com
```

### Avec systemd
```ini
# Dans /etc/systemd/system/talento.service
[Service]
Environment="BASE_URL=https://talentsmaroc.com"
```

---

## ✅ Vérification

Pour vérifier que l'URL de base est correctement configurée :

1. Connectez-vous à l'application
2. Accédez à votre profil
3. Générez un QR code
4. Scannez le QR code - il doit pointer vers votre domaine public

---

## 📝 Exemples d'URLs

| Environnement | BASE_URL | Résultat QR Code |
|--------------|----------|------------------|
| Replit | *(non défini)* | `https://xxx.replit.dev/profile/view/CODE` |
| VPS avec domaine | `https://talentsmaroc.com` | `https://talentsmaroc.com/profile/view/CODE` |
| VPS avec IP | `http://192.168.1.100:5000` | `http://192.168.1.100:5000/profile/view/CODE` |
| Local (dev) | *(non défini)* | `http://localhost:5000/profile/view/CODE` |

---

## 🎯 Impact sur les QR Codes

Cette configuration affecte :
- ✅ QR codes des profils utilisateurs
- ✅ QR codes des profils CINEMA
- ✅ Liens publics dans les emails
- ✅ Partages de profils

---

## 🔍 Dépannage

**Problème** : Les QR codes pointent vers localhost
- **Solution** : Définir la variable `BASE_URL` avec votre URL publique

**Problème** : Les QR codes ne fonctionnent pas après déploiement
- **Solution** : Vérifier que `BASE_URL` commence par `http://` ou `https://`

**Problème** : Besoin de régénérer tous les QR codes
- **Solution** : Les QR codes sont générés dynamiquement lors de l'inscription/modification des profils
