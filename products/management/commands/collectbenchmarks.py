from django.core.management.base import BaseCommand
from products.models import Processor, GraphicsCard


class Command(BaseCommand):
    help = "Collect the benchmarks"

    def handle(self, *args, **kwargs):
        Processor.collect_benchmarks()
        GraphicsCard.collect_benchmarks()

        self.stdout.write(self.style.SUCCESS("Successfully collected benchmarks"))
