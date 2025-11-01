# Changelog - Talento Platform

All notable changes to the Talento project are documented in this file.

**Version:** 2.0  
**Last Updated:** November 1, 2025

## [2.0.0] - 2025-11-01

### 🎉 Major Changes

#### Database Management
- **NEW:** Consolidated `database_manager.py` replacing 3 separate migration files
- **IMPROVED:** Safe GitHub update support (never deletes existing data)
- **ADDED:** Automatic backup before critical operations
- **ADDED:** Dry-run mode to preview changes
- **FIXED:** Idempotent migrations (can run multiple times safely)

#### Activity Logging
- **FIXED:** Display issue showing "page #None" in activity logs
- **ADDED:** Functional filter system with all real action types
- **ADDED:** User search filter (name, email, or code)
- **ADDED:** Date range filters (start and end dates)
- **IMPROVED:** Real-time filtering with form submission

#### Legal Pages
- **FIXED:** Terms of Service (CGU) activation not being saved correctly
- **FIXED:** Legal Mentions page returning 500 error
- **IMPROVED:** Consistent key naming between save and display logic
- **ADDED:** Activity logging for legal pages updates

#### Documentation
- **REORGANIZED:** All documentation moved to `docs/` folder
- **ADDED:** Bilingual documentation (French and English)
- **ADDED:** Comprehensive database management guide
- **ADDED:** Simplified root README with navigation
- **REMOVED:** Duplicate and outdated documentation files

### 📁 File Changes

#### Created
- `database_manager.py` - Consolidated database management tool
- `README.md` - Simplified navigation document
- `docs/README.en.md` - English main documentation
- `docs/README.fr.md` - French main documentation
- `docs/DEPLOYMENT.en.md` - English deployment guide
- `docs/CHANGELOG.en.md` - This file
- `docs/DATABASE_MANAGER.en.md` - English database guide
- `docs/DATABASE_MANAGER.fr.md` - French database guide

#### Modified
- `app/templates/admin/settings/activity_logs.html` - Fixed "page #None" display
- `app/services/logging_service.py` - Added filtering methods
- `app/routes/admin.py` - Updated activity logs route + fixed legal pages keys
- `docs/DEPLOYMENT.fr.md` - Renamed from root duplicate

#### Deleted
- `migrations_init.py` - Replaced by database_manager.py
- `init_essential_data.py` - Replaced by database_manager.py
- `init_full_database.py` - Replaced by database_manager.py
- `DEPLOYMENT.fr.md` (root) - Moved to docs/

### 🔧 Technical Improvements

#### Logging Service
```python
# New methods added
get_distinct_action_types()  # Get all unique action types
get_filtered_activities()     # Advanced filtering support
```

#### Legal Pages Fix
- Corrected key mapping: `terms_of_service` → `terms_page`
- Corrected key mapping: `mentions_legales` → `mentions_page`
- Added activity logging for legal page updates

#### Database Manager
- Supports `--force`, `--backup-first`, `--dry-run` options
- Compatible with PostgreSQL and SQLite
- Automatic rollback on errors
- Detailed operation logging

## [1.x.x] - Previous Versions

For previous version history, see the French changelog: [CHANGELOG.fr.md](./CHANGELOG.fr.md)

### Key Features from Previous Releases

#### Weekly Admin Recap (October 2025)
- Automated weekly email summaries every Sunday at 12:59 PM
- Separate sections for regular and cinema talents
- Direct links to view profiles
- Configurable fields per talent type

#### Enhanced AI Configuration (October 2025)
- Per-provider model selection (Perplexity, OpenAI, Gemini)
- Dynamic configuration through AppSettings
- Runtime model changes without code modifications

#### Name Tracking System (October 2025)
- Database models for monitoring specific names during registration
- Notification system when tracked individuals register
- Admin UI for managing tracked names

## 🔄 Upgrade Guide

### From 1.x to 2.0

#### 1. Backup Your Database

```bash
python database_manager.py --backup-first --dry-run
```

#### 2. Update Code

```bash
git pull origin main
```

#### 3. Run Migration

```bash
python database_manager.py --backup-first
```

#### 4. Verify Changes

- Test activity logs filtering
- Check legal pages activation
- Verify documentation links

### Breaking Changes

⚠️ **Migration Files Removed**
- `migrations_init.py` → Use `database_manager.py`
- `init_essential_data.py` → Use `database_manager.py`
- `init_full_database.py` → Use `database_manager.py`

⚠️ **Documentation Restructured**
- Root README is now just a navigation file
- All detailed docs moved to `docs/` folder
- Documentation now available in FR and EN

## 📝 Notes

### Compatibility
- Python 3.11+
- PostgreSQL 13+ or SQLite
- All existing data preserved during migration

### Security
- No breaking changes to authentication
- Encryption keys remain compatible
- Activity logging enhanced (non-breaking)

## 🙏 Credits

**MOA Digital Agency LLC**  
Developer: Aisance KALONJI  
Email: moa@myoneart.com  
Website: www.myoneart.com

---

*For detailed French changelog, see [CHANGELOG.fr.md](./CHANGELOG.fr.md)*
