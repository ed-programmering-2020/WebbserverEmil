from operator import itemgetter
from decimal import Decimal

from products.models.category_products.base import BaseCategoryProduct
from products.models.specifications.panel import RefreshRate
from django.db import models

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
        {"name": "weight", "group": "weight", "general": 1.5, "gaming": 0.25},
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
        if self.refresh_rate is None:
            self.refresh_rate = RefreshRate.objects.get(raw_value=60)

        super(Laptop, self).save(*args, **kwargs)

    @staticmethod
    def match(settings, **kwargs):
        """Matches the user with products based on their preferences/settings

        Args:
            settings (dict): settings with matching preferences

        Returns:
            QuerySet: Matched laptops in ranked order
        """

        laptops = BaseCategoryProduct.match(settings, Laptop)
        laptops = list(laptops)
        price_range = json.loads(settings["price"])
        priorities = json.loads(settings["priorities"])

        # Filter with size range
        size = settings.get("size", None)
        if size is not None:
            size_dict = json.loads(size)
            min_price = size_dict["min"]
            max_price = size_dict["max"]

            filtered_laptops = []
            for laptop in laptops:
                if laptop.screen_size and min_price <= int(laptop.screen_size.raw_value) <= max_price:
                    filtered_laptops.append(laptop)

            laptops = filtered_laptops

        # Score laptops
        sorted_laptops = {}
        for laptop in laptops:
            score = 0

            for specification in Laptop.specification_info:
                # Check if the laptop has the given specification
                name = specification["name"]
                if not laptop.has_ranked_specification(name):
                    continue

                # Get usage multiplier
                if settings["usage"] == "general":
                    usage_mult = specification.get("general", 1)
                else:
                    usage_mult = specification.get("gaming", 1)

                if usage_mult == 1:
                    usage_mult = specification.get("all", 1)

                # Get priority multiplier
                priority = priorities[specification["group"]]
                priority_mult = priority / 2.5

                # Add score to the total
                temp_score = eval("laptop.{}.score ".format(name)) * Decimal(usage_mult + priority_mult)
                score += temp_score

                print(laptop.name, name, temp_score)

            # Divide total score by price and save it to dict
            sorted_laptops[laptop] = laptop.calculate_score(score, price_range)

        # sort laptops based on score
        laptops = sorted(sorted_laptops.items(), key=itemgetter(1), reverse=True)

        print("ranked laptops")
        for name, score in laptops:
            print(name, score)

        # Return ten category products
        if len(laptops) >= 10:
            return laptops[:10]

        return laptops
