from django.core.management.base import BaseCommand
from products.models import BaseSpecification


class Command(BaseCommand):
    help = "Update the product rankings"

    def handle(self, *args, **kwargs):
        BaseSpecification.rank()

        self.stdout.write(self.style.SUCCESS("Successfully updated product rankings"))
