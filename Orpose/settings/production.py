from .base import *
import os

# Allowed hosts
ALLOWED_HOSTS = [
    "www.orposegroup.com",
    "elasticbeanstalk-eu-north-1-064640888666.s3.eu-north-1.amazonaws.com"
]

# Database setup
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
