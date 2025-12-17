# Reference API Complete - taalentio.com

**Documentation technique de l'API REST v1**
**Version 2.0 | Decembre 2024**

---

## Table des matieres

1. [Introduction](#introduction)
2. [Authentification](#authentification)
3. [Endpoints Utilisateurs](#endpoints-utilisateurs)
4. [Endpoints Talents](#endpoints-talents)
5. [Endpoints CINEMA](#endpoints-cinema)
6. [Endpoints Statistiques](#endpoints-statistiques)
7. [Endpoints Exports](#endpoints-exports)
8. [Endpoints Internes](#endpoints-internes)
9. [Codes d'erreur](#codes-derreur)
10. [Exemples d'integration](#exemples-dintegration)

---

## Introduction

### Base URL

```
https://votre-domaine.com/api/v1
```

### Format des reponses

Toutes les reponses sont au format JSON.

**Structure standard :**
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation reussie"
}
```

**Structure d'erreur :**
```json
{
  "success": false,
  "error": "Description de l'erreur",
  "code": "ERROR_CODE"
}
```

### Headers requis

```
Content-Type: application/json
Accept: application/json
```

### Pagination

Les endpoints listes supportent la pagination :

| Parametre | Type | Default | Description |
|-----------|------|---------|-------------|
| page | int | 1 | Numero de page |
| per_page | int | 20 | Elements par page (max 100) |

**Reponse paginee :**
```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "pages": 8
}
```

---

## Authentification

L'API utilise une authentification basee sur les sessions (cookies).

### Login

**Endpoint :** `POST /api/v1/auth/login`

**Body :**
```json
{
  "email": "user@example.com",
  "password": "motdepasse"
}
```

**Reponse 200 :**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "unique_code": "MAM0001RAB",
    "first_name": "Jean",
    "last_name": "Dupont",
    "is_admin": false,
    "role": "user"
  }
}
```

**Reponse 401 :**
```json
{
  "success": false,
  "error": "Identifiants invalides"
}
```

### Logout

**Endpoint :** `POST /api/v1/auth/logout`

**Reponse 200 :**
```json
{
  "success": true,
  "message": "Deconnexion reussie"
}
```

### Verification session

**Endpoint :** `GET /api/v1/auth/me`

**Reponse 200 (connecte) :**
```json
{
  "success": true,
  "authenticated": true,
  "user": { ... }
}
```

**Reponse 200 (non connecte) :**
```json
{
  "success": true,
  "authenticated": false
}
```

---

## Endpoints Utilisateurs

### Liste des utilisateurs

**Endpoint :** `GET /api/v1/users`

**Parametres query :**
| Parametre | Type | Description |
|-----------|------|-------------|
| page | int | Numero de page |
| per_page | int | Elements par page |
| search | string | Recherche nom/email |
| country_id | int | Filtrer par pays |
| city_id | int | Filtrer par ville |
| gender | string | Filtrer par genre (M/F/N) |
| availability | string | Filtrer par disponibilite |
| talent_id | int | Filtrer par talent |

**Reponse 200 :**
```json
{
  "success": true,
  "users": [
    {
      "id": 1,
      "unique_code": "MAM0001RAB",
      "first_name": "Jean",
      "last_name": "Dupont",
      "email": "jean@example.com",
      "gender": "M",
      "age": 32,
      "country": {
        "id": 1,
        "name": "Maroc",
        "code": "MA"
      },
      "city": {
        "id": 1,
        "name": "Rabat",
        "code": "RAB"
      },
      "photo_url": "/static/uploads/photos/abc123.jpg",
      "talents": [
        {
          "id": 1,
          "name": "Developpement Web",
          "emoji": "🖥️",
          "category": "Technologie"
        }
      ],
      "availability": "Temps plein",
      "profile_score": 85,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "pages": 8
}
```

### Detail utilisateur

**Endpoint :** `GET /api/v1/users/{id}`

**Reponse 200 :**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "unique_code": "MAM0001RAB",
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean@example.com",
    "phone": "+212600000000",
    "whatsapp": "+212600000000",
    "date_of_birth": "1992-05-15",
    "age": 32,
    "gender": "M",
    "nationality": "Marocaine",
    "bio": "Developpeur full-stack avec 5 ans d'experience",
    "years_experience": 5,
    "education": "Master en Informatique",
    "languages": "Francais, Anglais, Arabe",
    "availability": "Temps plein",
    "work_mode": "hybrid",
    "rate_range": "500 MAD/h | 8000 MAD/mois",
    "country": { ... },
    "city": { ... },
    "residence_country": { ... },
    "residence_city": { ... },
    "talents": [ ... ],
    "photo_url": "/static/uploads/photos/abc123.jpg",
    "cv_url": "/static/uploads/cvs/cv123.pdf",
    "qr_code_url": "/static/uploads/qrcodes/MAM0001RAB.png",
    "portfolio_url": "https://portfolio.example.com",
    "website": "https://example.com",
    "linkedin": "https://linkedin.com/in/user",
    "instagram": "https://instagram.com/user",
    "profile_score": 85,
    "account_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-06-20T14:45:00Z"
  }
}
```

### Mise a jour utilisateur (Admin)

**Endpoint :** `PUT /api/v1/users/{id}`

**Body :**
```json
{
  "first_name": "Jean",
  "last_name": "Dupont",
  "phone": "+212600000001",
  "bio": "Nouvelle biographie",
  "availability": "Flexible",
  "account_active": true
}
```

**Reponse 200 :**
```json
{
  "success": true,
  "message": "Utilisateur mis a jour",
  "user": { ... }
}
```

### Suppression utilisateur (Admin)

**Endpoint :** `DELETE /api/v1/users/{id}`

**Reponse 200 :**
```json
{
  "success": true,
  "message": "Utilisateur supprime"
}
```

### Utilisateur par code unique

**Endpoint :** `GET /api/v1/users/code/{unique_code}`

**Reponse 200 :**
```json
{
  "success": true,
  "user": { ... }
}
```

---

## Endpoints Talents

### Liste des talents

**Endpoint :** `GET /api/v1/talents`

**Parametres query :**
| Parametre | Type | Description |
|-----------|------|-------------|
| tag | string | Filtrer par tag (general/cinema) |
| category | string | Filtrer par categorie |

**Reponse 200 :**
```json
{
  "success": true,
  "talents": [
    {
      "id": 1,
      "name": "Developpement Web",
      "emoji": "🖥️",
      "category": "Technologie",
      "tag": "general",
      "is_active": true,
      "users_count": 45
    }
  ],
  "total": 150
}
```

### Detail talent

**Endpoint :** `GET /api/v1/talents/{id}`

**Reponse 200 :**
```json
{
  "success": true,
  "talent": {
    "id": 1,
    "name": "Developpement Web",
    "emoji": "🖥️",
    "category": "Technologie",
    "tag": "general",
    "is_active": true,
    "users_count": 45
  }
}
```

### Utilisateurs par talent

**Endpoint :** `GET /api/v1/talents/{id}/users`

**Reponse 200 :**
```json
{
  "success": true,
  "talent": { ... },
  "users": [ ... ],
  "total": 45
}
```

---

## Endpoints CINEMA

### Liste talents CINEMA

**Endpoint :** `GET /api/v1/cinema/talents`

**Parametres query :**
| Parametre | Type | Description |
|-----------|------|-------------|
| page | int | Numero de page |
| per_page | int | Elements par page |
| search | string | Recherche nom |
| gender | string | Filtrer par genre |
| talent_type | string | Type de talent cinema |
| age_min | int | Age minimum |
| age_max | int | Age maximum |
| eye_color | string | Couleur des yeux |
| hair_color | string | Couleur de cheveux |
| skin_tone | string | Teint |
| height_min | int | Taille minimum (cm) |
| height_max | int | Taille maximum (cm) |
| country | string | Pays de residence |
| language | string | Langue parlee |
| experience | string | Niveau d'experience |

**Reponse 200 :**
```json
{
  "success": true,
  "talents": [
    {
      "id": 1,
      "unique_code": "MACAS000001F",
      "first_name": "Fatima",
      "last_name": "Benani",
      "gender": "F",
      "age": 28,
      "nationality": "Marocaine",
      "country_of_residence": "Maroc",
      "city_of_residence": "Casablanca",
      "height": 168,
      "eye_color": "Marron",
      "hair_color": "Noir",
      "hair_type": "Ondules",
      "skin_tone": "Mat",
      "build": "Svelte",
      "talent_types": ["Actrice Principale", "Mannequin"],
      "languages_spoken": ["Francais", "Arabe", "Anglais"],
      "years_of_experience": 5,
      "profile_photo_url": "/static/uploads/cinema_photos/abc.jpg",
      "email": "fatima@example.com",
      "created_at": "2024-02-10T09:00:00Z"
    }
  ],
  "total": 250,
  "page": 1,
  "per_page": 20,
  "pages": 13
}
```

### Detail talent CINEMA

**Endpoint :** `GET /api/v1/cinema/talents/{id}`

**Reponse 200 :**
```json
{
  "success": true,
  "talent": {
    "id": 1,
    "unique_code": "MACAS000001F",
    "first_name": "Fatima",
    "last_name": "Benani",
    "gender": "F",
    "date_of_birth": "1996-03-20",
    "age": 28,
    "id_document_type": "CIN",
    "id_document_initials": "AB***23",
    "ethnicities": ["Arabe", "Berbere"],
    "nationality": "Marocaine",
    "country_of_origin": "Maroc",
    "country_of_residence": "Maroc",
    "city_of_residence": "Casablanca",
    "height": 168,
    "eye_color": "Marron",
    "hair_color": "Noir",
    "hair_type": "Ondules",
    "skin_tone": "Mat",
    "build": "Svelte",
    "talent_types": ["Actrice Principale", "Mannequin"],
    "other_talents": ["Danse contemporaine", "Chant"],
    "languages_spoken": ["Francais", "Arabe", "Anglais"],
    "years_of_experience": 5,
    "previous_productions": "Film X (2022), Serie Y (2023)",
    "profile_photo_url": "/static/uploads/cinema_photos/abc.jpg",
    "gallery_photos": [
      "/static/uploads/cinema_photos/g1.jpg",
      "/static/uploads/cinema_photos/g2.jpg"
    ],
    "email": "fatima@example.com",
    "phone": "+212600000000",
    "whatsapp": "+212600000000",
    "website": "https://fatima.com",
    "instagram": "https://instagram.com/fatima",
    "qr_code_url": "/static/uploads/qrcodes/MACAS000001F.png",
    "is_active": true,
    "created_at": "2024-02-10T09:00:00Z",
    "updated_at": "2024-06-15T11:30:00Z"
  }
}
```

### Talent CINEMA par code

**Endpoint :** `GET /api/v1/cinema/talents/code/{unique_code}`

### Liste productions

**Endpoint :** `GET /api/v1/cinema/productions`

**Reponse 200 :**
```json
{
  "success": true,
  "productions": [
    {
      "id": 1,
      "name": "Atlas Productions",
      "logo_url": "/static/uploads/logos/atlas.png",
      "description": "Societe de production cinematographique",
      "specialization": "Films, Series",
      "city": "Casablanca",
      "country": "Maroc",
      "founded_year": 2010,
      "employees_count": 50,
      "productions_count": 25,
      "is_verified": true,
      "email": "contact@atlas.ma",
      "website": "https://atlas.ma"
    }
  ],
  "total": 15
}
```

### Liste projets

**Endpoint :** `GET /api/v1/cinema/projects`

**Parametres query :**
| Parametre | Type | Description |
|-----------|------|-------------|
| status | string | Filtrer par statut |
| production_id | int | Filtrer par production |

**Reponse 200 :**
```json
{
  "success": true,
  "projects": [
    {
      "id": 1,
      "name": "Le Desert Blanc",
      "production_type": "Film",
      "production_company": {
        "id": 1,
        "name": "Atlas Productions"
      },
      "origin_country": "Maroc",
      "shooting_locations": "Ouarzazate, Marrakech",
      "start_date": "2024-09-01",
      "end_date": "2024-12-15",
      "status": "en_tournage",
      "status_display": "En tournage",
      "talents_count": 45
    }
  ],
  "total": 8
}
```

### Detail projet

**Endpoint :** `GET /api/v1/cinema/projects/{id}`

**Reponse 200 :**
```json
{
  "success": true,
  "project": {
    "id": 1,
    "name": "Le Desert Blanc",
    "production_type": "Film",
    "production_company": { ... },
    "origin_country": "Maroc",
    "shooting_locations": "Ouarzazate, Marrakech",
    "start_date": "2024-09-01",
    "end_date": "2024-12-15",
    "status": "en_tournage",
    "is_active": true,
    "assigned_talents": [
      {
        "id": 1,
        "project_code": "PRJ-001-042",
        "talent": {
          "unique_code": "MACAS000001F",
          "first_name": "Fatima",
          "last_name": "Benani"
        },
        "talent_type": "Actrice Principale",
        "role_description": "Role de la protagoniste",
        "assigned_at": "2024-08-15T10:00:00Z"
      }
    ],
    "created_at": "2024-07-01T08:00:00Z"
  }
}
```

---

## Endpoints Statistiques

### Vue d'ensemble

**Endpoint :** `GET /api/v1/stats/overview`

**Reponse 200 :**
```json
{
  "success": true,
  "stats": {
    "total_users": 500,
    "total_cinema_talents": 250,
    "total_productions": 15,
    "total_projects": 8,
    "active_projects": 5,
    "new_users_7d": 25,
    "new_cinema_7d": 12
  }
}
```

### Statistiques utilisateurs

**Endpoint :** `GET /api/v1/stats/users`

**Reponse 200 :**
```json
{
  "success": true,
  "stats": {
    "total": 500,
    "active": 480,
    "inactive": 20,
    "by_gender": {
      "M": 280,
      "F": 200,
      "N": 20
    },
    "by_country": [
      { "country": "Maroc", "count": 200 },
      { "country": "Senegal", "count": 80 },
      { "country": "Cote d'Ivoire", "count": 60 }
    ],
    "top_talents": [
      { "talent": "Developpement Web", "count": 45 },
      { "talent": "Graphisme", "count": 38 }
    ],
    "avg_profile_score": 72,
    "with_photo_pct": 85,
    "with_cv_pct": 60
  }
}
```

### Statistiques CINEMA

**Endpoint :** `GET /api/v1/stats/cinema`

**Reponse 200 :**
```json
{
  "success": true,
  "stats": {
    "total_talents": 250,
    "by_gender": {
      "M": 120,
      "F": 130
    },
    "by_talent_type": [
      { "type": "Figurant(e)", "count": 150 },
      { "type": "Acteur Secondaire", "count": 60 },
      { "type": "Acteur Principal", "count": 40 }
    ],
    "by_country": [
      { "country": "Maroc", "count": 150 },
      { "country": "Senegal", "count": 40 }
    ],
    "by_experience": {
      "debutant": 80,
      "1_5_ans": 100,
      "5_10_ans": 50,
      "10_plus": 20
    },
    "with_photo_pct": 95,
    "avg_height": 172
  }
}
```

---

## Endpoints Exports

### Export Excel utilisateurs

**Endpoint :** `GET /api/v1/exports/users/excel`

**Reponse :** Fichier XLSX telecharge

### Export CSV utilisateurs

**Endpoint :** `GET /api/v1/exports/users/csv`

**Reponse :** Fichier CSV telecharge

### Export Excel CINEMA

**Endpoint :** `GET /api/v1/exports/cinema/excel`

**Reponse :** Fichier XLSX telecharge

---

## Endpoints Internes

Ces endpoints sont utilises par l'interface web.

### Pays

**Endpoint :** `GET /api/countries`

### Villes par pays

**Endpoint :** `GET /api/cities/{country_id}`

### Talents (formulaires)

**Endpoint :** `GET /api/talents`

### Recherche IA

**Endpoint :** `POST /ai-search`

**Body :**
```json
{
  "job_description": "Recherche developpeur Python...",
  "file": null
}
```

### Casting IA CINEMA

**Endpoint :** `POST /cinema/ai-search`

**Body :**
```json
{
  "role_description": "Recherche actrice 25-35 ans...",
  "gender": "F",
  "age_min": 25,
  "age_max": 35,
  "skin_tone": "Mat"
}
```

---

## Codes d'erreur

| Code HTTP | Code | Description |
|-----------|------|-------------|
| 400 | BAD_REQUEST | Requete invalide |
| 401 | UNAUTHORIZED | Non authentifie |
| 403 | FORBIDDEN | Acces refuse |
| 404 | NOT_FOUND | Ressource non trouvee |
| 422 | VALIDATION_ERROR | Erreur de validation |
| 500 | SERVER_ERROR | Erreur serveur |

---

## Exemples d'integration

### Python (requests)

```python
import requests

BASE_URL = "https://votre-domaine.com/api/v1"
session = requests.Session()

# Login
response = session.post(f"{BASE_URL}/auth/login", json={
    "email": "user@example.com",
    "password": "motdepasse"
})

# Liste utilisateurs
users = session.get(f"{BASE_URL}/users", params={
    "page": 1,
    "per_page": 50,
    "country_id": 1
})
print(users.json())

# Detail talent CINEMA
talent = session.get(f"{BASE_URL}/cinema/talents/code/MACAS000001F")
print(talent.json())

# Logout
session.post(f"{BASE_URL}/auth/logout")
```

### JavaScript (fetch)

```javascript
const BASE_URL = 'https://votre-domaine.com/api/v1';

// Login
async function login(email, password) {
    const response = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
        credentials: 'include'
    });
    return response.json();
}

// Liste utilisateurs
async function getUsers(page = 1) {
    const response = await fetch(
        `${BASE_URL}/users?page=${page}`,
        { credentials: 'include' }
    );
    return response.json();
}

// Utilisation
login('user@example.com', 'motdepasse')
    .then(() => getUsers())
    .then(data => console.log(data));
```

### cURL

```bash
# Login
curl -X POST "https://votre-domaine.com/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"motdepasse"}' \
  -c cookies.txt

# Liste utilisateurs
curl "https://votre-domaine.com/api/v1/users?page=1" \
  -b cookies.txt

# Detail talent CINEMA
curl "https://votre-domaine.com/api/v1/cinema/talents/code/MACAS000001F" \
  -b cookies.txt
```

---

*Documentation API par MOA Digital Agency LLC - www.myoneart.com*
