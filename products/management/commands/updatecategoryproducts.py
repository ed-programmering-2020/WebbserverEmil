from django.core.management.base import BaseCommand
from products.models import BaseCategoryProduct


class Command(BaseCommand):
    help = "Update all category products"

    def handle(self, *args, **kwargs):
        for category_product in BaseCategoryProduct.objects.all().iterator():
            category_product.update()

        self.stdout.write(self.style.SUCCESS("Successfully updated category products"))
