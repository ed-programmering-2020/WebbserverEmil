from django.core.management.base import BaseCommand
from products.models.spec_groups import RefreshRate
from products.models.categories import Laptop


class Command(BaseCommand):
    help = "Creates singular model instanced"

    def create_model_instance(self, model):
        if model.objects.count() == 0:
            instance = model.objects.create()
            print("created", instance)

    def create_spec_groups(self):
        self.create_model_instance(RefreshRate)

    def create_categories(self):
        self.create_model_instance(Laptop)

    def handle(self, *args, **kwargs):
        self.create_spec_groups()
        self.create_categories()
        self.stdout.write(self.style.SUCCESS("Successfully deployed models"))
