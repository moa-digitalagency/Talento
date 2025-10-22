# 🔐 Accès Admin - TalentsMaroc.com

## Identifiants Admin par Défaut

Les identifiants administrateur sont **GARANTIS** de fonctionner à chaque démarrage de l'application :

### 📧 Option 1 : Connexion par Email
- **Email**: `admin@talento.com`
- **Mot de passe**: `@4dm1n`

### 🔢 Option 2 : Connexion par Code Unique
- **Code Unique**: `MARAB0001N`
- **Mot de passe**: `@4dm1n`

---

## ✅ Garanties de Fonctionnement

L'application vérifie **automatiquement** à chaque démarrage que :

1. ✅ Le compte admin existe dans la base de données
2. ✅ Le mot de passe est configuré correctement
3. ✅ Les droits administrateur sont activés
4. ✅ Le compte est actif

Si le compte n'existe pas, il est **créé automatiquement** au démarrage.

---

## 🔧 Configuration Avancée

### Modifier le Mot de Passe Admin

Pour changer le mot de passe administrateur par défaut, définissez la variable d'environnement :

```bash
ADMIN_PASSWORD=VotreNouveauMotDePasse123
```

Le système utilisera automatiquement ce mot de passe à la place de `@4dm1n`.

---

## 📋 Initialisation Manuelle de la Base de Données

Si vous déployez l'application pour la première fois ou après une réinitialisation complète de la base de données :

```bash
python3 migrations_init.py
```

Ce script va :
- ✅ Créer toutes les tables nécessaires
- ✅ Ajouter 194 pays du monde
- ✅ Ajouter 79 villes marocaines
- ✅ Créer 73 catégories de talents
- ✅ Créer le compte admin
- ✅ Créer 5 utilisateurs de démonstration
- ✅ Créer 3 profils CINEMA de démonstration

---

## 🚀 Vérification des Accès

Pour vérifier que le compte admin existe et fonctionne :

```bash
python3 ensure_admin.py
```

Ce script affichera le statut du compte admin et le recréera si nécessaire.

---

## 🛡️ Sécurité en Production

### ⚠️ IMPORTANT - À faire avant la mise en production :

1. **Changez le mot de passe admin** en définissant la variable `ADMIN_PASSWORD`
2. **Utilisez une base de données PostgreSQL** pour la production (au lieu de SQLite)
3. **Activez HTTPS** pour sécuriser les connexions
4. **Désactivez le mode debug** (`DEBUG=False`)

### Configuration Production

```bash
# Variables d'environnement recommandées
export ADMIN_PASSWORD="UnMotDePasseTrèsSecurisé2024!"
export DATABASE_URL="postgresql://user:password@host:5432/dbname"
export SECRET_KEY="une-clé-secrète-longue-et-aléatoire"
export DEBUG=False
```

---

## 🔍 Dépannage

### Problème : "Identifiant ou mot de passe incorrect"

**Solutions :**

1. Vérifiez que vous utilisez les bons identifiants :
   - Email : `admin@talento.com` OU Code : `MARAB0001N`
   - Mot de passe : `@4dm1n`

2. Réinitialisez le mot de passe admin :
   ```bash
   python3 ensure_admin.py
   ```

3. Vérifiez la base de données :
   ```bash
   python3 -c "from app import create_app; from app.models.user import User; app = create_app(); app.app_context().push(); admin = User.query.filter_by(email='admin@talento.com').first(); print(f'Admin existe: {admin is not None}')"
   ```

### Problème : Base de données vide

Si la base de données est vide, exécutez :

```bash
python3 migrations_init.py
```

---

## 📞 Support

Si les accès admin ne fonctionnent toujours pas après avoir suivi ces étapes, vérifiez :
- Les logs de l'application au démarrage
- Que la base de données est accessible
- Que les tables `users`, `countries` et `cities` existent

---

**Dernière mise à jour** : 22 octobre 2025
