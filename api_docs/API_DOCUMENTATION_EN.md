# Talento API Documentation - Version 1.0

**Base URL**: `https://your-domain.com/api/v1`

**Response Format**: JSON

**Authentication**: Session-based (cookies)

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Talents & Location](#talents--location)
4. [CINEMA Module](#cinema-module)
5. [Statistics](#statistics)
6. [Data Exports](#data-exports)
7. [Error Codes](#error-codes)

---

## 🔐 Authentication

### Login

**Endpoint**: `POST /api/v1/auth/login`

**Description**: Authenticates a user via email or unique code.

**Request**:
```json
{
  "identifier": "user@example.com",
  "password": "password123"
}
```

**Success Response** (200):
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

**Error Response** (401):
```json
{
  "success": false,
  "error": "Invalid credentials"
}
```

---

### Logout

**Endpoint**: `POST /api/v1/auth/logout`

**Authentication**: Required

**Success Response** (200):
```json
{
  "success": true,
  "message": "Logout successful"
}
```

---

### Current User

**Endpoint**: `GET /api/v1/auth/me`

**Authentication**: Required

**Description**: Retrieves the current authenticated user's information.

**Success Response** (200):
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

## 👥 User Management

### List Users

**Endpoint**: `GET /api/v1/users`

**Authentication**: Admin required

**Query Parameters**:
- `search` (string, optional): Search by name, email, or code
- `country_id` (integer, optional): Filter by country
- `city_id` (integer, optional): Filter by city
- `gender` (string, optional): `M`, `F`, or `N`
- `availability` (string, optional): `disponible_maintenant`, `disponible_prochainement`, etc.
- `page` (integer, default: 1): Page number
- `limit` (integer, default: 20, max: 100): Results per page

**Example Request**:
```
GET /api/v1/users?search=ahmed&country_id=1&page=1&limit=20
```

**Success Response** (200):
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

### Get User Details

**Endpoint**: `GET /api/v1/users/:user_id`

**Authentication**: Required (admin or owner)

**Example**:
```
GET /api/v1/users/42
```

**Success Response** (200):
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
    "bio": "Passionate web developer...",
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

### Delete User

**Endpoint**: `DELETE /api/v1/users/:user_id`

**Authentication**: Admin required

**Example**:
```
DELETE /api/v1/users/42
```

**Success Response** (200):
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

**Error Response** (400):
```json
{
  "success": false,
  "error": "Cannot delete admin account"
}
```

---

### Toggle User Active Status

**Endpoint**: `POST /api/v1/users/:user_id/toggle-active`

**Authentication**: Admin required

**Example**:
```
POST /api/v1/users/42/toggle-active
```

**Success Response** (200):
```json
{
  "success": true,
  "active": true,
  "message": "Account activated"
}
```

---

## 🎯 Talents & Location

### List Talents

**Endpoint**: `GET /api/v1/talents`

**Authentication**: None

**Success Response** (200):
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

### List Countries

**Endpoint**: `GET /api/v1/countries`

**Authentication**: None

**Success Response** (200):
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

### List Cities

**Endpoint**: `GET /api/v1/cities`

**Authentication**: None

**Query Parameters**:
- `country_id` (integer, optional): Filter by country

**Example**:
```
GET /api/v1/cities?country_id=1
```

**Success Response** (200):
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

## 🎬 CINEMA Module

### List CINEMA Talents

**Endpoint**: `GET /api/v1/cinema/talents`

**Authentication**: Required

**Query Parameters**:
- `search` (string, optional): Search by name
- `gender` (string, optional): `M`, `F`, or `N`
- `country_origin_id` (integer, optional): Filter by country of origin
- `page` (integer, default: 1): Page number
- `limit` (integer, default: 20, max: 100): Results per page

**Example**:
```
GET /api/v1/cinema/talents?gender=F&page=1&limit=20
```

**Success Response** (200):
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

### Get CINEMA Talent Details

**Endpoint**: `GET /api/v1/cinema/talents/:talent_id`

**Authentication**: Required

**Example**:
```
GET /api/v1/cinema/talents/12
```

**Success Response** (200):
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

### CINEMA Statistics

**Endpoint**: `GET /api/v1/cinema/stats`

**Authentication**: Required

**Success Response** (200):
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

## 📊 Statistics

### Overview Statistics

**Endpoint**: `GET /api/v1/stats/overview`

**Authentication**: Admin required

**Success Response** (200):
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

### Talent Statistics

**Endpoint**: `GET /api/v1/stats/talents`

**Authentication**: Admin required

**Success Response** (200):
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

## 📥 Data Exports

### Export to Excel

**Endpoint**: `GET /api/v1/export/users/excel`

**Authentication**: Admin required

**Description**: Downloads all users in Excel format (.xlsx)

**Response**: Downloadable Excel file

---

### Export to CSV

**Endpoint**: `GET /api/v1/export/users/csv`

**Authentication**: Admin required

**Description**: Downloads all users in CSV format

**Response**: Downloadable CSV file

---

### Export to PDF

**Endpoint**: `POST /api/v1/export/users/pdf`

**Authentication**: Admin required

**Description**: Downloads selected users in PDF format

**Request**:
```json
{
  "user_ids": [1, 5, 12, 24, 42]
}
```

**Response**: Downloadable PDF file

**Error Response** (400):
```json
{
  "success": false,
  "error": "No user IDs provided"
}
```

---

## ⚠️ Error Codes

| HTTP Code | Description |
|-----------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden (insufficient permissions) |
| 404 | Resource not found |
| 500 | Internal Server Error |

---

## 📝 Important Notes

1. **Authentication**: Use session cookies after login
2. **Pagination**: Maximum limit of 100 results per request
3. **Dates**: ISO 8601 format (`YYYY-MM-DDTHH:MM:SS`)
4. **Encrypted Fields**: Sensitive data is automatically decrypted server-side
5. **CSRF**: POST/PUT/DELETE requests require a valid CSRF token

---

## 🔄 Usage Examples

### Example with cURL (Login + Get Users)

```bash
# 1. Login
curl -X POST https://your-domain.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"identifier":"admin@talento.com","password":"@4dm1n"}' \
  -c cookies.txt

# 2. Get users
curl -X GET "https://your-domain.com/api/v1/users?page=1&limit=20" \
  -b cookies.txt
```

### Example with JavaScript (Fetch API)

```javascript
// Login
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

// Get users
const getUsers = async () => {
  const response = await fetch('/api/v1/users?page=1&limit=20', {
    credentials: 'include'
  });
  
  const data = await response.json();
  console.log(data.users);
};
```

### Example with Python (requests)

```python
import requests

# Create session to maintain cookies
session = requests.Session()

# Login
login_response = session.post(
    'https://your-domain.com/api/v1/auth/login',
    json={
        'identifier': 'admin@talento.com',
        'password': '@4dm1n'
    }
)

print(login_response.json())

# Get users
users_response = session.get(
    'https://your-domain.com/api/v1/users',
    params={'page': 1, 'limit': 20}
)

print(users_response.json())
```

---

**Version**: 1.0  
**Last Updated**: October 21, 2025
