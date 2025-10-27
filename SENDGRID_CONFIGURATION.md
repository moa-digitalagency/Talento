# Configuration SendGrid - TalentsMaroc.com

## ⚠️ Problème Identifié

Les variables d'environnement SendGrid **ne sont PAS configurées** dans Replit:
- `SENDGRID_API_KEY` ❌ N'existe pas
- `SENDGRID_FROM_EMAIL` ❌ N'existe pas

## 🔧 Solution

### Option 1: Configuration via Replit Secrets (Recommandé)
Cliquez sur l'icône "Secrets" (🔒) dans Replit et ajoutez :

1. **SENDGRID_API_KEY**: Votre clé API SendGrid
   - Exemple: `SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   
2. **SENDGRID_FROM_EMAIL**: L'email expéditeur vérifié dans SendGrid
   - Exemple: `noreply@talentsmaroc.com` ou `noreply@myoneart.com`

### Option 2: Configuration via Base de Données AppSettings
Si vous préférez utiliser la base de données, allez dans l'interface admin:
- `/admin/settings/api-keys`
- Ajoutez vos clés SendGrid

## 📋 Vérification de la Configuration

### Pour vérifier si SendGrid est configuré:
1. Connectez-vous en tant qu'admin
2. Allez dans **Paramètres** > **Clés API**
3. Vérifiez que la clé SendGrid est présente et valide

### Test d'envoi d'email:
1. Inscrivez un nouveau talent
2. Ou utilisez le bouton "Renvoyer identifiants" sur un profil existant
3. Vérifiez les logs pour voir si l'email a été envoyé

## 🔍 Priorité de Chargement des Clés

L'application charge les clés dans cet ordre:
1. Base de données `AppSettings` (via interface admin)
2. Variables d'environnement Replit Secrets
3. Fichier `.env` (pour développement local)

## ✅ Fonctionnalités Email Implémentées

### 1. **Inscription Talent Normal** (`/auth/register`)
Après inscription:
- ✅ Email de confirmation de candidature
- ✅ Email avec identifiants de connexion

### 2. **Inscription Talent Cinéma** (`/cinema/register`)
Après inscription:
- ✅ Email de confirmation de candidature
- ✅ Email avec identifiants de connexion

### 3. **Bouton "Renvoyer identifiants"**
Disponible pour:
- ✅ Profils talents normaux (`/profile/view/<code>`)
- ✅ Profils talents cinéma (`/cinema/view/<code>`)

**Condition**: Admin uniquement

## 🐛 Débogage

Si les emails ne partent toujours pas après configuration:

1. **Vérifiez les logs**:
   ```
   Recherchez: 🔴 ERREUR SENDGRID
   ```

2. **Erreurs courantes**:
   - Clé API invalide ou expirée
   - Email expéditeur non vérifié dans SendGrid
   - Quota SendGrid dépassé
   - Domaine expéditeur non configuré

3. **Testez la clé SendGrid**:
   - Allez dans `/admin/settings/api-keys`
   - Utilisez le bouton "Tester l'email"

## 📝 Code Ajouté

### Nouvelles Routes:
- `POST /profile/resend_credentials/<unique_code>` - Renvoie identifiants talent normal
- `POST /cinema/resend_credentials/<unique_code>` - Renvoie identifiants talent cinéma

### Templates Modifiés:
- `app/templates/cinema/profile_view.html` - Ajout bouton "Renvoyer identifiants"
- Tous les formulaires ont maintenant des tokens CSRF

## 🚀 Pour VPS

Sur votre VPS, ajoutez ces variables dans votre fichier `.env` ou configuration serveur:
```bash
export SENDGRID_API_KEY="votre_clé_api_sendgrid"
export SENDGRID_FROM_EMAIL="noreply@talentsmaroc.com"
```

Puis redémarrez votre application.
