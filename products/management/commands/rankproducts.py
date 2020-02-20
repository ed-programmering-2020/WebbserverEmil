from django.core.management.base import BaseCommand
from products.matching.ranking import rank_products


class Command(BaseCommand):
    help = "Update the product rankings"

    def handle(self, *args, **kwargs):
        rank_products()
        self.stdout.write(self.style.SUCCESS("Successfully updated product rankings"))
