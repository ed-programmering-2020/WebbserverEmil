from .base import *
import os

# Allowed hosts
ALLOWED_HOSTS = [
    "www.orposegroup.com",
    "http://corebackend-env.eba-qkwpqud8.eu-north-1.elasticbeanstalk.com/"
]

# Database setup
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'OrposeDB',
        'PASSWORD':  os.environ['DB_PASSWORD'],
        'HOST': 'https://eu-north-1.console.aws.amazon.com/rds/home?region=eu-north-1#dbinstances:id=aar41h3vgnc3uz',
        'OPTIONS': {'init_command": "SET foreign_key_checks = 0;'}
    }
}
