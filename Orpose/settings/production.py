from .base import *
import os


ALLOWED_HOSTS = [
    "www.orpose.pythonanywhere.com",
    "www.orpose.se",
    "www.orpose.com",
    "www.orpose.co.uk"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("DB_USERNAME") + "$default",
        "USER": os.getenv("DB_USERNAME"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": "Orpose.mysql.pythonanywhere-services.com",
        'OPTIONS': {"init_command": "SET foreign_key_checks = 0;"}
    }
}