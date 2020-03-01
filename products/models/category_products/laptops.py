from products.models.category_products.base import BaseCategoryProduct
from collections import defaultdict
from operator import itemgetter
from django.db import models


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

        laptops = super().match(settings, model=Laptop)
        laptops = list(laptops)

        # Filter with size range
        size = settings.get("size", None)
        if size is not None:
            min_size, max_size = settings["size"]
            filtered_laptops = []
            for laptop in laptops:
                if min_size < laptop.screen_size < max_size:
                    filtered_laptops.append(laptop)

            laptops = filtered_laptops

        # Get usage score
        sorted_laptops = defaultdict()
        for laptop in laptops:
            usage_score = 0

            for specification in Laptop.specifications:
                if settings["usage"] == "general":
                    multiplier = specification.get("general", 1)
                else:
                    multiplier = specification.get("gaming", 1)

                eval("usage_score += laptop.{}.score * {}".format(specification["name"], multiplier))

            sorted_laptops[laptop.id] = {"usage": usage_score}
        laptops = sorted(sorted_laptops, key=itemgetter("usage"), reverse=True)[:10]

        # Get priority score
        priorities = settings.get("priorities", None)
        if priorities is not None:
            for laptop in laptops:
                priority_score = 0

                for specification in Laptop.specifications:
                    eval("priority_score += laptop.{}.score * {}".format(
                        specification["name"],
                        priorities[specification["group"]] / 5)
                    )

                sorted_laptops[laptop.id] = {"priority": priority_score}
            laptops = sorted(laptops, key=itemgetter("priority"), reverse=True)

        laptop_instances = []
        for laptop_id, __ in laptops:
            laptop_instance = BaseCategoryProduct.objects.get(id=laptop_id)
            laptop_instances.append(laptop_instance)

        return laptop_instances

    @staticmethod
    def rank():
        """Ranks the laptop products with specification scores"""

        for laptop in Laptop.objects.all().iterator():
            if not laptop.is_ranked:
                specifications = [
                    laptop.battery_time,
                    laptop.weight,
                    laptop.processor,
                    laptop.graphics_card,
                    laptop.storage_size,
                    laptop.storage_type,
                    laptop.ram,
                    laptop.panel_type,
                    laptop.refresh_rate,
                    laptop.resolution
                ]

                score = 0
                for specification in specifications:
                    if specification is not None:
                        score += specification.score

                laptop.score = score / laptop.price
                laptop.is_ranked = True
                laptop.save()
