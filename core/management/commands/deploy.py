from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from Orpose.settings.base import BASE_DIR
import os, django


class Command(BaseCommand):
    help = "does everything necessary for a production build"

    def handle(self, *args, **kwargs):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Orpose.settings.production')
        call_command("migrate", interactive=False)
