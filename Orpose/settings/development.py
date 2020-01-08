from .base import *
import os

# Debug tools
DEBUG = True
TEMPLATE_DEBUG = True

# Database setup
DATABASE_ENGINE = "sqlite3"
DATABASE_NAME = os.path.join(BASE_DIR, "db")
