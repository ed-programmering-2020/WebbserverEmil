from products.models.category_products.base import BaseCategoryProduct
from collections import defaultdict
from operator import itemgetter
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
    specifications = [
        {"name": "battery_time", "group": "battery", "general": 1.3, "gaming": 0.7},
        {"name": "weight", "group": "weight", "general": 1.3, "gaming": 0.7},
        {"name": "processor", "group": "performance", "gaming": 1.15},
        {"name": "graphics_card", "group": "performance", "general": 0.7, "gaming": 1.3},
        {"name": "refresh_rate", "group": "screen", "general": 0.7, "gaming": 1.3},
        {"name": "ram", "group": "performance"},
        {"name": "storage_type", "group": "performance"},
        {"name": "storage_size", "group": "storage"},
        {"name": "resolution", "group": "screen"},
        {"name": "panel_type", "group": "screen"}
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

    @staticmethod
    def match(settings, **kwargs):
        """Matches the user with products based on their preferences/settings"""

        laptops = BaseCategoryProduct.match(settings, model=Laptop)
        laptops = list(laptops)
        print(laptops)

        # Filter with size range
        size = settings.get("size", None)
        if size is not None:
            size_dict = json.loads(size)
            min_price = size_dict["min"]
            max_price = size_dict["max"]

            filtered_laptops = []
            for laptop in laptops:
                if laptop.screen_size and min_price < laptop.screen_size.value < max_price:
                    filtered_laptops.append(laptop)

            laptops = filtered_laptops
        print(laptops)

        # Get usage score
        sorted_laptops = defaultdict()
        for laptop in laptops:
            usage_score = 0

            for specification in Laptop.specifications:
                if settings["usage"] == "general":
                    multiplier = specification.get("general", 1)
                else:
                    multiplier = specification.get("gaming", 1)

                name = specification["name"]
                if exec("laptop.{}.score is not None".format(name)):
                    exec("usage_score += laptop.{}.score * {}".format(name, multiplier))

            usage_score /= laptop.price
            sorted_laptops[laptop.id] = {"usage": usage_score}
        laptops = sorted(sorted_laptops, key=itemgetter("usage"), reverse=True)[:10]
        print(laptops)

        # Get priority score
        priorities = settings.get("priorities", None)
        if priorities is not None:
            for laptop in laptops:
                priority_score = 0

                for specification in Laptop.specifications:
                    name = specification["name"]

                    if exec("laptop.{}.score is not None".format(name)):
                        priority = priorities[specification["group"]]

                        exec("priority_score += laptop.{}.score * {}".format(name, priority / 5))

                priority_score /= laptop.price
                sorted_laptops[laptop.id] = {"priority": priority_score}
            laptops = sorted(laptops, key=itemgetter("priority"), reverse=True)
        print(laptops)

        laptop_instances = []
        for laptop_id, __ in laptops:
            laptop_instance = BaseCategoryProduct.objects.get(id=laptop_id)
            laptop_instances.append(laptop_instance)

        print(laptop_instances)
        return laptop_instances
