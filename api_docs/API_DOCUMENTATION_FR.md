# Documentation API TalentsMaroc.com - Version 3.0

**Base URL**: `https://votre-domaine.com/api/v1`

**Format de réponse**: JSON

**Authentification**: Session-based (cookies)

**Protection CSRF**: Désactivée pour toutes les routes API v1

---

## 📋 Table des matières

1. [Authentification](#authentification)
2. [Gestion des utilisateurs](#gestion-des-utilisateurs)
3. [Talents et localisation](#talents-et-localisation)
4. [Module CINEMA](#module-cinema)
5. [Productions et Projets](#productions-et-projets)
6. [Système de Présence](#système-de-présence)
7. [Statistiques](#statistiques)
8. [Exports de données](#exports-de-données)
9. [Codes d'erreur](#codes-derreur)
10. [Interactions et Workflows](#interactions-et-workflows)

---

## 🔐 Authentification

### Connexion

**Endpoint**: `POST /api/v1/auth/login`

**Description**: Authentifie un utilisateur via email ou code unique. Crée une session côté serveur.

**Headers requis**:
```
Content-Type: application/json
```

**Requête**:
```json
{
  "identifier": "user@example.com",
  "password": "motdepasse123"
}
```

**Paramètres**:
- `identifier` (string, requis): Email OU code unique de l'utilisateur
- `password` (string, requis): Mot de passe (sera vérifié avec bcrypt)

**Réponse réussie** (200):
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 42,
    "email": "user@example.com",
    "unique_code": "MARAB0042M",
    "first_name": "Ahmed",
    "last_name": "Benali",
    "is_admin": false,
    "role": "user",
    "account_active": true
  }
}
```

**Réponse d'erreur** (401):
```json
{
  "success": false,
  "error": "Invalid credentials"
}
```

**Réponse d'erreur** (400):
```json
{
  "success": false,
  "error": "Missing required fields"
}
```

---

### Déconnexion

**Endpoint**: `POST /api/v1/auth/logout`

**Authentification**: Requise

**Description**: Déconnecte l'utilisateur et détruit la session côté serveur.

**Réponse réussie** (200):
```json
{
  "success": true,
  "message": "Logout successful"
}
```

---

### Utilisateur actuel

**Endpoint**: `GET /api/v1/auth/me`

**Authentification**: Requise

**Description**: Récupère les informations complètes de l'utilisateur connecté.

**Réponse réussie** (200):
```json
{
  "success": true,
  "user": {
    "id": 42,
    "email": "user@example.com",
    "unique_code": "MARAB0042M",
    "first_name": "Ahmed",
    "last_name": "Benali",
    "date_of_birth": "1990-05-15",
    "gender": "M",
    "phone": "+212600000000",
    "country": "Maroc",
    "city": "Rabat",
    "availability": "disponible_maintenant",
    "work_mode": "hybride",
    "rate_range": "50000-100000",
    "years_experience": 8,
    "bio": "Développeur Full Stack passionné...",
    "profile_score": 85,
    "is_admin": false,
    "role": "user",
    "account_active": true,
    "talents": [
      {
        "id": 18,
        "name": "Développement Web",
        "emoji": "💻",
        "category": "Technologie"
      }
    ],
    "social_media": {
      "linkedin": "https://linkedin.com/in/ahmedbenali",
      "github": "https://github.com/ahmedbenali"
    },
    "created_at": "2025-10-15T10:30:00",
    "updated_at": "2025-10-20T14:22:00"
  }
}
```

**Réponse d'erreur** (401):
```json
{
  "success": false,
  "error": "Authentication required"
}
```

---

## 👥 Gestion des utilisateurs

### Liste des utilisateurs

**Endpoint**: `GET /api/v1/users`

**Authentification**: Admin requis

**Paramètres de requête**:
- `search` (string, optionnel): Recherche par nom, email ou code
- `country_id` (integer, optionnel): Filtrer par pays
- `city_id` (integer, optionnel): Filtrer par ville
- `gender` (string, optionnel): `M`, `F`, ou `N`
- `availability` (string, optionnel): 
  - `disponible_maintenant`
  - `disponible_prochainement`
  - `non_disponible`
  - `projet_actuel`
- `work_mode` (string, optionnel):
  - `sur_site`
  - `a_distance`
  - `hybride`
  - `flexible`
- `has_cv` (boolean, optionnel): Filtre les utilisateurs avec CV
- `has_portfolio` (boolean, optionnel): Filtre les utilisateurs avec URL portfolio
- `page` (integer, défaut: 1): Numéro de page
- `limit` (integer, défaut: 20, max: 100): Résultats par page

**Exemple de requête**:
```
GET /api/v1/users?search=ahmed&country_id=1&availability=disponible_maintenant&page=1&limit=20
```

**Réponse réussie** (200):
```json
{
  "success": true,
  "total": 156,
  "page": 1,
  "limit": 20,
  "total_pages": 8,
  "users": [
    {
      "id": 42,
      "unique_code": "MARAB0042M",
      "first_name": "Ahmed",
      "last_name": "Benali",
      "email": "ahmed@example.com",
      "gender": "M",
      "age": 34,
      "availability": "disponible_maintenant",
      "work_mode": "hybride",
      "country": "Maroc",
      "city": "Rabat",
      "account_active": true,
      "profile_score": 85,
      "has_cv": true,
      "has_portfolio": true,
      "created_at": "2025-10-15T10:30:00",
      "talents": [
        {
          "id": 18,
          "name": "Développement Web",
          "emoji": "💻"
        },
        {
          "id": 25,
          "name": "Designer UI/UX",
          "emoji": "🎨"
        }
      ]
    }
  ]
}
```

---

### Détails d'un utilisateur

**Endpoint**: `GET /api/v1/users/:user_id`

**Authentification**: Requise (admin ou utilisateur propriétaire)

**Paramètres d'URL**:
- `user_id` (integer): ID de l'utilisateur

**Exemple**:
```
GET /api/v1/users/42
```

**Réponse réussie** (200):
```json
{
  "success": true,
  "user": {
    "id": 42,
    "unique_code": "MARAB0042M",
    "first_name": "Ahmed",
    "last_name": "Benali",
    "email": "ahmed@example.com",
    "date_of_birth": "1990-05-15",
    "gender": "M",
    "age": 34,
    "phone": "+212600000000",
    "whatsapp": "+212600000000",
    "address": "123 Avenue Mohammed V, Rabat",
    "country": "Maroc",
    "city": "Rabat",
    "bio": "Développeur Full Stack avec 8 ans d'expérience...",
    "years_experience": 8,
    "profile_score": 85,
    "availability": "disponible_maintenant",
    "work_mode": "hybride",
    "rate_range": "50000-100000",
    "portfolio_url": "https://ahmedbenali.com",
    "website": "https://ahmedbenali.com",
    "talents": [
      {
        "id": 18,
        "name": "Développement Web",
        "emoji": "💻",
        "category": "Technologie"
      }
    ],
    "social_media": {
      "linkedin": "https://linkedin.com/in/ahmedbenali",
      "github": "https://github.com/ahmedbenali",
      "twitter": "https://twitter.com/ahmedbenali"
    },
    "cv_analysis": {
      "summary": "Développeur senior avec expertise en React, Node.js...",
      "skills": ["React", "Node.js", "Python", "PostgreSQL"],
      "score": 85
    },
    "photo_url": "/static/uploads/photos/abc123.jpg",
    "cv_url": "/static/uploads/cvs/xyz789.pdf",
    "qr_code_url": "/static/uploads/qrcodes/qr_abc123.png",
    "account_active": true,
    "is_admin": false,
    "created_at": "2025-10-15T10:30:00",
    "updated_at": "2025-10-20T14:22:00"
  }
}
```

**Réponse d'erreur** (404):
```json
{
  "success": false,
  "error": "User not found"
}
```

**Réponse d'erreur** (403):
```json
{
  "success": false,
  "error": "Access denied"
}
```

---

### Mettre à jour un utilisateur

**Endpoint**: `PUT /api/v1/users/:user_id`

**Authentification**: Admin requis

**Requête**:
```json
{
  "availability": "disponible_maintenant",
  "work_mode": "a_distance",
  "rate_range": "75000-125000",
  "account_active": true
}
```

**Champs modifiables**:
- `availability`, `work_mode`, `rate_range`
- `bio`, `years_experience`
- `portfolio_url`, `website`
- `account_active` (admin uniquement)
- `is_admin` (super admin uniquement)

**Réponse réussie** (200):
```json
{
  "success": true,
  "message": "User updated successfully",
  "user": {
    "id": 42,
    "unique_code": "MARAB0042M",
    "first_name": "Ahmed",
    "last_name": "Benali",
    "availability": "disponible_maintenant"
  }
}
```

---

### Supprimer un utilisateur

**Endpoint**: `DELETE /api/v1/users/:user_id`

**Authentification**: Admin requis

**Description**: Supprime définitivement un utilisateur et toutes ses données associées.

**Réponse réussie** (200):
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

**Réponse d'erreur** (403):
```json
{
  "success": false,
  "error": "Cannot delete admin users"
}
```

---

### Activer/Désactiver un compte

**Endpoint**: `POST /api/v1/users/:user_id/toggle-active`

**Authentification**: Admin requis

**Réponse réussie** (200):
```json
{
  "success": true,
  "message": "User account activated",
  "account_active": true
}
```

---

## 🎭 Talents et localisation

### Liste des talents

**Endpoint**: `GET /api/v1/talents`

**Description**: Récupère tous les talents disponibles dans le catalogue.

**Réponse réussie** (200):
```json
{
  "success": true,
  "total": 73,
  "talents": [
    {
      "id": 1,
      "name": "Développement Web",
      "emoji": "💻",
      "category": "Technologie",
      "is_active": true,
      "user_count": 145
    },
    {
      "id": 2,
      "name": "Designer UI/UX",
      "emoji": "🎨",
      "category": "Créatif",
      "is_active": true,
      "user_count": 89
    }
  ],
  "categories": {
    "Technologie": 12,
    "Créatif": 18,
    "Business": 15
  }
}
```

---

### Détails d'un talent

**Endpoint**: `GET /api/v1/talents/:talent_id`

**Réponse réussie** (200):
```json
{
  "success": true,
  "talent": {
    "id": 1,
    "name": "Développement Web",
    "emoji": "💻",
    "category": "Technologie",
    "is_active": true,
    "user_count": 145,
    "users": [
      {
        "id": 42,
        "unique_code": "MARAB0042M",
        "first_name": "Ahmed",
        "last_name": "Benali",
        "availability": "disponible_maintenant"
      }
    ]
  }
}
```

---

### Liste des pays

**Endpoint**: `GET /api/v1/countries`

**Description**: Liste des 54 pays africains avec codes ISO-2 et drapeaux.

**Réponse réussie** (200):
```json
{
  "success": true,
  "total": 54,
  "countries": [
    {
      "id": 1,
      "name": "Maroc",
      "code": "MA",
      "flag": "🇲🇦",
      "user_count": 45,
      "cinema_talent_count": 12
    },
    {
      "id": 2,
      "name": "Sénégal",
      "code": "SN",
      "flag": "🇸🇳",
      "user_count": 23,
      "cinema_talent_count": 8
    }
  ]
}
```

---

### Liste des villes

**Endpoint**: `GET /api/v1/cities`

**Paramètres de requête**:
- `country_code` (string, optionnel): Code ISO-2 du pays (ex: MA)

**Exemple**:
```
GET /api/v1/cities?country_code=MA
```

**Réponse réussie** (200):
```json
{
  "success": true,
  "total": 12,
  "cities": [
    {
      "id": 1,
      "name": "Rabat",
      "code": "RAB",
      "country": "Maroc",
      "country_code": "MA",
      "user_count": 15
    },
    {
      "id": 2,
      "name": "Casablanca",
      "code": "CAS",
      "country": "Maroc",
      "country_code": "MA",
      "user_count": 22
    }
  ]
}
```

---

## 🎬 Module CINEMA

### Liste des talents CINEMA

**Endpoint**: `GET /api/v1/cinema/talents`

**Description**: Liste des talents CINEMA avec filtres avancés (13 critères).

**Paramètres de requête** (tous optionnels):
- `search` (string): Recherche globale (nom, email, téléphone, code, document)
- `talent_type` (string): Type de talent parmi:
  - `Acteur Principal`
  - `Acteur Secondaire`
  - `Figurant`
  - `Silhouette`
  - `Doublure`
  - `Doublure Lumière`
  - `Cascadeur`
  - `Mannequin`
  - `Voix Off`
  - `Figurant Spécialisé`
  - `Choriste`
  - `Danseur de fond`
  - `Autre`
- `gender` (string): `M` ou `F`
- `age_range` (string): Tranche d'âge
  - `18-25`
  - `26-35`
  - `36-50`
  - `51+`
- `ethnicity` (string): Ethnicité
- `eye_color` (string): Couleur des yeux (12 options)
- `hair_color` (string): Couleur des cheveux (16 options)
- `hair_type` (string): Type de cheveux (10 options)
- `skin_tone` (string): Teint de peau (10 options)
- `build` (string): Corpulence (10 options)
- `height_min` (integer): Taille minimum en cm
- `height_max` (integer): Taille maximum en cm
- `country` (string): Pays de résidence
- `language` (string): Langue parlée
- `page` (integer, défaut: 1): Numéro de page
- `limit` (integer, défaut: 20, max: 100): Résultats par page

**Exemple**:
```
GET /api/v1/cinema/talents?talent_type=Acteur Principal&gender=F&age_range=26-35&country=Maroc&page=1&limit=20
```

**Réponse réussie** (200):
```json
{
  "success": true,
  "total": 45,
  "page": 1,
  "limit": 20,
  "total_pages": 3,
  "talents": [
    {
      "id": 1,
      "unique_code": "MACAS0001F",
      "first_name": "Sophia",
      "last_name": "Martinez",
      "gender": "F",
      "age": 28,
      "email": "sophia@demo.cinema",
      "phone": "+212600111222",
      "talent_types": ["Acteur Principal", "Mannequin"],
      "physical_characteristics": {
        "height": 170,
        "eye_color": "Marron",
        "hair_color": "Noir",
        "hair_type": "Ondulé",
        "skin_tone": "Medium",
        "build": "Athlétique"
      },
      "languages": [
        {"code": "fr", "name": "Français", "flag": "🇫🇷"},
        {"code": "ar", "name": "Arabe", "flag": "🇸🇦"},
        {"code": "en", "name": "Anglais", "flag": "🇬🇧"}
      ],
      "location": {
        "country_of_origin": "Maroc",
        "nationality": "Marocaine",
        "country_of_residence": "Maroc",
        "city_of_residence": "Casablanca"
      },
      "experience": {
        "years": 8,
        "previous_productions": [
          {
            "title": "Casablanca Nights",
            "type": "Film",
            "year": "2022"
          }
        ]
      },
      "has_profile_photo": true,
      "has_id_photo": true,
      "gallery_count": 3,
      "qr_code_url": "/static/uploads/qrcodes/cinema_qr_xyz.png",
      "created_at": "2025-02-10T14:20:00"
    }
  ]
}
```

---

### Détails d'un talent CINEMA

**Endpoint**: `GET /api/v1/cinema/talents/:talent_id`

**Paramètres d'URL**:
- `talent_id` (integer): ID du talent CINEMA

**Exemple**:
```
GET /api/v1/cinema/talents/1
```

**Réponse réussie** (200):
```json
{
  "success": true,
  "talent": {
    "id": 1,
    "unique_code": "MACAS0001F",
    "first_name": "Sophia",
    "last_name": "Martinez",
    "gender": "F",
    "date_of_birth": "1996-03-15",
    "age": 28,
    "id_document": {
      "type": "Passeport",
      "number": "AB123456"
    },
    "contact": {
      "email": "sophia@demo.cinema",
      "phone": "+212600111222",
      "whatsapp": "+212600111222",
      "website": "https://sophiamartinez.com"
    },
    "origins": {
      "country_of_origin": "Maroc",
      "nationality": "Marocaine",
      "ethnicities": ["Africaine", "Arabe"]
    },
    "residence": {
      "country": "Maroc",
      "city": "Casablanca"
    },
    "languages": [
      {"code": "fr", "name": "Français", "flag": "🇫🇷"},
      {"code": "ar", "name": "Arabe", "flag": "🇸🇦"},
      {"code": "en", "name": "Anglais", "flag": "🇬🇧"}
    ],
    "talent_types": ["Acteur Principal", "Mannequin"],
    "physical_characteristics": {
      "height": 170,
      "eye_color": "Marron",
      "hair_color": "Noir",
      "hair_type": "Ondulé",
      "skin_tone": "Medium",
      "build": "Athlétique"
    },
    "other_talents": ["Chant", "Danse moderne", "Équitation"],
    "experience": {
      "years": 8,
      "previous_productions": [
        {
          "title": "Casablanca Nights",
          "type": "Film",
          "year": "2022"
        },
        {
          "title": "Desert Dreams",
          "type": "Série TV",
          "year": "2021"
        }
      ]
    },
    "social_media": {
      "facebook": "https://facebook.com/sophiamartinez",
      "instagram": "https://instagram.com/sophiamartinez",
      "tiktok": "https://tiktok.com/@sophiamartinez"
    },
    "media": {
      "profile_photo": "/static/uploads/cinema/profile_xyz.jpg",
      "id_photo": "/static/uploads/cinema/id_abc.jpg",
      "gallery": [
        "/static/uploads/cinema/gallery_1_def.jpg",
        "/static/uploads/cinema/gallery_2_ghi.jpg",
        "/static/uploads/cinema/gallery_3_jkl.jpg"
      ],
      "qr_code": "/static/uploads/qrcodes/cinema_qr_xyz.png"
    },
    "created_at": "2025-02-10T14:20:00",
    "updated_at": "2025-10-15T09:12:00"
  }
}
```

---

### Statistiques CINEMA

**Endpoint**: `GET /api/v1/cinema/stats`

**Réponse réussie** (200):
```json
{
  "success": true,
  "stats": {
    "total_talents": 45,
    "by_type": {
      "Acteur Principal": 12,
      "Acteur Secondaire": 8,
      "Figurant": 15,
      "Mannequin": 6,
      "Autre": 4
    },
    "by_gender": {
      "M": 23,
      "F": 22
    },
    "by_age_range": {
      "18-25": 10,
      "26-35": 18,
      "36-50": 12,
      "51+": 5
    },
    "by_country": {
      "Maroc": 35,
      "Sénégal": 6,
      "Côte d'Ivoire": 4
    },
    "top_languages": [
      {"language": "Français", "count": 40},
      {"language": "Arabe", "count": 38},
      {"language": "Anglais", "count": 25}
    ],
    "with_photos": 40,
    "without_photos": 5,
    "with_experience": 35,
    "without_experience": 10,
    "average_age": 32.5,
    "average_height": 172
  }
}
```

---

## 🎥 Productions et Projets

### Liste des productions

**Endpoint**: `GET /api/v1/cinema/productions`

**Paramètres de requête**:
- `is_active` (boolean, optionnel): Filtre productions actives
- `is_verified` (boolean, optionnel): Filtre productions vérifiées
- `country` (string, optionnel): Pays de la production
- `page` (integer, défaut: 1)
- `limit` (integer, défaut: 20, max: 100)

**Réponse réussie** (200):
```json
{
  "success": true,
  "total": 12,
  "page": 1,
  "limit": 20,
  "productions": [
    {
      "id": 1,
      "name": "Morocco Films Production",
      "description": "Société de production spécialisée dans le cinéma marocain",
      "specialization": "Films, Séries, Documentaires",
      "country": "Maroc",
      "city": "Casablanca",
      "founded_year": 2005,
      "ceo": "Youssef Alami",
      "employees_count": 45,
      "productions_count": 28,
      "is_verified": true,
      "is_active": true,
      "contact": {
        "email": "info@moroccofilms.ma",
        "phone": "+212522000000",
        "website": "https://moroccofilms.ma"
      },
      "social_media": {
        "facebook": "https://facebook.com/moroccofilms",
        "instagram": "https://instagram.com/moroccofilms"
      },
      "created_at": "2024-01-10T09:00:00"
    }
  ]
}
```

---

### Détails d'une production

**Endpoint**: `GET /api/v1/cinema/productions/:production_id`

**Réponse réussie** (200):
```json
{
  "success": true,
  "production": {
    "id": 1,
    "name": "Morocco Films Production",
    "logo_url": "https://moroccofilms.ma/logo.png",
    "description": "Société de production leader au Maroc",
    "specialization": "Films, Séries, Documentaires",
    "address": "123 Boulevard Mohammed V",
    "city": "Casablanca",
    "country": "Maroc",
    "postal_code": "20000",
    "founded_year": 2005,
    "ceo": "Youssef Alami",
    "employees_count": 45,
    "productions_count": 28,
    "notable_productions": [
      {"title": "Le Grand Voyage", "year": 2020},
      {"title": "Nuits de Casablanca", "year": 2022}
    ],
    "services": [
      "Production",
      "Post-production",
      "Distribution",
      "Location de matériel"
    ],
    "equipment": "Caméras RED, Sony, Drones DJI, Éclairage complet",
    "studios": "2 studios de 500m² et 800m²",
    "certifications": [
      "ISO 9001",
      "CCM Certifié"
    ],
    "memberships": [
      "FIPCA",
      "Chambre Marocaine des Producteurs"
    ],
    "awards": [
      {"title": "Prix du Meilleur Film", "year": 2021},
      {"title": "Grand Prix du Festival", "year": 2022}
    ],
    "is_active": true,
    "is_verified": true,
    "active_projects_count": 3,
    "total_projects_count": 12,
    "created_at": "2024-01-10T09:00:00"
  }
}
```

---

### Liste des projets

**Endpoint**: `GET /api/v1/cinema/projects`

**Paramètres de requête**:
- `production_id` (integer, optionnel): Filtrer par production
- `status` (string, optionnel): Statut du projet
  - `en_preparation`
  - `en_tournage`
  - `post_production`
  - `termine`
- `production_type` (string, optionnel): Type de production
- `is_active` (boolean, optionnel)
- `page` (integer, défaut: 1)
- `limit` (integer, défaut: 20)

**Réponse réussie** (200):
```json
{
  "success": true,
  "total": 8,
  "page": 1,
  "limit": 20,
  "projects": [
    {
      "id": 1,
      "name": "Le Dernier Voyage",
      "production_type": "Film",
      "production_company": {
        "id": 1,
        "name": "Morocco Films Production"
      },
      "origin_country": "Maroc",
      "shooting_locations": "Marrakech, Essaouira, Atlas",
      "start_date": "2025-11-01",
      "end_date": "2025-12-31",
      "status": "en_preparation",
      "is_active": true,
      "assigned_talents_count": 15,
      "created_at": "2025-09-15T10:00:00"
    }
  ]
}
```

---

### Détails d'un projet

**Endpoint**: `GET /api/v1/cinema/projects/:project_id`

**Réponse réussie** (200):
```json
{
  "success": true,
  "project": {
    "id": 1,
    "name": "Le Dernier Voyage",
    "production_type": "Film",
    "production_company": {
      "id": 1,
      "name": "Morocco Films Production",
      "logo_url": "https://moroccofilms.ma/logo.png"
    },
    "origin_country": "Maroc",
    "shooting_locations": "Marrakech, Essaouira, Atlas",
    "start_date": "2025-11-01",
    "end_date": "2025-12-31",
    "status": "en_preparation",
    "is_active": true,
    "assigned_talents": [
      {
        "id": 1,
        "project_talent_id": 10,
        "unique_code": "MACAS0001F",
        "first_name": "Sophia",
        "last_name": "Martinez",
        "talent_type": "Acteur Principal",
        "role_description": "Rôle principal féminin",
        "project_code": "PRJ001001",
        "badge_generated": true,
        "assigned_at": "2025-09-20T14:00:00"
      }
    ],
    "created_by": {
      "id": 1,
      "email": "admin@talento.com",
      "first_name": "Admin"
    },
    "created_at": "2025-09-15T10:00:00",
    "updated_at": "2025-10-01T16:30:00"
  }
}
```

---

## 📊 Système de Présence

### Enregistrer présence (check-in/check-out)

**Endpoint**: `POST /api/v1/presence/record`

**Authentification**: Requise (admin ou rôle "presence")

**Requête**:
```json
{
  "project_id": 1,
  "cinema_talent_code": "MACAS0001F",
  "action": "check_in"
}
```

**Paramètres**:
- `project_id` (integer, requis): ID du projet
- `cinema_talent_code` (string, requis): Code unique du talent CINEMA
- `action` (string, requis): `check_in` ou `check_out`

**Réponse réussie** (200):
```json
{
  "success": true,
  "message": "Check-in recorded successfully",
  "attendance": {
    "id": 42,
    "project_id": 1,
    "cinema_talent_code": "MACAS0001F",
    "date": "2025-10-26",
    "check_in_time": "2025-10-26T08:30:00",
    "check_out_time": null,
    "recorded_by": "admin@talento.com"
  }
}
```

---

### Pointer tous présents

**Endpoint**: `POST /api/v1/presence/check-in-all/:project_id`

**Authentification**: Requise (admin ou rôle "presence")

**Réponse réussie** (200):
```json
{
  "success": true,
  "message": "15 talents marked as present",
  "count": 15
}
```

---

### Pointer toutes les sorties

**Endpoint**: `POST /api/v1/presence/check-out-all/:project_id`

**Authentification**: Requise (admin ou rôle "presence")

**Réponse réussie** (200):
```json
{
  "success": true,
  "message": "12 departures recorded",
  "count": 12
}
```

---

### Historique de présence d'un talent

**Endpoint**: `GET /api/v1/presence/history/:cinema_talent_code`

**Paramètres de requête**:
- `project_id` (integer, optionnel): Filtrer par projet
- `date_from` (date, optionnel): Date de début (YYYY-MM-DD)
- `date_to` (date, optionnel): Date de fin (YYYY-MM-DD)
- `page` (integer, défaut: 1)
- `limit` (integer, défaut: 50)

**Réponse réussie** (200):
```json
{
  "success": true,
  "talent": {
    "unique_code": "MACAS0001F",
    "first_name": "Sophia",
    "last_name": "Martinez"
  },
  "total": 45,
  "page": 1,
  "limit": 50,
  "attendance_records": [
    {
      "id": 42,
      "project": {
        "id": 1,
        "name": "Le Dernier Voyage"
      },
      "date": "2025-10-26",
      "check_in_time": "08:30:00",
      "check_out_time": "18:45:00",
      "duration_hours": 10.25,
      "recorded_by": "admin@talento.com"
    }
  ],
  "statistics": {
    "total_days": 45,
    "total_hours": 452.5,
    "average_hours_per_day": 10.05
  }
}
```

---

## 📈 Statistiques

### Vue d'ensemble

**Endpoint**: `GET /api/v1/stats/overview`

**Authentification**: Admin requis

**Réponse réussie** (200):
```json
{
  "success": true,
  "stats": {
    "users": {
      "total": 250,
      "active": 230,
      "inactive": 20,
      "new_last_7_days": 15,
      "new_last_30_days": 52
    },
    "cinema": {
      "total_talents": 45,
      "total_productions": 12,
      "total_projects": 8,
      "active_projects": 3
    },
    "profile_completion": {
      "average": 75.5,
      "complete_profiles": 180,
      "incomplete_profiles": 70
    },
    "talents": {
      "total_categories": 73,
      "most_popular": [
        {"name": "Développement Web", "count": 45},
        {"name": "Designer", "count": 32}
      ]
    },
    "geographic": {
      "countries": 18,
      "cities": 45,
      "top_countries": [
        {"name": "Maroc", "count": 120},
        {"name": "Sénégal", "count": 45}
      ]
    }
  },
  "generated_at": "2025-10-26T15:30:00"
}
```

---

### Statistiques utilisateurs

**Endpoint**: `GET /api/v1/stats/users`

**Authentification**: Admin requis

**Paramètres de requête**:
- `period` (string, optionnel): `7d`, `30d`, `90d`, `1y`

**Réponse réussie** (200):
```json
{
  "success": true,
  "stats": {
    "total": 250,
    "by_availability": {
      "disponible_maintenant": 120,
      "disponible_prochainement": 80,
      "non_disponible": 30,
      "projet_actuel": 20
    },
    "by_work_mode": {
      "sur_site": 60,
      "a_distance": 100,
      "hybride": 70,
      "flexible": 20
    },
    "by_country": {
      "Maroc": 120,
      "Sénégal": 45,
      "Côte d'Ivoire": 35
    },
    "by_gender": {
      "M": 150,
      "F": 90,
      "N": 10
    },
    "with_cv": 200,
    "without_cv": 50,
    "with_portfolio": 180,
    "average_experience_years": 5.8,
    "average_profile_score": 72.3
  }
}
```

---

### Statistiques talents

**Endpoint**: `GET /api/v1/stats/talents`

**Authentification**: Admin requis

**Réponse réussie** (200):
```json
{
  "success": true,
  "stats": {
    "total_categories": 73,
    "by_category": {
      "Technologie": 120,
      "Créatif": 89,
      "Business": 56,
      "Éducation": 34
    },
    "top_10": [
      {"id": 1, "name": "Développement Web", "emoji": "💻", "count": 45},
      {"id": 2, "name": "Designer UI/UX", "emoji": "🎨", "count": 32}
    ]
  }
}
```

---

## 📥 Exports de données

### Export Excel utilisateurs

**Endpoint**: `GET /api/v1/export/users/excel`

**Authentification**: Admin requis

**Paramètres de requête**: Mêmes filtres que `/api/v1/users`

**Réponse**: Fichier Excel (.xlsx)

**Headers de réponse**:
```
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename=users_export_20251026.xlsx
```

---

### Export CSV utilisateurs

**Endpoint**: `GET /api/v1/export/users/csv`

**Authentification**: Admin requis

**Paramètres de requête**: Mêmes filtres que `/api/v1/users`

**Réponse**: Fichier CSV

**Headers de réponse**:
```
Content-Type: text/csv; charset=utf-8
Content-Disposition: attachment; filename=users_export_20251026.csv
```

---

### Export Excel CINEMA

**Endpoint**: `GET /api/v1/export/cinema/excel`

**Authentification**: Admin requis

**Paramètres de requête**: Mêmes filtres que `/api/v1/cinema/talents`

**Réponse**: Fichier Excel (.xlsx) avec toutes les données CINEMA

---

### Export PDF talent CINEMA

**Endpoint**: `GET /api/v1/cinema/talents/:talent_id/pdf`

**Authentification**: Requise

**Réponse**: Fichier PDF professionnel du profil talent

**Headers de réponse**:
```
Content-Type: application/pdf
Content-Disposition: attachment; filename=talent_MACAS0001F.pdf
```

---

## ❌ Codes d'erreur

### Codes HTTP standard

| Code | Description | Utilisation |
|------|-------------|-------------|
| 200 | OK | Requête réussie |
| 201 | Created | Ressource créée avec succès |
| 204 | No Content | Succès sans contenu de retour |
| 400 | Bad Request | Données invalides ou manquantes |
| 401 | Unauthorized | Authentification requise ou échouée |
| 403 | Forbidden | Accès interdit (droits insuffisants) |
| 404 | Not Found | Ressource introuvable |
| 409 | Conflict | Conflit (ex: email déjà existant) |
| 422 | Unprocessable Entity | Validation échouée |
| 429 | Too Many Requests | Limite de taux dépassée |
| 500 | Internal Server Error | Erreur serveur |

### Format des erreurs

Toutes les réponses d'erreur suivent ce format:

```json
{
  "success": false,
  "error": "Message d'erreur lisible",
  "code": "ERROR_CODE",
  "details": {
    "field": "Description de l'erreur du champ"
  }
}
```

### Exemples d'erreurs courantes

**Authentification requise** (401):
```json
{
  "success": false,
  "error": "Authentication required",
  "code": "AUTH_REQUIRED"
}
```

**Données invalides** (400):
```json
{
  "success": false,
  "error": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": {
    "email": "Format d'email invalide",
    "password": "Le mot de passe doit contenir au moins 8 caractères"
  }
}
```

**Accès refusé** (403):
```json
{
  "success": false,
  "error": "Admin access required",
  "code": "FORBIDDEN"
}
```

**Ressource introuvable** (404):
```json
{
  "success": false,
  "error": "User not found",
  "code": "NOT_FOUND"
}
```

**Conflit** (409):
```json
{
  "success": false,
  "error": "Email already exists",
  "code": "DUPLICATE_EMAIL"
}
```

---

## 🔄 Interactions et Workflows

### Workflow 1: Inscription et Profil Utilisateur

```
1. POST /api/v1/auth/register (Web uniquement - pas disponible en API)
   → Crée l'utilisateur avec code unique PPGNNNNVVV
   → Hash du mot de passe (bcrypt)
   → Chiffrement des données sensibles (Fernet)
   → Génération du QR code
   → Email de bienvenue (si configuré)

2. POST /api/v1/auth/login
   → Authentification (email OU code unique)
   → Création de session
   
3. GET /api/v1/auth/me
   → Récupération du profil complet
   
4. PUT /api/v1/users/:user_id
   → Mise à jour du profil
```

### Workflow 2: Inscription Talent CINEMA

```
1. POST /cinema/register (Web uniquement - formulaire public)
   → Création du talent avec code unique PPVVVNNNNNG
   → Upload de photos (profil, ID, galerie)
   → Chiffrement des données sensibles
   → Génération du QR code
   → Email de confirmation

2. GET /api/v1/cinema/talents/:talent_id
   → Récupération du profil CINEMA complet
   
3. GET /api/v1/cinema/talents/:talent_id/pdf
   → Export PDF professionnel
```

### Workflow 3: Création de Projet et Assignation

```
1. POST /cinema/projects/new (Web uniquement)
   → Création du projet
   → Association à une production
   
2. POST /cinema/projects/:id/assign-talent (Web uniquement)
   → Génération du code projet (PRJXXXYYY)
   → Assignation du talent au projet
   → Badge généré automatiquement
   
3. GET /api/v1/cinema/projects/:project_id
   → Récupération du projet avec tous les talents assignés
```

### Workflow 4: Gestion de Présence

```
1. POST /api/v1/presence/record
   {
     "project_id": 1,
     "cinema_talent_code": "MACAS0001F",
     "action": "check_in"
   }
   → Premier scan de la journée = Arrivée
   
2. POST /api/v1/presence/record
   {
     "project_id": 1,
     "cinema_talent_code": "MACAS0001F",
     "action": "check_out"
   }
   → Deuxième scan = Départ
   
3. GET /api/v1/presence/history/MACAS0001F?project_id=1
   → Historique complet avec durées calculées
   
4. GET /api/v1/presence/export/:project_id (Web uniquement)
   → Export Excel des présences
```

### Workflow 5: Recherche et Filtrage Avancé

```
1. GET /api/v1/cinema/talents?talent_type=Acteur Principal&gender=F&age_range=26-35&country=Maroc
   → Recherche multicritères (13 filtres combinables)
   
2. GET /api/v1/cinema/talents/:talent_id
   → Détails complets du talent sélectionné
   
3. POST /cinema/projects/:id/assign-talent (Web uniquement)
   → Assignation au projet
```

### Workflow 6: Statistiques et Exports

```
1. GET /api/v1/stats/overview
   → Vue d'ensemble globale
   
2. GET /api/v1/stats/cinema
   → Statistiques détaillées CINEMA
   
3. GET /api/v1/export/cinema/excel?talent_type=Acteur Principal
   → Export filtré des talents
```

---

## 🔒 Sécurité et Bonnes Pratiques

### Authentification

- **Sessions**: Utilisez les cookies de session pour toutes les requêtes authentifiées
- **HTTPS**: Toujours utiliser HTTPS en production
- **Expiration**: Les sessions expirent après 24h d'inactivité

### Chiffrement des données

- **Données chiffrées** (Fernet AES-128):
  - Numéros de téléphone et WhatsApp
  - Adresses postales
  - Tous les réseaux sociaux
  - Numéros de documents d'identité (CINEMA)

- **Données hashées** (bcrypt 12 rounds):
  - Mots de passe utilisateurs

### Limites de taux

| Endpoint | Limite |
|----------|--------|
| POST /api/v1/auth/login | 5 tentatives / 15 min |
| GET /api/v1/* | 1000 requêtes / heure |
| POST /api/v1/* | 500 requêtes / heure |
| Exports | 10 exports / heure |

### Upload de fichiers

| Type | Formats | Taille Max |
|------|---------|------------|
| Photos | PNG, JPG, JPEG | 5 MB |
| CVs | PDF, DOC, DOCX | 10 MB |

---

## 📚 Ressources Additionnelles

- **Documentation Technique**: `/docs/TECHNICAL_DOCUMENTATION.md`
- **Documentation des Routes**: `/docs/ROUTES_DOCUMENTATION.md`
- **Code Source**: GitHub (privé)

---

**Version**: 3.0  
**Dernière mise à jour**: 26 Octobre 2025  
**Auteur**: MOA Digital Agency LLC - Aisance KALONJI  
**Contact**: moa@myoneart.com
