from ..models import (Weight, BatteryTime, StorageType, StorageSize,
                      Ram, PanelType, RefreshRate, Resolution,
                      ScreenSize, Processor, GraphicsCard, Height)
from django.contrib import admin


@admin.register(
    BatteryTime, Weight, Ram, StorageSize,
    StorageType, PanelType, RefreshRate, Resolution,
    ScreenSize, Processor, GraphicsCard, Height)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ["value", "score"]
    search_fields = ["value"]
    ordering = ["value"]
