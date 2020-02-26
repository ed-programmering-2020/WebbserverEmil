from django.core.management.base import BaseCommand
from products.models import Laptop, BaseSpecification


class Command(BaseCommand):
    help = "Update the product rankings"

    def handle(self, *args, **kwargs):
        # Update all specification rankings
        BaseSpecification.rank()

        # Update category product rankings
        # - This should be done after specifications because of their dependency on them
        Laptop.rank()

        self.stdout.write(self.style.SUCCESS("Successfully updated product rankings"))
