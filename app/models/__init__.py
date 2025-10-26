"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from app.models.user import User
from app.models.talent import Talent, UserTalent
from app.models.location import Country, City
from app.models.settings import AppSettings
from app.models.cinema_talent import CinemaTalent
from app.models.production import Production
from app.models.project import Project, ProjectTalent
from app.models.attendance import Attendance

__all__ = ['User', 'Talent', 'UserTalent', 'Country', 'City', 'AppSettings', 'CinemaTalent', 'Production', 'Project', 'ProjectTalent', 'Attendance']
