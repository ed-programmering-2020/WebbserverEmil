import os

# Static files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Debug tools
DEBUG = True
TEMPLATE_DEBUG = True

# Database setup
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, "db"),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
