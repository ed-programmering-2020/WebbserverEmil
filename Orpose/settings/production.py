from .base import *
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(BASE_DIR, ".env"))

# React config
REACT_APP_DIR = "/home/Orpose/Orpose-Frontend/"
REACT_BUILD_DIR = os.path.join(REACT_APP_DIR, 'build')

# Static config
STATICFILES_DIRS = [
    os.path.join(REACT_BUILD_DIR, 'static'),
    REACT_BUILD_DIR
]

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

