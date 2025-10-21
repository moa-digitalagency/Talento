# TalentsMaroc.com - Plateforme de Centralisation des Talents

TalentsMaroc.com est une application web professionnelle conçue pour centraliser et mettre en valeur les profils de talents à travers l'Afrique. La plateforme permet aux individus de créer des profils professionnels détaillés, de mettre en avant leurs compétences et de se connecter aux opportunités.

## Fonctionnalités

- **Inscription des Utilisateurs**: Création de profils professionnels complets avec informations personnelles, compétences et expérience
- **Système d'ID Unique**: Chaque utilisateur reçoit un code unique de 10 caractères pour une identification facile
- **Support Multi-Talents**: Les utilisateurs peuvent présenter plusieurs compétences dans diverses catégories
- **Génération de QR Code**: Génération automatique d'un QR code pour chaque profil
- **Tableau de Bord Admin**: Outils administratifs puissants pour gérer les utilisateurs et visualiser les statistiques
- **Recherche & Filtres**: Capacités de recherche avancées par nom, compétences, localisation, etc.
- **Export de Données**: Exportation des données utilisateur en formats Excel, PDF et CSV
- **Données Chiffrées**: Les informations sensibles sont chiffrées pour la sécurité
- **Couverture Africaine**: Support des 54 pays africains

## Stack Technique

- **Backend**: Flask (Python 3.11)
- **Base de Données**: PostgreSQL
- **Frontend**: HTML5, Tailwind CSS
- **Authentification**: Flask-Login
- **ORM**: SQLAlchemy
- **Email**: Flask-Mail

## Démarrage

### Prérequis

- Python 3.11+
- Base de données PostgreSQL

### Installation

1. Installer les dépendances:
```bash
pip install -r requirements.txt
```

2. Configurer les variables d'environnement:
```bash
ENCRYPTION_KEY=votre-cle-de-chiffrement
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=votre-cle-secrete
```

3. Initialiser la base de données:
```bash
python migrations_init.py
```

4. Lancer l'application:
```bash
python app.py
```

L'application sera disponible à `http://localhost:5000`

### Identifiants Admin par Défaut

- **Email**: admin@talentsmaroc.com
- **Mot de passe**: @4dm1n

⚠️ **Important**: Changez le mot de passe admin après la première connexion !

### Comptes de Démonstration

Le système inclut 5 comptes utilisateur de démonstration pour les tests:
- demo1@talentsmaroc.com à demo5@talentsmaroc.com
- Mot de passe: demo123

## Structure du Projet

```
talentsmaroc/
├── app/
│   ├── models/          # Modèles de base de données
│   ├── routes/          # Routes de l'application
│   ├── services/        # Services de logique métier
│   ├── templates/       # Templates HTML
│   ├── static/          # CSS, fichiers uploadés
│   └── utils/           # Fonctions utilitaires
├── migrations_init.py   # Initialisation de la base de données
├── app.py              # Point d'entrée de l'application
├── config.py           # Configuration
└── requirements.txt    # Dépendances Python
```

## Fonctionnalités Clés Expliquées

### 🔢 Système de Codification Unique

TalentsMaroc.com utilise **deux systèmes de codes uniques** pour identifier les profils :

#### 1. Codes CINEMA (Profils Cinématographiques)
Format : **`PPVVVNNNNNNNG`** (12 caractères)

**Exemple** : `MACAS000001F`

| Composant | Description | Exemple |
|-----------|-------------|---------|
| **PP** (2 lettres) | Code pays ISO-2 | `MA` = Maroc |
| **VVV** (3 lettres) | Ville de résidence (3 premières lettres) | `CAS` = Casablanca |
| **NNNNNN** (6 chiffres) | Numéro séquentiel **par pays** | `000001` = 1er talent du pays |
| **G** (1 lettre) | Genre | `F` = Femme, `M` = Homme |

**Important** : Le numéro séquentiel est incrémenté **par pays**, pas par ville.
- `MACAS000001F` = 1ère personne enregistrée au **Maroc**
- `MARAB000002F` = 2ème personne enregistrée au **Maroc** (de Rabat)
- `FRPAR000001M` = 1ère personne enregistrée en **France** (de Paris)

#### 2. Codes Utilisateurs (Profils Standards)
Format : **`PPVVVNNNNG`** (10 caractères)

**Exemple** : `MARAB0001N`

| Composant | Description | Exemple |
|-----------|-------------|---------|
| **PP** (2 lettres) | Code pays ISO-2 | `MA` = Maroc |
| **VVV** (3 lettres) | Ville (3 premières lettres) | `RAB` = Rabat |
| **NNNN** (4 chiffres) | Numéro **aléatoire** | `0001` |
| **G** (1 lettre) | Genre | `M`, `F`, ou `N` (non précisé) |

**Important** : Pour les profils standards, le numéro est **aléatoire** et le système vérifie l'unicité dans la base de données.

### Sécurité
- Les mots de passe sont hachés avec bcrypt
- Les données sensibles (numéros de téléphone) sont chiffrées
- Validation et vérification des emails
- Contrôles d'accès réservés aux administrateurs

### Export de Données
Les administrateurs peuvent exporter les données utilisateur dans plusieurs formats:
- **Excel**: Feuille de calcul complète avec tous les détails utilisateur
- **PDF**: Document formaté avec les informations utilisateur
- **CSV**: Format simple séparé par virgules

## Licence

© 2024 TalentsMaroc.com. Tous droits réservés.

## Support

Pour les problèmes ou questions, veuillez contacter l'équipe de développement.
