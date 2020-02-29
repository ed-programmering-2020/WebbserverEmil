from django.core.management.base import BaseCommand
from products.models import Weight, ScreenSize, GraphicsCard, Processor, PanelType, StorageSize, StorageType, Resolution, RefreshRate, Ram, BatteryTime
from products.models import Laptop


class Command(BaseCommand):
    help = "Do everything necessary for deployment"

    def handle(self, *args, **kwargs):
        # Create category product dummy's
        Laptop.create_dummy()

        # Create specification dummy's
        Weight.create_dummy()
        ScreenSize.create_dummy()
        GraphicsCard.create_dummy()
        Processor.create_dummy()
        PanelType.create_dummy()
        StorageType.create_dummy()
        StorageSize.create_dummy()
        RefreshRate.create_dummy()
        Resolution.create_dummy()
        Ram.create_dummy()
        BatteryTime.create_dummy()

        self.stdout.write(self.style.SUCCESS("Deployment was successful"))