from ..models import (
    Weight,
    BatteryTime,
    StorageType,
    StorageSize,
    Ram,
    PanelType,
    RefreshRate,
    Resolution,
    ScreenSize,
    Processor,
    GraphicsCard
)


from django.contrib import admin


class SpecificationAdmin(admin.ModelAdmin):
    list_display = ["raw_value", "score"]

    search_fields = ["raw_value"]


class BenchmarkedSpecificationAdmin(SpecificationAdmin):
    list_display = SpecificationAdmin.list_display + ["full_score"]


@admin.register(BatteryTime)
class BatteryTimeAdmin(SpecificationAdmin):
    pass


@admin.register(Weight)
class WeightAdmin(SpecificationAdmin):
    pass


@admin.register(Ram)
class RamAdmin(SpecificationAdmin):
    pass


@admin.register(StorageSize)
class StorageSizeAdmin(SpecificationAdmin):
    pass


@admin.register(StorageType)
class StorageTypeAdmin(SpecificationAdmin):
    pass


@admin.register(PanelType)
class PanelTypeAdmin(SpecificationAdmin):
    pass


@admin.register(RefreshRate)
class RefreshRateAdmin(SpecificationAdmin):
    pass


@admin.register(Resolution)
class BatteryTimeAdmin(SpecificationAdmin):
    pass


@admin.register(ScreenSize)
class ScreenSizeAdmin(SpecificationAdmin):
    pass


@admin.register(Processor)
class ProcessorAdmin(BenchmarkedSpecificationAdmin):
    pass


@admin.register(GraphicsCard)
class GraphicsCardAdmin(BenchmarkedSpecificationAdmin):
    pass
