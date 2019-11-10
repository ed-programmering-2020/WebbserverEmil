import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
from Orpose.settings.base import BASE_DIR

load_dotenv(os.path.join(BASE_DIR, '.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Orpose.settings')

application = get_wsgi_application()
