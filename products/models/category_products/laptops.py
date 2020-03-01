from products.models.category_products.base import BaseCategoryProduct
from operator import itemgetter
from django.db import models
import json, time


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

        start = time.time()
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
        print(laptops, start - time.time())

        # Get usage score
        start = time.time()

        sorted_laptops = {}
        for laptop in laptops:
            score = 0

            for specification in Laptop.specifications:
                if settings["usage"] == "general":
                    multiplier = specification.get("general", 1)
                else:
                    multiplier = specification.get("gaming", 1)

                name = specification["name"]
                if eval("laptop.{} is not None and laptop.{}.to_rank is True".format(name, name)):
                    exec("score += laptop.{}.score * {}".format(name, multiplier))

            sorted_laptops[laptop] = score / laptop.price
        laptops = sorted(sorted_laptops.items(), key=itemgetter(1), reverse=True)
        if len(laptops) >= 10:
            laptops = laptops[:10]
        else:
            laptops = laptops[:len(laptops)]
        print(laptops, start - time.time())

        # Get priority score
        start = time.time()
        priorities = settings.get("priorities", None)
        if priorities is not None:
            priorities = json.loads(priorities)

            sorted_laptops = {}
            for laptop, __ in laptops:
                score = 0

                for specification in Laptop.specifications:
                    priority = priorities.get(specification["group"], None)
                    if priority is not None:
                        name = specification["name"]
                        exec("score += laptop.{}.score * {}".format(name, priority / 5))

                sorted_laptops[laptop] = score / laptop.price
            laptops = sorted(sorted_laptops.items(), key=itemgetter(1), reverse=True)
        print(laptops, start - time.time())

        return laptops
