from django.core.management.base import BaseCommand
from products.scraping.benchmark_collector import Collector


class Command(BaseCommand):
    help = "Update the benchmarks"

    def handle(self, *args, **kwargs):
        Collector()
        self.stdout.write(self.style.SUCCESS("Successfully updated product rankings"))
