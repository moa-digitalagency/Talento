# Guide d'Utilisation du Gestionnaire de Base de Données

> `database_manager.py` - Gestionnaire unique et consolidé pour la base de données Talento

## 📋 Vue d'Ensemble

Le fichier `database_manager.py` remplace les anciens fichiers de migration (`migrations_init.py`, `init_essential_data.py`, `init_full_database.py`) et fournit un outil unique, sûr et puissant pour gérer la base de données.

## ✨ Fonctionnalités

- ✅ Création automatique des tables manquantes
- ✅ Ajout intelligent des colonnes manquantes (sans perte de données)
- ✅ Chargement des données essentielles (pays, villes, talents, admin)
- ✅ Backup automatique avant toute modification critique
- ✅ Rollback automatique en cas d'erreur
- ✅ Logging détaillé de toutes les opérations
- ✅ Mode dry-run pour prévisualiser les changements
- ✅ Compatible PostgreSQL et SQLite
- ✅ **Sûr pour les mises à jour GitHub** (ne supprime jamais de données existantes)

## 🚀 Utilisation

### Premier Démarrage (Installation Fraîche)

```bash
python database_manager.py --force
```

Cette commande:
1. Crée toutes les tables nécessaires
2. Charge les données essentielles (pays, villes, catégories de talents)
3. Crée le compte administrateur par défaut
4. Configure les paramètres de l'application

### Après un Pull GitHub (Mise à Jour Sécurisée)

```bash
python database_manager.py --backup-first
```

Cette commande:
1. **Crée un backup complet de la base de données**
2. Détecte et crée les nouvelles tables si nécessaire
3. Ajoute les nouvelles colonnes sans toucher aux données existantes
4. Charge les nouvelles données de référence
5. Préserve toutes vos données existantes

### Mode Interactif (avec Confirmations)

```bash
python database_manager.py
```

Le script vous demandera confirmation avant chaque opération importante.

### Vérifier l'État Sans Modification

```bash
python database_manager.py --dry-run
```

Affiche ce qui serait modifié sans rien changer dans la base de données.

## 📌 Options Disponibles

| Option | Description |
|--------|-------------|
| `--force` | Mode non-interactif (pas de confirmation) |
| `--backup-first` | Créer un backup avant toute opération |
| `--dry-run` | Afficher les modifications sans les appliquer |
| `--verbose` / `-v` | Afficher les logs détaillés |
| `--help` / `-h` | Afficher l'aide |

## 🔒 Sécurité et Garanties

### Protection des Données

1. **Jamais de suppression automatique** - Le script ne supprime JAMAIS de données existantes
2. **Backups automatiques** - Créés avant toute opération risquée
3. **Rollback automatique** - En cas d'erreur, toutes les modifications sont annulées
4. **Idempotent** - Peut être exécuté plusieurs fois sans danger

### Cas d'Usage Sûrs

✅ **Mise à jour après git pull** → Parfaitement sûr  
✅ **Re-exécution** → Aucun problème  
✅ **Réparation après erreur** → Restaure automatiquement  

## 📖 Exemples Pratiques

### Scenario 1: Nouveau Développeur

```bash
# Clone le projet
git clone https://github.com/votre-repo/talento.git
cd talento

# Installe les dépendances
pip install -r requirements.txt

# Initialise la base de données
python database_manager.py --force

# Démarre l'application
python app.py
```

### Scenario 2: Mise à Jour du Code

```bash
# Pull les dernières modifications
git pull origin main

# Met à jour la base de données en toute sécurité
python database_manager.py --backup-first

# Redémarre l'application
python app.py
```

### Scenario 3: Vérification Avant Déploiement

```bash
# Vérifie ce qui sera modifié
python database_manager.py --dry-run

# Si tout est OK, applique les changements
python database_manager.py --backup-first --force
```

## 🛠️ Résolution de Problèmes

### Erreur: "Table already exists"

C'est normal et géré automatiquement. Le script détecte les tables existantes et ne les recrée pas.

### Erreur: "Column already exists"

Également normal. Le script vérifie l'existence des colonnes avant de les ajouter.

### Backup Introuvable

Les backups sont créés dans le dossier `backups/` à la racine du projet.

### Base de Données Corrompue

```bash
# Restaurer depuis un backup
# 1. Localisez le fichier de backup dans backups/
# 2. Restaurez-le manuellement ou contactez l'équipe technique
```

## 📊 Logs et Rapports

Le script génère des logs détaillés de toutes les opérations:

```
[2025-11-01 09:00:00] [INFO] 🔍 Vérification de la structure de la base de données...
[2025-11-01 09:00:01] [INFO] ✅ Toutes les tables requises existent déjà
[2025-11-01 09:00:02] [INFO] 📊 Vérification des colonnes...
[2025-11-01 09:00:03] [INFO] ✅ Toutes les colonnes requises existent
```

## 🔄 Migration depuis les Anciens Fichiers

Si vous utilisez encore les anciens fichiers (`migrations_init.py`, `init_essential_data.py`, `init_full_database.py`), passez à `database_manager.py`:

```bash
# Aucune action requise!
# database_manager.py fait tout ce que faisaient les anciens fichiers
python database_manager.py --backup-first
```

Les anciens fichiers peuvent être supprimés en toute sécurité.

## 💡 Conseils et Bonnes Pratiques

1. **Toujours utiliser `--backup-first` en production**
2. **Utiliser `--dry-run` pour prévisualiser les changements**
3. **Garder les backups pendant au moins 30 jours**
4. **Tester sur un environnement de développement d'abord**
5. **Lire les logs après chaque exécution**

## 📞 Support

Pour toute question ou problème:
- Consultez la [documentation technique](./TECHNICAL_DOCUMENTATION.md)
- Vérifiez le [changelog](./CHANGELOG.md) pour les modifications récentes
- Contactez: moa@myoneart.com

---

**Dernière mise à jour:** 1er novembre 2025  
**Version:** 2.0 (Gestionnaire consolidé)
