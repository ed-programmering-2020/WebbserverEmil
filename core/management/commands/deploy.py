from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from dotenv import load_dotenv
from Orpose.settings.base import BASE_DIR
import os, django


class Command(BaseCommand):
    help = "does everything necessary for a production build"

    def handle(self, *args, **kwargs):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Orpose.settings.production')
        load_dotenv(os.path.join(BASE_DIR, ".env"))
        print(os.path.join(BASE_DIR, ".env"))
        call_command("migrate", interactive=False)
