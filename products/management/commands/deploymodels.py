from django.core.management.base import BaseCommand
from products.models.spec_groups import RefreshRate
from products.models.categories import Laptop


class Command(BaseCommand):
    help = "Creates singular model instanced"

    def create_model_instance(self, model):
        if model.objects.count() == 0:
            instance = model.objects.create()
            print("created", instance)

    def handle(self, *args, **kwargs):
        models = [
            RefreshRate,
            Laptop
        ]

        for model in models:
            self.create_model_instance(model)

        self.stdout.write(self.style.SUCCESS("Successfully deployed models"))
