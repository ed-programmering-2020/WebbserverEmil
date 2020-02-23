from .base import BaseCategoryProduct
from django.db import models


class Laptop(BaseCategoryProduct):
    def get_foreign_key(self, model_name):
        return models.ForeignKey("products."+model_name, related_name="laptops", on_delete=models.SET_NULL)

    # Measurements
    battery_time = get_foreign_key("BatteryTime")
    weight = get_foreign_key("Weight"),

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
