from products.models.category_products.base import BaseCategoryProduct
from collections import defaultdict
from operator import itemgetter
from django.db import models


def get_foreign_key(model_name):
    return models.ForeignKey("products." + model_name, related_name="laptops", null=True, on_delete=models.SET_NULL)


class Laptop(BaseCategoryProduct):
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

        def get_priority(value):
            return value / 5

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

            if settings["usage"] == "general":
                usage_score += laptop.battery_time.score * 1.3  # Battery time
                usage_score += laptop.weight.score * 1.3  # Weight
                usage_score += laptop.processor.score  # Processor
                usage_score += laptop.graphics_card.score * 0.7  # Graphics card
                usage_score += laptop.refresh_rate.score * 0.7  # Refresh rate

            elif settings["usage"] == "gaming":
                usage_score += laptop.battery_time.score * 0.7  # Battery time
                usage_score += laptop.weight.score * 0.7  # Weight
                usage_score += laptop.processor.score * 1.15  # Processor
                usage_score += laptop.graphics_card.score * 1.3  # Graphics card
                usage_score += laptop.refresh_rate.score * 1.15  # Refresh rate

            usage_score += laptop.ram.score  # Ram
            usage_score += laptop.storage_type.score  # Storage type
            usage_score += laptop.storage_size.score  # Storage size
            usage_score += laptop.resolution.score  # Resolution
            usage_score += laptop.panel_type.score  # Panel type

            sorted_laptops[laptop.id] = {"usage": usage_score}
        laptops = sorted(sorted_laptops, key=itemgetter("usage"), reverse=True)[:10]

        # Get priority score
        priorities = settings.get("priorities", None)
        if priorities is not None:
            weight = get_priority(priorities["weight"])
            battery = get_priority(priorities["battery"])
            performance = get_priority(priorities["performance"])
            storage = get_priority(priorities["storage"])
            screen = get_priority(priorities["screen"])

            for laptop in laptops:
                priority_score = 0

                priority_score += laptop.weight.score * weight  # Weight
                priority_score += laptop.battery_time.score * battery  # Battery time
                priority_score += laptop.storage_size.score * storage  # Storage size

                priority_score += laptop.processor.score * performance  # Processor
                priority_score += laptop.graphics_card.score * performance  # Graphics card
                priority_score += laptop.ram.score * performance  # Ram
                priority_score += laptop.storage_type.score * performance  # Storage type

                priority_score += laptop.refresh_rate.score * screen  # Refresh rate
                priority_score += laptop.resolution.score * screen  # Resolution
                priority_score += laptop.panel_type.score * screen  # Panel type

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
                    score += specification.score

                laptop.score = score / laptop.price
                laptop.is_ranked = True
                laptop.save()
