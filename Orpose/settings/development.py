from .base import *
import os

# Debug tools
DEBUG = True
TEMPLATE_DEBUG = True

# Database setup
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': "db",
    }
}
