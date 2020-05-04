from products.models.products.base_products import BaseProduct
from products.models.specifications.processing.processors import Processor
from products.models.specifications.processing.graphics_cards import GraphicsCard
from django.db import models

from operator import itemgetter
from decimal import Decimal

import json


def get_foreign_key(model_name):
    return models.ForeignKey(
        "products." + model_name,
        related_name="laptops",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )


class Laptop(BaseProduct):
    score_bias_table = {
        # Performance group
        "ram_capacity": {"general": 0.25, "gaming": 0.25},
        "storage_type": {"general": 1.5, "gaming": 1.5},
        "processor": {"general": 0.5, "gaming": 1.75},
        "graphics_card": {"general": 0.5, "gaming": 1.75},

        # Screen group
        "resolution": {"general": 0.5, "gaming": 0.5},
        "panel_type": {"general": 1.5, "gaming": 1.5},
        "refresh_rate": {"general": 0.25, "gaming": 0.5},

        # Others
        "battery_time": {"general": 1.5, "gaming": 0.5},  # Battery time group
        "storage_size": {"general": 1.5, "gaming": 1.5},  # Storage group
        "weight": {"general": 1.5, "gaming": 0.5},  # Weight group
        "height": {"general": 1, "gaming": 1}
    }

    storage_type_choices = (
        ("HDD", "hdd"),
        ("SSD", "ssd")
    )

    panel_type_choices = (
        ("TN", "tn"),
        ("VA", "va"),
        ("IPS", "ips"),
        ("RETINA", "retina"),
        ("OLED", "oled")
    )

    # Screen
    screen_size = models.DecimalField(null=True, max_digits=3, decimal_places=1, help_text="in inches")
    resolution = models.PositiveSmallIntegerField(null=True, help_text="in pixels")
    refresh_rate = models.PositiveSmallIntegerField(null=True, help_text="in hertz")
    panel_type = models.CharField(null=True, max_length=128, choices=panel_type_choices)

    # Storage
    storage_type = models.CharField(null=True, max_length=128, choices=storage_type_choices)
    storage_size = models.PositiveSmallIntegerField(null=True, help_text="in gigabytes")

    # Processing
    processor = models.ForeignKey(
        "products.Processor", related_name="laptops",
        null=True, blank=True, on_delete=models.SET_NULL
    )
    graphics_card = models.ForeignKey(
        "products.GraphicsCard", related_name="laptops",
        null=True, blank=True, on_delete=models.SET_NULL
    )

    # Other
    ram_capacity = models.PositiveSmallIntegerField(null=True, help_text="in gigabytes")
    battery_time = models.DecimalField(null=True, max_digits=3, decimal_places=1, help_text="in hours")
    color = models.CharField(null=True, max_length=128, help_text="primary color")
    operating_system = models.CharField(null=True, max_length=128)

    def update(self, data, exclude=[]):
        super(Laptop, self).update(data, exclude)

        if "processor" in data:
            self.processor = Processor.objects.filter(value__icontains=data["processor"]).first()
        if "graphics_card" in data:
            self.graphics_card = GraphicsCard.objects.filter(value__icontains=data["graphics_card"]).first()

    @classmethod
    def match(cls, settings):
        laptops = list(super(cls, cls).match(settings))
        price_range = json.loads(settings["price"])
        priorities = json.loads(settings["priorities"])
        usage = settings["usage"]

        # Filter with screen size
        if "size" in settings:
            size_dict = json.loads(settings["size"])
            min_size, max_size = size_dict["min"], size_dict["max"]
            laptops = [laptop for laptop in laptops
                       if laptop.screen_size and min_size <= int(laptop.screen_size) <= max_size]

        # Score laptops
        scored_laptops = {}
        for laptop in laptops:
            args = (usage, priorities)
            score = 0

            # Score performance group
            group = "performance"
            storage_types = [["hdd"], ["ssd"]]
            score += cls.get_relative_score(laptop.ram_capacity, 8) * cls.get_bias("ram_capacity", *args, group)
            score += cls.get_type_score(laptop.storage_type, storage_types) * cls.get_bias("storage_type", *args, group)
            score += cls.get_benchmarked_score(laptop.processor) * cls.get_bias("processor", *args, group)
            score += cls.get_benchmarked_score(laptop.graphics_card) * cls.get_bias("graphics_card", *args, group)

            # Score screen group
            group = "screen"
            panel_types = [["tn"], ["va"], ["ips", "retina"], ["oled"]]
            score += cls.get_relative_score(laptop.resolution, 1080) * cls.get_bias("resolution", *args, group)
            score += cls.get_type_score(laptop.panel_type, panel_types) * cls.get_bias("panel_type", *args, group)
            score += cls.get_relative_score(laptop.refresh_rate, 60) * cls.get_bias("refresh_rate", *args, group)

            # Score other groups
            score += cls.get_relative_score(laptop.weight, 1.5) * cls.get_bias("weight", *args)
            score += cls.get_relative_score(laptop.battery_time, 8) * cls.get_bias("battery_time", *args, "battery")
            score += cls.get_relative_score(laptop.storage_size, 256) * cls.get_bias("storage_size", usage)
            score += cls.get_relative_score(laptop.height, 15.0) * cls.get_bias("height", usage)

            scored_laptops[laptop] = laptop.calculate_score(score, price_range)

        laptops = sorted(scored_laptops.items(), key=itemgetter(1), reverse=True)

        if len(laptops) >= 4:
            return laptops[:4]
        return laptops

    def __str__(self):
        return "<Laptop %s>" % self.name
