# TalentsMaroc.com - Platform for Talent Centralization

TalentsMaroc.com is a professional web application designed to centralize and showcase talent profiles across Africa. The platform enables individuals to create detailed professional profiles, highlight their skills, and connect with opportunities.

## Features

- **User Registration**: Create comprehensive professional profiles with personal information, skills, and experience
- **Unique ID System**: Each user receives a unique 10-character code for easy identification
- **Multi-Talent Support**: Users can showcase multiple skills and talents across various categories
- **QR Code Generation**: Automatic QR code generation for each profile
- **Admin Dashboard**: Powerful administrative tools for managing users and viewing statistics
- **Search & Filter**: Advanced search capabilities by name, skills, location, and more
- **Data Export**: Export user data in Excel, PDF, and CSV formats
- **Encrypted Data**: Sensitive information is encrypted for security
- **African Coverage**: Support for all 54 African countries

## Technical Stack

- **Backend**: Flask (Python 3.11)
- **Database**: PostgreSQL
- **Frontend**: HTML5, Tailwind CSS
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy
- **Email**: Flask-Mail

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL database

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
ENCRYPTION_KEY=your-encryption-key-here
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key
```

3. Initialize the database:
```bash
python migrations_init.py
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Default Admin Credentials

- **Email**: admin@talentsmaroc.com
- **Password**: @4dm1n

⚠️ **Important**: Change the admin password after first login!

### Demo Accounts

The system includes 5 demo user accounts for testing:
- demo1@talentsmaroc.com to demo5@talentsmaroc.com
- Password: demo123

## Project Structure

```
talentsmaroc/
├── app/
│   ├── models/          # Database models
│   ├── routes/          # Application routes
│   ├── services/        # Business logic services
│   ├── templates/       # HTML templates
│   ├── static/          # CSS, uploads
│   └── utils/           # Utility functions
├── migrations_init.py   # Database initialization
├── app.py              # Application entry point
├── config.py           # Configuration
└── requirements.txt    # Python dependencies
```

## Key Features Explained

### Unique ID System
Each user receives a unique 10-character code in the format:
`CC-CCC-NNNN-G`
- CC: Country code
- CCC: City code
- NNNN: Sequential number
- G: Gender (M/F/N)

### Security
- Passwords are hashed using bcrypt
- Sensitive data (phone numbers) is encrypted
- Email validation and verification
- Admin-only access controls

### Data Export
Administrators can export user data in multiple formats:
- **Excel**: Comprehensive spreadsheet with all user details
- **PDF**: Formatted document with user information
- **CSV**: Simple comma-separated format

## License

© 2024 TalentsMaroc.com. All rights reserved.

## Support

For issues or questions, please contact the development team.
