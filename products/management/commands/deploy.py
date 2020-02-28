from django.core.management.base import BaseCommand
from products.models import Laptop


class Command(BaseCommand):
    help = "Do everything necessary for deployment"

    def handle(self, *args, **kwargs):
        Laptop.create_dummy()

        self.stdout.write(self.style.SUCCESS("Deployment was successful"))
