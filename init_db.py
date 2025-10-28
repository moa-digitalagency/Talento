#!/usr/bin/env python
"""
Initialize database tables for TalentsMaroc.com
"""
import os
import sys

os.environ['SKIP_AUTO_MIGRATION'] = '1'

from app import create_app, db
from app.models.user import User
from app.models.talent import Talent, UserTalent
from app.models.location import Country, City
from app.models.cinema_talent import CinemaTalent
from app.models.production import Production
from app.models.project import Project, ProjectTalent
from app.models.settings import AppSettings
from app.models.activity_log import ActivityLog
from app.models.security_log import SecurityLog
from app.models.attendance import Attendance

print("🔧 Creating Flask app...")
app = create_app()

with app.app_context():
    print("🗄️  Creating all database tables...")
    try:
        db.create_all()
        print("✅ All database tables created successfully!")
        
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📊 Total tables created: {len(tables)}")
        for table in sorted(tables):
            print(f"   ✓ {table}")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)
