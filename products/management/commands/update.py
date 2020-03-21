from django.core.management.base import BaseCommand
from products.models import Laptop


class Command(BaseCommand):
    help = "Update all category products"

    def handle(self, *args, **kwargs):
        for laptop in Laptop.objects.filter(is_active=True).iterator():
            laptop.update()

        self.stdout.write(self.style.SUCCESS("Successfully updated category products"))
