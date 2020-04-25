from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **kwargs):
        User.objects.create_superuser("admin", "admin@admin.com", "admin")
        self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
