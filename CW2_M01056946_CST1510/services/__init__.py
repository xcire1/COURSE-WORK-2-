from pathlib import Path

Path("app/__init__.py").touch()
Path("app/data/__init__.py").touch()
Path("app/services/__init__.py").touch()

from app.data.db import connect_database
from app.data.incidents import insert_incident, get_all_incidents
from app.services.user_service import register_user, login_user


