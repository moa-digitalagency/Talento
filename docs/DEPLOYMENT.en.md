# Talento - Deployment Guide

> Complete guide for deploying Talento platform

**Version:** 2.0  
**Last Updated:** November 1, 2025

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Development Environment](#development-environment)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Security Checklist](#security-checklist)
7. [Maintenance](#maintenance)

## 🔧 Prerequisites

### System Requirements
- **OS:** Linux (Ubuntu 20.04+ recommended) or macOS
- **Python:** 3.11+
- **Database:** PostgreSQL 13+ (production) or SQLite (development)
- **Memory:** 2GB+ RAM
- **Storage:** 10GB+ available space

### Required Services
- PostgreSQL database
- SendGrid account (for emails)
- AI API keys (optional but recommended):
  - OpenRouter API
  - Perplexity AI
  - OpenAI
  - Google Gemini

## 💻 Development Environment

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/your-repo/talento.git
cd talento

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```bash
# Application
SECRET_KEY=dev_secret_key_change_in_production
ENCRYPTION_KEY=dev_encryption_key_change_in_production
PORT=5000
DEBUG=True
SKIP_AUTO_MIGRATION=1

# Database (SQLite for dev)
DATABASE_URL=sqlite:///talento_dev.db

# Email (optional in dev)
SENDGRID_API_KEY=your_sendgrid_key

# AI Services (optional)
OPENROUTER_API_KEY=your_key
PERPLEXITY_API_KEY=your_key
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
```

### 3. Initialize Database

```bash
python database_manager.py --force
```

### 4. Run Development Server

```bash
python app.py
```

Access the application at `http://localhost:5000`

## 🚀 Production Deployment

### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Install Nginx (optional, for reverse proxy)
sudo apt install nginx
```

### 2. Application Setup

```bash
# Create application user
sudo useradd -m -s /bin/bash talento
sudo su - talento

# Clone repository
git clone https://github.com/your-repo/talento.git
cd talento

# Setup virtual environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn
```

### 3. Production Environment Variables

Create `/home/talento/talento/.env`:

```bash
# CRITICAL: Use strong, unique values in production!
SECRET_KEY=<generate_strong_random_key>
ENCRYPTION_KEY=<generate_strong_random_key>
PORT=5000
DEBUG=False
SKIP_AUTO_MIGRATION=1

# PostgreSQL Database
DATABASE_URL=postgresql://talento_user:secure_password@localhost/talento_db

# Email Service
SENDGRID_API_KEY=<your_sendgrid_api_key>

# AI Services
OPENROUTER_API_KEY=<your_key>
PERPLEXITY_API_KEY=<your_key>
OPENAI_API_KEY=<your_key>
GEMINI_API_KEY=<your_key>

# Admin Configuration
ADMIN_PASSWORD=<secure_admin_password>
```

### 4. Database Configuration

```bash
# Create PostgreSQL database and user
sudo -u postgres psql

CREATE DATABASE talento_db;
CREATE USER talento_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE talento_db TO talento_user;
\q

# Initialize database
cd /home/talento/talento
source venv/bin/activate
python database_manager.py --backup-first --force
```

### 5. Production Server (Gunicorn)

Create systemd service `/etc/systemd/system/talento.service`:

```ini
[Unit]
Description=Talento Web Application
After=network.target postgresql.service

[Service]
User=talento
Group=talento
WorkingDirectory=/home/talento/talento
Environment="PATH=/home/talento/talento/venv/bin"
EnvironmentFile=/home/talento/talento/.env
ExecStart=/home/talento/talento/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 --reuse-port app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable talento
sudo systemctl start talento
sudo systemctl status talento
```

### 6. Nginx Configuration (Optional)

Create `/etc/nginx/sites-available/talento`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /home/talento/talento/app/static;
    }
}
```

Enable and restart:

```bash
sudo ln -s /etc/nginx/sites-available/talento /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔐 Environment Configuration

### Generating Secure Keys

```python
# SECRET_KEY
import secrets
print(secrets.token_hex(32))

# ENCRYPTION_KEY
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### Required Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Flask secret key (64+ chars) |
| `ENCRYPTION_KEY` | Yes | Fernet encryption key |
| `DATABASE_URL` | Yes | Database connection string |
| `PORT` | No | Server port (default: 5000) |
| `DEBUG` | No | Debug mode (False in production) |
| `SENDGRID_API_KEY` | Yes | Email service key |
| `ADMIN_PASSWORD` | Yes | Admin account password |

## 🗄️ Database Setup

### PostgreSQL (Production)

```bash
# Backup
python database_manager.py --backup-first

# Update after git pull
python database_manager.py --backup-first

# Check status without changes
python database_manager.py --dry-run
```

### SQLite (Development)

SQLite is automatically configured for development. No additional setup needed.

## ✅ Security Checklist

- [ ] Strong `SECRET_KEY` and `ENCRYPTION_KEY` generated
- [ ] `DEBUG=False` in production
- [ ] Admin password changed from default
- [ ] Database credentials are secure
- [ ] Firewall configured (only ports 80, 443, 22 open)
- [ ] Regular backups scheduled
- [ ] HTTPS/SSL certificate installed
- [ ] Environment variables secured (not in version control)
- [ ] SendGrid API key secured
- [ ] AI API keys secured

## 🔄 Maintenance

### Regular Backups

```bash
# Manual backup
python database_manager.py --backup-first --dry-run

# Scheduled backups (cron)
0 2 * * * cd /home/talento/talento && /home/talento/talento/venv/bin/python database_manager.py --backup-first --force
```

### Updates and Migrations

```bash
# Pull latest code
git pull origin main

# Update database safely
python database_manager.py --backup-first

# Restart application
sudo systemctl restart talento
```

### Logs Monitoring

```bash
# Application logs
sudo journalctl -u talento -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Database logs
sudo tail -f /var/log/postgresql/postgresql-*-main.log
```

### Performance Optimization

1. **Database Indexing** - Ensure proper indexes on frequently queried columns
2. **Static File Serving** - Use Nginx for static files
3. **Gunicorn Workers** - Adjust based on CPU cores (2-4 workers per core)
4. **Database Connection Pooling** - Configure in SQLAlchemy
5. **Caching** - Implement Redis for session storage

## 🆘 Troubleshooting

### Application Won't Start

```bash
# Check logs
sudo journalctl -u talento -n 50

# Test application manually
cd /home/talento/talento
source venv/bin/activate
python app.py
```

### Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U talento_user -d talento_db
```

### Permission Issues

```bash
# Fix ownership
sudo chown -R talento:talento /home/talento/talento

# Fix permissions
chmod 755 /home/talento/talento
chmod 600 /home/talento/talento/.env
```

## 📞 Support

For deployment assistance:
- **Documentation:** [TECHNICAL_DOCUMENTATION.en.md](./TECHNICAL_DOCUMENTATION.en.md)
- **Email:** moa@myoneart.com
- **GitHub Issues:** https://github.com/your-repo/talento/issues

---

*Pour la version française, voir [DEPLOYMENT.fr.md](./DEPLOYMENT.fr.md)*
