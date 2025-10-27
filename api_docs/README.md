# TalentsMaroc.com API Documentation

Bienvenue dans la documentation API de TalentsMaroc.com ! / Welcome to TalentsMaroc.com API documentation!

## 📚 Documentation disponible / Available Documentation

### Français
- **[Documentation complète (FR)](./API_DOCUMENTATION_FR.md)** - Documentation détaillée en français avec tous les endpoints, exemples de requêtes et réponses

### English
- **[Full Documentation (EN)](./API_DOCUMENTATION_EN.md)** - Complete documentation in English with all endpoints, request/response examples

### Postman Collection
- **[Postman Collection](./TalentsMaroc.com_API_Postman_Collection.json)** - Import this file into Postman to test all API endpoints easily

## 🚀 Quick Start

### Base URL
```
Production: https://your-domain.com/api/v1
Development: http://localhost:5004/api/v1
```

### Authentication
```bash
curl -X POST http://localhost:5004/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"identifier":"admin@talento.com","password":"@4dm1n"}' \
  -c cookies.txt
```

### Test Endpoint
```bash
curl -X GET http://localhost:5004/api/v1/auth/me \
  -b cookies.txt
```

## 📋 Available Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/logout` - Logout
- `GET /api/v1/auth/me` - Current user

### Users
- `GET /api/v1/users` - List users (Admin)
- `GET /api/v1/users/:id` - Get user details
- `DELETE /api/v1/users/:id` - Delete user (Admin)
- `POST /api/v1/users/:id/toggle-active` - Toggle active status (Admin)

### Talents & Location
- `GET /api/v1/talents` - List talents
- `GET /api/v1/countries` - List countries
- `GET /api/v1/cities` - List cities

### CINEMA Module
- `GET /api/v1/cinema/talents` - List CINEMA talents
- `GET /api/v1/cinema/talents/:id` - Get CINEMA talent details
- `GET /api/v1/cinema/stats` - CINEMA statistics

### Statistics
- `GET /api/v1/stats/overview` - Platform overview (Admin)
- `GET /api/v1/stats/talents` - Talent statistics (Admin)

### Data Exports
- `GET /api/v1/export/users/excel` - Export to Excel (Admin)
- `GET /api/v1/export/users/csv` - Export to CSV (Admin)
- `POST /api/v1/export/users/pdf` - Export to PDF (Admin)

## 🔧 Using the Postman Collection

1. Open Postman
2. Click "Import"
3. Select `TalentsMaroc.com_API_Postman_Collection.json`
4. Update the `base_url` variable if needed
5. Start with "Login" request to authenticate
6. Test other endpoints

## 📖 Response Format

All API responses follow this format:

### Success Response
```json
{
  "success": true,
  "data": {...}
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message here"
}
```

## 🔐 Authentication

The API uses session-based authentication with cookies. After successful login:
- Cookie is automatically set
- Include credentials in subsequent requests
- Use `credentials: 'include'` in JavaScript Fetch API

## ⚠️ Important Notes

- **Pagination**: Maximum 100 results per request
- **Dates**: ISO 8601 format (`YYYY-MM-DDTHH:MM:SS`)
- **CSRF Protection**: Required for POST/PUT/DELETE operations
- **Admin Endpoints**: Require admin privileges

## 📞 Support

For questions or issues with the API, please contact the TalentsMaroc.com development team.

---

**Version**: 1.0.0  
**Last Updated**: October 21, 2025
