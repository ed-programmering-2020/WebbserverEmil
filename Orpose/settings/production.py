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
        'NAME': "DtaskDevDb",
        "USER": os.environ.get("RDS_DB_USERNAME"),
        "PASSWORD": os.environ.get("RDS_DB_PASSWORD"),
        "HOST": "dtask-dev-db.cmrx3tyslvo1.eu-north-1.rds.amazonaws.com",
        "PORT": "3306",
        'OPTIONS': {"init_command": "SET foreign_key_checks = 0;"}
    }
}