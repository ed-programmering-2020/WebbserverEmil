from .base import *
import os
from dotenv import load_dotenv

# Static files
BASE_DIR = "/home/Orpose/Orpose-Backend"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_ROOT,
    REACT_BUILD_DIR,
    os.path.join(REACT_BUILD_DIR, "static")
]

# Environment variables
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Allowed hosts
ALLOWED_HOSTS = [
    "www.orpose.pythonanywhere.com",
    "www.orpose.se",
    "www.orpose.com",
    "www.orpose.co.uk"
]

# Database setup
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "Orpose$default",
        "USER": "Orpose",
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": "Orpose.mysql.pythonanywhere-services.com",
        'OPTIONS': {"init_command": "SET foreign_key_checks = 0;"}
    }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000

