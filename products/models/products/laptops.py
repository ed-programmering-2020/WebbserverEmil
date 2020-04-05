from products.models.products.base import BaseCategoryProduct
from products.models.specifications.screen.panel_types import RefreshRate
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


class Laptop(BaseCategoryProduct):
    specification_info = [
        {"name": "battery_time", "group": "battery", "general": 1.5, "gaming": 0.5},
        {"name": "weight", "group": "weight", "general": 1.5, "gaming": 0.5},
        {"name": "processor", "group": "performance", "general": 0.5, "gaming": 1.75},
        {"name": "graphics_card", "group": "performance", "general": 0.5, "gaming": 1.75},
        {"name": "refresh_rate", "group": "screen", "general": 0.25, "gaming": 0.5},
        {"name": "ram", "group": "performance", "all": 0.25},
        {"name": "storage_type", "group": "performance", "all": 1.5},
        {"name": "storage_size", "group": "storage", "all": 1.5},
        {"name": "resolution", "group": "screen", "all": 0.5},
        {"name": "panel_type", "group": "screen", "all": 1.5}
    ]

    # Measurements
    battery_time = get_foreign_key("BatteryTime")
    weight = get_foreign_key("Weight")

    # Processing
    processor = get_foreign_key("Processor")
    graphics_card = get_foreign_key("GraphicsCard")

    # Memory
    storage_size = get_foreign_key("StorageSize")
    storage_type = get_foreign_key("StorageType")
    ram = get_foreign_key("Ram")

    # Panel
    panel_type = get_foreign_key("PanelType")
    refresh_rate = get_foreign_key("RefreshRate")
    resolution = get_foreign_key("Resolution")
    screen_size = get_foreign_key("ScreenSize")

    def save(self, *args, **kwargs):
        if self.refresh_rate is None:  # When None set default refresh rate
            self.refresh_rate = RefreshRate.objects.get(value=60)

        super(Laptop, self).save(*args, **kwargs)

    @classmethod
    def match(cls, settings):
        laptops = list(super(cls, cls).match(settings))
        price_range, priorities = json.loads(settings["price"]), json.loads(settings["priorities"])

        if "size" in settings:
            size_dict = json.loads(settings["size"])
            min_size, max_size = size_dict["min"], size_dict["max"]
            laptops = [laptop for laptop in laptops
                       if laptop.screen_size and min_size <= int(laptop.screen_size.value) <= max_size]

        sorted_laptops = {}
        for laptop in laptops:
            score = 0
            for specification in Laptop.specification_info:
                name = specification["name"]
                attribute = getattr(laptop, name)
                if attribute is not None or attribute.score is not None:
                    continue

                if settings["usage"] in specification:
                    usage_mult = specification[settings["usage"]]
                else:
                    usage_mult = specification.get("all", 1)

                priority = priorities[specification["group"]]
                score += attribute.score * Decimal(usage_mult + priority / 2.5)

            sorted_laptops[laptop] = laptop.calculate_score(score, price_range)

        laptops = sorted(sorted_laptops.items(), key=itemgetter(1), reverse=True)

        if len(laptops) >= 10:
            return laptops[:10]
        return laptops
