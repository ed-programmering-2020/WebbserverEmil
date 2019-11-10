from .base import *
import os


REACT_APP_DIR = "/home/Orpose/Orpose-Frontend/"

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
STATICFILES_DIRS = [
    os.path.join(REACT_APP_DIR, 'build', 'static')
]


ALLOWED_HOSTS = [
    "www.orpose.pythonanywhere.com",
    "www.orpose.se",
    "www.orpose.com",
    "www.orpose.co.uk"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "Orpose.Default",
        "USER": os.environ.get("DB_USERNAME"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": "Orpose.mysql.pythonanywhere-services.com",
        'OPTIONS': {"init_command": "SET foreign_key_checks = 0;"}
    }
}