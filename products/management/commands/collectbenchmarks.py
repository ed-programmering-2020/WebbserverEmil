from django.core.management.base import BaseCommand
from products.scraping import Collector


class Command(BaseCommand):
    help = "Collect the benchmarks"

    def handle(self, *args, **kwargs):
        Collector()
        self.stdout.write(self.style.SUCCESS("Successfully collected benchmarks"))
