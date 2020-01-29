from django.core.management.base import BaseCommand
from products.ranking.ranker import Ranker


class Command(BaseCommand):
    help = "Updates the product rankings"

    def handle(self, *args, **kwargs):
        Ranker()
        self.stdout.write(self.style.SUCCESS("Successfully updated product rankings"))
