# Guide d'utilisation - init_full_database.py

## 📖 Vue d'ensemble

Script complet et sécurisé pour initialiser et migrer la base de données Talento.

## ✅ Ce que fait le script

1. **Création des tables** - Crée toutes les tables manquantes
2. **Migration des colonnes** - Ajoute les colonnes manquantes sans perte de données
3. **Seeding des données** :
   - 194 pays du monde entier
   - 1711+ villes principales
   - 70 talents (acteurs, réalisateurs, techniciens, etc.)
   - Compte administrateur par défaut
   - Paramètres de base de l'application
4. **Backup/Restore** - Sauvegarde avant opérations critiques
5. **Rollback automatique** - Annulation en cas d'erreur

## 🚀 Utilisation

### Mode interactif (recommandé pour la première fois)
```bash
python init_full_database.py
```
Le script demandera confirmation avant chaque opération critique.

### Mode automatique (CI/CD, déploiement)
```bash
python init_full_database.py --force
```
Aucune confirmation demandée, idéal pour les scripts automatisés.

### Voir les modifications sans les appliquer
```bash
python init_full_database.py --dry-run
```
Affiche tout ce qui serait fait sans modifier la base de données.

### Avec backup de sécurité
```bash
python init_full_database.py --backup-first
```
Crée un backup complet avant toute modification.

### Logs détaillés
```bash
python init_full_database.py --verbose
```
Affiche tous les logs de débogage.

### Combinaison d'options
```bash
python init_full_database.py --backup-first --force
```

## 📊 Exemple de sortie

```
================================================================================
    INITIALISATION COMPLÈTE DE LA BASE DE DONNÉES - taalentio.com
================================================================================

────────────────────────────────────────────────────────────────────────────────
ÉTAPE 1: CRÉATION DES TABLES
────────────────────────────────────────────────────────────────────────────────
✅ Toutes les tables requises existent déjà

────────────────────────────────────────────────────────────────────────────────
ÉTAPE 2: MIGRATION DES COLONNES
────────────────────────────────────────────────────────────────────────────────
➕ Colonnes manquantes dans users: 3
   ✅ Colonne users.website ajoutée
   ✅ Colonne users.imdb_url_encrypted ajoutée
   ✅ Colonne users.threads_encrypted ajoutée

────────────────────────────────────────────────────────────────────────────────
ÉTAPE 3: CHARGEMENT DES DONNÉES ESSENTIELLES
────────────────────────────────────────────────────────────────────────────────
🌍 Chargement des pays...
✅ 193 nouveaux pays ajoutés (Total: 194 pays)

🏙️  Chargement des villes...
✅ 1710 nouvelles villes ajoutées (Total: 1711 villes)

⭐ Chargement des talents...
✅ 70 nouveaux talents ajoutés (Total: 70 talents)

👤 Vérification du compte administrateur...
✅ Compte admin créé: admin@talento.com
🔑 Mot de passe par défaut: @4dm1n

================================================================================
    RÉSUMÉ DE L'INITIALISATION
================================================================================

✅ Initialisation terminée avec succès!

📊 Statistiques:
   • Tables créées: 0
   • Colonnes ajoutées: 3
   • Pays ajoutés: 193
   • Villes ajoutées: 1710
   • Talents ajoutés: 70
   • Compte admin: Créé
   • Paramètres ajoutés: 8

📈 État final de la base de données:
   • Tables: 16
   • Utilisateurs: 1
   • Pays: 194
   • Villes: 1711
   • Talents: 70

================================================================================
```

## 🔒 Sécurité

- **Backups automatiques** avant opérations destructives
- **Rollback automatique** en cas d'erreur
- **Confirmations** pour les opérations critiques (sauf avec --force)
- **Données sensibles chiffrées** (téléphone, adresses, etc.)
- **Logs détaillés** de toutes les opérations

## 🔄 Idempotence

Le script peut être exécuté plusieurs fois sans problème :
- Détecte les données existantes
- N'ajoute que ce qui manque
- Aucune duplication

**Exemple de 2ème exécution :**
```bash
python init_full_database.py --force
# Sortie: "Base de données déjà à jour, aucune modification nécessaire"
```

## 📋 Options complètes

| Option | Description |
|--------|-------------|
| `--force` | Mode non-interactif, sans confirmations |
| `--backup-first` | Créer un backup avant toute opération |
| `--dry-run` | Afficher les modifications sans les appliquer |
| `--verbose` ou `-v` | Logs détaillés (niveau DEBUG) |
| `--help` ou `-h` | Afficher l'aide |

## 🎯 Cas d'usage

### Premier déploiement
```bash
python init_full_database.py --force
```

### Migration de production (sécurisée)
```bash
python init_full_database.py --backup-first
```

### Vérifier avant migration
```bash
python init_full_database.py --dry-run --verbose
```

### Développement local
```bash
python init_full_database.py
```

## ⚠️ Important

1. **Compte admin** : Le mot de passe par défaut est `@4dm1n` - **Changez-le immédiatement** après la première connexion !

2. **Variables d'environnement** : Le script nécessite :
   - `SECRET_KEY` - Clé secrète Flask
   - `ENCRYPTION_KEY` - Clé de chiffrement des données sensibles
   - `DATABASE_URL` - URL de connexion PostgreSQL

3. **Backups** : Les backups sont sauvegardés dans le dossier `backups/`

## 🐛 Dépannage

### Erreur "SECRET_KEY must be set"
```bash
# Vérifier que les variables d'environnement sont définies
echo $SECRET_KEY
echo $ENCRYPTION_KEY
```

### Erreur de connexion à la base de données
```bash
# Vérifier DATABASE_URL
echo $DATABASE_URL
```

### Le script est trop lent
```bash
# Utiliser --force pour éviter les confirmations
python init_full_database.py --force
```

## 📚 Documentation complète

Consultez l'en-tête du fichier `init_full_database.py` pour la documentation complète avec tous les détails techniques.

---

**Développé par MOA Digital Agency LLC**  
**Contact : moa@myoneart.com**
