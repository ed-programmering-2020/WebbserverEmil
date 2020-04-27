from .base import *
import os

# Allowed hosts
ALLOWED_HOSTS = [
    "orposegroup.com",
    "corebackend-env.eba-h3im4jjp.eu-north-1.elasticbeanstalk.com"
]

# Database setup
if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
