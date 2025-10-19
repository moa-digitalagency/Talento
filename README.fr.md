# Talento - Plateforme de Centralisation des Talents

Talento est une application web professionnelle conçue pour centraliser et mettre en valeur les profils de talents à travers l'Afrique. La plateforme permet aux individus de créer des profils professionnels détaillés, de mettre en avant leurs compétences et de se connecter aux opportunités.

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

- **Email**: admin@talento.com
- **Mot de passe**: @4dm1n

⚠️ **Important**: Changez le mot de passe admin après la première connexion !

### Comptes de Démonstration

Le système inclut 5 comptes utilisateur de démonstration pour les tests:
- demo1@talento.com à demo5@talento.com
- Mot de passe: demo123

## Structure du Projet

```
talento/
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

### Système d'ID Unique
Chaque utilisateur reçoit un code unique de 10 caractères au format:
`CC-CCC-NNNN-G`
- CC: Code du pays
- CCC: Code de la ville
- NNNN: Numéro séquentiel
- G: Genre (M/F/N)

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

© 2024 Talento. Tous droits réservés.

## Support

Pour les problèmes ou questions, veuillez contacter l'équipe de développement.
