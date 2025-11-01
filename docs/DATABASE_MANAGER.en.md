# Database Manager Usage Guide

> `database_manager.py` - Unified and consolidated database manager for Talento

## 📋 Overview

The `database_manager.py` file replaces the old migration files (`migrations_init.py`, `init_essential_data.py`, `init_full_database.py`) and provides a single, safe, and powerful tool for managing the database.

## ✨ Features

- ✅ Automatic creation of missing tables
- ✅ Intelligent addition of missing columns (without data loss)
- ✅ Loading of essential data (countries, cities, talents, admin)
- ✅ Automatic backup before any critical modification
- ✅ Automatic rollback on error
- ✅ Detailed logging of all operations
- ✅ Dry-run mode to preview changes
- ✅ Compatible with PostgreSQL and SQLite
- ✅ **Safe for GitHub updates** (never deletes existing data)

## 🚀 Usage

### First Startup (Fresh Installation)

```bash
python database_manager.py --force
```

This command:
1. Creates all necessary tables
2. Loads essential data (countries, cities, talent categories)
3. Creates the default admin account
4. Configures application settings

### After a GitHub Pull (Secure Update)

```bash
python database_manager.py --backup-first
```

This command:
1. **Creates a complete database backup**
2. Detects and creates new tables if needed
3. Adds new columns without touching existing data
4. Loads new reference data
5. Preserves all your existing data

### Interactive Mode (with Confirmations)

```bash
python database_manager.py
```

The script will ask for confirmation before each important operation.

### Check Status Without Modifications

```bash
python database_manager.py --dry-run
```

Displays what would be modified without changing anything in the database.

## 📌 Available Options

| Option | Description |
|--------|-------------|
| `--force` | Non-interactive mode (no confirmation) |
| `--backup-first` | Create backup before any operation |
| `--dry-run` | Display modifications without applying them |
| `--verbose` / `-v` | Display detailed logs |
| `--help` / `-h` | Display help |

## 🔒 Security and Guarantees

### Data Protection

1. **Never automatic deletion** - The script NEVER deletes existing data
2. **Automatic backups** - Created before any risky operation
3. **Automatic rollback** - In case of error, all modifications are cancelled
4. **Idempotent** - Can be run multiple times safely

### Safe Use Cases

✅ **Update after git pull** → Perfectly safe  
✅ **Re-execution** → No problem  
✅ **Repair after error** → Automatically restores  

## 📖 Practical Examples

### Scenario 1: New Developer

```bash
# Clone the project
git clone https://github.com/your-repo/talento.git
cd talento

# Install dependencies
pip install -r requirements.txt

# Initialize database
python database_manager.py --force

# Start the application
python app.py
```

### Scenario 2: Code Update

```bash
# Pull latest modifications
git pull origin main

# Safely update the database
python database_manager.py --backup-first

# Restart the application
python app.py
```

### Scenario 3: Pre-Deployment Verification

```bash
# Check what will be modified
python database_manager.py --dry-run

# If everything is OK, apply changes
python database_manager.py --backup-first --force
```

## 🛠️ Troubleshooting

### Error: "Table already exists"

This is normal and automatically handled. The script detects existing tables and doesn't recreate them.

### Error: "Column already exists"

Also normal. The script checks for column existence before adding them.

### Backup Not Found

Backups are created in the `backups/` folder at the project root.

### Corrupted Database

```bash
# Restore from a backup
# 1. Locate the backup file in backups/
# 2. Restore it manually or contact technical support
```

## 📊 Logs and Reports

The script generates detailed logs of all operations:

```
[2025-11-01 09:00:00] [INFO] 🔍 Checking database structure...
[2025-11-01 09:00:01] [INFO] ✅ All required tables already exist
[2025-11-01 09:00:02] [INFO] 📊 Checking columns...
[2025-11-01 09:00:03] [INFO] ✅ All required columns exist
```

## 🔄 Migration from Old Files

If you're still using the old files (`migrations_init.py`, `init_essential_data.py`, `init_full_database.py`), switch to `database_manager.py`:

```bash
# No action required!
# database_manager.py does everything the old files did
python database_manager.py --backup-first
```

Old files can be safely deleted.

## 💡 Tips and Best Practices

1. **Always use `--backup-first` in production**
2. **Use `--dry-run` to preview changes**
3. **Keep backups for at least 30 days**
4. **Test on a development environment first**
5. **Read logs after each execution**

## 📞 Support

For any questions or issues:
- Check the [technical documentation](./TECHNICAL_DOCUMENTATION.en.md)
- Review the [changelog](./CHANGELOG.en.md) for recent changes
- Contact: moa@myoneart.com

---

**Last Updated:** November 1, 2025  
**Version:** 2.0 (Consolidated Manager)

*For French version, see [DATABASE_MANAGER.fr.md](./DATABASE_MANAGER.fr.md)*
