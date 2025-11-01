# Talento - Plateforme de Centralisation des Talents

> Plateforme professionnelle pour la centralisation et la mise en valeur des profils de talents à travers l'Afrique

## 📚 Documentation Complète

Toute la documentation du projet se trouve dans le dossier [`docs/`](./docs/) avec des versions **FR** (français) et **EN** (anglais).

### Documents Principaux

| Document | Français | English |
|----------|----------|---------|
| **README** | [README.fr.md](./docs/README.fr.md) | [README.en.md](./docs/README.en.md) |
| **CHANGELOG** | [CHANGELOG.fr.md](./docs/CHANGELOG.fr.md) | [CHANGELOG.en.md](./docs/CHANGELOG.en.md) |
| **DEPLOYMENT** | [DEPLOYMENT.fr.md](./docs/DEPLOYMENT.fr.md) | [DEPLOYMENT.en.md](./docs/DEPLOYMENT.en.md) |
| **TECHNICAL** | [TECHNICAL_DOCUMENTATION.fr.md](./docs/TECHNICAL_DOCUMENTATION.fr.md) | [TECHNICAL_DOCUMENTATION.en.md](./docs/TECHNICAL_DOCUMENTATION.en.md) |
| **DATABASE** | [DATABASE_MANAGER.fr.md](./docs/DATABASE_MANAGER.fr.md) | [DATABASE_MANAGER.en.md](./docs/DATABASE_MANAGER.en.md) |

📖 **[Index complet de la documentation →](./docs/INDEX.md)**

## 🚀 Démarrage Rapide

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/votre-repo/talento.git
cd talento

# Installer les dépendances Python
pip install -r requirements.txt

# Initialiser la base de données
python database_manager.py --force

# Démarrer l'application
python app.py
```

### Configuration

Définissez les variables d'environnement suivantes:

```bash
SECRET_KEY=votre_clé_secrète
ENCRYPTION_KEY=votre_clé_de_chiffrement
PORT=5000
```

## 📖 Plus d'Informations

Pour plus de détails sur:
- **L'architecture** → Voir [TECHNICAL_DOCUMENTATION.fr.md](./docs/TECHNICAL_DOCUMENTATION.fr.md) ou [EN](./docs/TECHNICAL_DOCUMENTATION.en.md)
- **Le déploiement** → Voir [DEPLOYMENT.fr.md](./docs/DEPLOYMENT.fr.md) ou [EN](./docs/DEPLOYMENT.en.md)
- **Les modifications** → Voir [CHANGELOG.fr.md](./docs/CHANGELOG.fr.md) ou [EN](./docs/CHANGELOG.en.md)
- **La base de données** → Voir [DATABASE_MANAGER.fr.md](./docs/DATABASE_MANAGER.fr.md) ou [EN](./docs/DATABASE_MANAGER.en.md)

## 📧 Contact

**MOA Digital Agency LLC**  
Par: Aisance KALONJI  
Email: moa@myoneart.com  
Web: www.myoneart.com

---

*Pour la documentation complète, consultez le dossier [`docs/`](./docs/)*

## Script d'initialisation des données

Pour charger ou recharger les données essentielles (pays, villes, talents) dans la base de données, exécutez:

```bash
SECRET_KEY=<votre_secret_key> ENCRYPTION_KEY=<votre_encryption_key> python init_essential_data.py
```

Ce script charge:
- **194 pays** du monde entier avec mapping automatique vers leur monnaie
- **1837 villes** réparties dans différents pays
- **188 talents** (131 talents généraux, 57 talents cinéma)
  - Talents généraux: visibles dans les listings principaux (/, /talents, /admin/users)
  - Talents cinéma: exclusifs à la plateforme cinéma (/cinema/talents)

Le script est **idempotent** - il peut être exécuté plusieurs fois sans créer de doublons.

## 🎯 Fonctionnalités Clés

### Système de Catégorisation des Talents
- **Talents Généraux (tag='general')**: 131 talents organisés en 14 catégories de services (Services à la personne, Bâtiment, Commerce, Multimédia, Santé, etc.)
- **Talents Cinéma (tag='cinema')**: 57 talents organisés en 7 catégories de compétences (artistiques, physiques, manuelles, sociales, techniques, expériences professionnelles, qualités humaines)
- Filtrage automatique basé sur les tags pour séparer les talents cinéma des talents généraux
- API `/api/talents` filtre automatiquement pour afficher uniquement les talents généraux dans le formulaire d'inscription standard

### Gestion des Localisations
- **Double gestion des villes**: Ville d'origine (city) et Ville de résidence (residence_city)
- **Affichage prioritaire**: Les listings administratifs affichent la ville de résidence (plus pertinent pour le recrutement)
- **Filtrage**: Recherches et filtres utilisent residence_city_id pour des résultats précis

### Support Multi-Devises
- Mapping automatique de **60+ pays** vers leur monnaie locale
- Support pour MAD (Maroc), CDF (RDC), EUR (France), USD (USA), FCFA (Afrique de l'Ouest), etc.
- **Affichage dynamique**: Les formulaires d'inscription mettent à jour automatiquement la devise affichée selon le pays de résidence sélectionné
- JavaScript synchronisé avec les constantes Python pour une expérience utilisateur cohérente
