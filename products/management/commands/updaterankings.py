from django.core.management.base import BaseCommand
from products.models import SpecifiedSpecification, BenchmarkSpecification, StandardSpecification


class Command(BaseCommand):
    help = "Update the product rankings"

    def handle(self, *args, **kwargs):
        StandardSpecification.rank()
        BenchmarkSpecification.rank()
        SpecifiedSpecification.rank()

        self.stdout.write(self.style.SUCCESS("Successfully updated product rankings"))
