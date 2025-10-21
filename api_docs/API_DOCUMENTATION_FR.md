# Documentation API Talento - Version 1.0

**Base URL**: `https://votre-domaine.com/api/v1`

**Format de réponse**: JSON

**Authentification**: Session-based (cookies)

---

## 📋 Table des matières

1. [Authentification](#authentification)
2. [Gestion des utilisateurs](#gestion-des-utilisateurs)
3. [Talents et localisation](#talents-et-localisation)
4. [Module CINEMA](#module-cinema)
5. [Statistiques](#statistiques)
6. [Exports de données](#exports-de-données)
7. [Codes d'erreur](#codes-derreur)

---

## 🔐 Authentification

### Connexion

**Endpoint**: `POST /api/v1/auth/login`

**Description**: Authentifie un utilisateur via email ou code unique.

**Requête**:
```json
{
  "identifier": "user@example.com",
  "password": "motdepasse123"
}
```

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
    "is_admin": false
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

---

### Déconnexion

**Endpoint**: `POST /api/v1/auth/logout`

**Authentification**: Requise

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

**Description**: Récupère les informations de l'utilisateur connecté.

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
    "gender": "M",
    "is_admin": false,
    "account_active": true,
    "created_at": "2025-10-15T10:30:00"
  }
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
- `availability` (string, optionnel): `disponible_maintenant`, `disponible_prochainement`, etc.
- `page` (integer, défaut: 1): Numéro de page
- `limit` (integer, défaut: 20, max: 100): Résultats par page

**Exemple de requête**:
```
GET /api/v1/users?search=ahmed&country_id=1&page=1&limit=20
```

**Réponse réussie** (200):
```json
{
  "success": true,
  "total": 156,
  "page": 1,
  "limit": 20,
  "users": [
    {
      "id": 42,
      "unique_code": "MARAB0042M",
      "first_name": "Ahmed",
      "last_name": "Benali",
      "email": "ahmed@example.com",
      "gender": "M",
      "availability": "disponible_maintenant",
      "country": "Maroc",
      "city": "Rabat",
      "account_active": true,
      "created_at": "2025-10-15T10:30:00",
      "talents": [
        {
          "id": 18,
          "name": "Développement Web",
          "emoji": "🖥️"
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
    "gender": "M",
    "date_of_birth": "1995-06-15",
    "bio": "Développeur web passionné...",
    "availability": "disponible_maintenant",
    "work_mode": "remote",
    "rate_range": "500-1000",
    "years_experience": 5,
    "country": {
      "id": 1,
      "name": "Maroc"
    },
    "city": {
      "id": 5,
      "name": "Rabat"
    },
    "portfolio_url": "https://portfolio.example.com",
    "linkedin": "https://linkedin.com/in/ahmed",
    "instagram": "@ahmed_dev",
    "twitter": "@ahmed",
    "facebook": "https://fb.com/ahmed",
    "github": "github.com/ahmed",
    "account_active": true,
    "photo_url": "/uploads/photos/abc123.jpg",
    "cv_url": "/uploads/cvs/cv_abc123.pdf",
    "qr_code_url": "/uploads/qrcodes/qr_abc123.png",
    "profile_score": 85,
    "created_at": "2025-10-15T10:30:00",
    "talents": [
      {
        "id": 18,
        "name": "Développement Web",
        "emoji": "🖥️"
      },
      {
        "id": 20,
        "name": "Développement Mobile",
        "emoji": "📱"
      }
    ]
  }
}
```

---

### Supprimer un utilisateur

**Endpoint**: `DELETE /api/v1/users/:user_id`

**Authentification**: Admin requis

**Exemple**:
```
DELETE /api/v1/users/42
```

**Réponse réussie** (200):
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

**Réponse d'erreur** (400):
```json
{
  "success": false,
  "error": "Cannot delete admin account"
}
```

---

### Activer/Désactiver un utilisateur

**Endpoint**: `POST /api/v1/users/:user_id/toggle-active`

**Authentification**: Admin requis

**Exemple**:
```
POST /api/v1/users/42/toggle-active
```

**Réponse réussie** (200):
```json
{
  "success": true,
  "active": true,
  "message": "Account activated"
}
```

---

## 🎯 Talents et localisation

### Liste des talents

**Endpoint**: `GET /api/v1/talents`

**Authentification**: Aucune

**Réponse réussie** (200):
```json
{
  "success": true,
  "total": 73,
  "talents": [
    {
      "id": 1,
      "name": "Maçonnerie",
      "emoji": "🧱",
      "category": "Construction",
      "is_active": true
    },
    {
      "id": 18,
      "name": "Développement Web",
      "emoji": "🖥️",
      "category": "Technologie",
      "is_active": true
    }
  ]
}
```

---

### Liste des pays

**Endpoint**: `GET /api/v1/countries`

**Authentification**: Aucune

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
      "flag": "🇲🇦"
    },
    {
      "id": 2,
      "name": "Algérie",
      "code": "DZ",
      "flag": "🇩🇿"
    }
  ]
}
```

---

### Liste des villes

**Endpoint**: `GET /api/v1/cities`

**Authentification**: Aucune

**Paramètres de requête**:
- `country_id` (integer, optionnel): Filtrer par pays

**Exemple**:
```
GET /api/v1/cities?country_id=1
```

**Réponse réussie** (200):
```json
{
  "success": true,
  "total": 79,
  "cities": [
    {
      "id": 1,
      "name": "Rabat",
      "code": "RAB",
      "country_id": 1
    },
    {
      "id": 2,
      "name": "Casablanca",
      "code": "CAS",
      "country_id": 1
    }
  ]
}
```

---

## 🎬 Module CINEMA

### Liste des talents CINEMA

**Endpoint**: `GET /api/v1/cinema/talents`

**Authentification**: Requise

**Paramètres de requête**:
- `search` (string, optionnel): Recherche par nom
- `gender` (string, optionnel): `M`, `F`, ou `N`
- `country_origin_id` (integer, optionnel): Filtrer par pays d'origine
- `page` (integer, défaut: 1): Numéro de page
- `limit` (integer, défaut: 20, max: 100): Résultats par page

**Exemple**:
```
GET /api/v1/cinema/talents?gender=F&page=1&limit=20
```

**Réponse réussie** (200):
```json
{
  "success": true,
  "total": 45,
  "page": 1,
  "limit": 20,
  "talents": [
    {
      "id": 12,
      "first_name": "Fatima",
      "last_name": "Zahra",
      "gender": "F",
      "date_of_birth": "1998-03-20",
      "country_origin": "Maroc",
      "country_residence": "Maroc",
      "photo_profile_url": "/uploads/cinema/profile_xyz.jpg",
      "is_active": true,
      "created_at": "2025-10-20T15:00:00",
      "email": "fatima@example.com",
      "ethnicities": ["Arabe", "Amazigh"],
      "languages_spoken": ["Français", "Arabe", "Anglais", "Amazigh"],
      "other_talents": ["Acteur", "Chant", "Danse"]
    }
  ]
}
```

---

### Détails d'un talent CINEMA

**Endpoint**: `GET /api/v1/cinema/talents/:talent_id`

**Authentification**: Requise

**Exemple**:
```
GET /api/v1/cinema/talents/12
```

**Réponse réussie** (200):
```json
{
  "success": true,
  "talent": {
    "id": 12,
    "first_name": "Fatima",
    "last_name": "Zahra",
    "gender": "F",
    "date_of_birth": "1998-03-20",
    "id_document_type": "CIN",
    "country_origin": {
      "id": 1,
      "name": "Maroc",
      "flag": "🇲🇦"
    },
    "nationality_country": {
      "id": 1,
      "name": "Maroc",
      "flag": "🇲🇦"
    },
    "country_residence": {
      "id": 1,
      "name": "Maroc",
      "flag": "🇲🇦"
    },
    "city_residence": "Casablanca",
    "eye_color": "Marron",
    "hair_color": "Noir",
    "hair_type": "Bouclés",
    "height": 165,
    "skin_tone": "Bronzé",
    "build": "Mince",
    "photo_profile_url": "/uploads/cinema/profile_xyz.jpg",
    "photo_id_url": "/uploads/cinema/id_xyz.jpg",
    "photo_gallery_1_url": "/uploads/cinema/gallery1_xyz.jpg",
    "is_active": true,
    "created_at": "2025-10-20T15:00:00",
    "email": "fatima@example.com",
    "phone": "+212600000000",
    "facebook": "https://fb.com/fatima",
    "instagram": "@fatima_actress",
    "tiktok": "@fatima_tiktok",
    "youtube": "https://youtube.com/c/fatima",
    "ethnicities": ["Arabe", "Amazigh"],
    "languages_spoken": ["Français", "Arabe", "Anglais", "Amazigh", "Espagnol"],
    "other_talents": ["Acteur", "Chant", "Danse", "Mannequinat"],
    "previous_productions": [
      {
        "title": "Film Example",
        "year": 2024,
        "type": "Film"
      }
    ]
  }
}
```

---

### Statistiques CINEMA

**Endpoint**: `GET /api/v1/cinema/stats`

**Authentification**: Requise

**Réponse réussie** (200):
```json
{
  "success": true,
  "stats": {
    "total_talents": 150,
    "active_talents": 145,
    "inactive_talents": 5,
    "by_gender": {
      "M": 80,
      "F": 60,
      "N": 5
    },
    "by_country": {
      "Maroc": 120,
      "Algérie": 15,
      "Tunisie": 10
    }
  }
}
```

---

## 📊 Statistiques

### Vue d'ensemble

**Endpoint**: `GET /api/v1/stats/overview`

**Authentification**: Admin requis

**Réponse réussie** (200):
```json
{
  "success": true,
  "stats": {
    "total_users": 450,
    "active_users": 432,
    "inactive_users": 18,
    "by_gender": {
      "M": 280,
      "F": 150,
      "N": 2
    },
    "by_availability": {
      "disponible_maintenant": 200,
      "disponible_prochainement": 150,
      "pas_disponible": 82
    },
    "by_country": {
      "Maroc": 380,
      "Algérie": 30,
      "Tunisie": 22
    },
    "top_talents": [
      {
        "name": "Développement Web",
        "emoji": "🖥️",
        "count": 85
      },
      {
        "name": "Graphisme",
        "emoji": "🖌️",
        "count": 62
      }
    ]
  }
}
```

---

### Statistiques par talents

**Endpoint**: `GET /api/v1/stats/talents`

**Authentification**: Admin requis

**Réponse réussie** (200):
```json
{
  "success": true,
  "stats": {
    "by_category": {
      "Technologie": 150,
      "Construction": 120,
      "Créatif": 80,
      "Restauration": 60
    },
    "total_talents": 73,
    "total_users_with_talents": 420
  }
}
```

---

## 📥 Exports de données

### Export Excel

**Endpoint**: `GET /api/v1/export/users/excel`

**Authentification**: Admin requis

**Description**: Télécharge tous les utilisateurs au format Excel (.xlsx)

**Réponse**: Fichier Excel téléchargeable

---

### Export CSV

**Endpoint**: `GET /api/v1/export/users/csv`

**Authentification**: Admin requis

**Description**: Télécharge tous les utilisateurs au format CSV

**Réponse**: Fichier CSV téléchargeable

---

### Export PDF

**Endpoint**: `POST /api/v1/export/users/pdf`

**Authentification**: Admin requis

**Description**: Télécharge les utilisateurs sélectionnés au format PDF

**Requête**:
```json
{
  "user_ids": [1, 5, 12, 24, 42]
}
```

**Réponse**: Fichier PDF téléchargeable

**Réponse d'erreur** (400):
```json
{
  "success": false,
  "error": "No user IDs provided"
}
```

---

## ⚠️ Codes d'erreur

| Code HTTP | Description |
|-----------|-------------|
| 200 | Succès |
| 400 | Requête invalide |
| 401 | Non authentifié |
| 403 | Accès refusé (permissions insuffisantes) |
| 404 | Ressource non trouvée |
| 500 | Erreur serveur |

---

## 📝 Notes importantes

1. **Authentification**: Utiliser les cookies de session après connexion
2. **Pagination**: Limite maximale de 100 résultats par requête
3. **Dates**: Format ISO 8601 (`YYYY-MM-DDTHH:MM:SS`)
4. **Champs cryptés**: Les données sensibles sont automatiquement décryptées côté serveur
5. **CSRF**: Les requêtes POST/PUT/DELETE nécessitent un token CSRF valide

---

## 🔄 Exemples d'utilisation

### Exemple avec cURL (Connexion + Récupération des utilisateurs)

```bash
# 1. Connexion
curl -X POST https://votre-domaine.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"identifier":"admin@talento.com","password":"@4dm1n"}' \
  -c cookies.txt

# 2. Récupération des utilisateurs
curl -X GET "https://votre-domaine.com/api/v1/users?page=1&limit=20" \
  -b cookies.txt
```

### Exemple avec JavaScript (Fetch API)

```javascript
// Connexion
const login = async () => {
  const response = await fetch('/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({
      identifier: 'user@example.com',
      password: 'password123'
    })
  });
  
  const data = await response.json();
  console.log(data);
};

// Récupération des utilisateurs
const getUsers = async () => {
  const response = await fetch('/api/v1/users?page=1&limit=20', {
    credentials: 'include'
  });
  
  const data = await response.json();
  console.log(data.users);
};
```

---

**Version**: 1.0  
**Dernière mise à jour**: 21 octobre 2025
