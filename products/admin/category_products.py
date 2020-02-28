from django.contrib import admin
from products.models import Laptop, AlternativeCategoryName, CategoryProductType, BaseCategoryProduct
from .tags import get_image_tag


@admin.register(AlternativeCategoryName)
class AlternativeCategoryNameAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    fields = ["name", "category_product_type"]
    list_display = ["name", "category_product_type"]


@admin.register(CategoryProductType)
class CategoryProductTypeAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]


class BaseCategoryProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Main info", {
            "fields": ["name", "manufacturing_name", "price", "score"]
        })
    ]

    list_display = ["name", "price", "score", "serve_image"]
    search_fields = ["name", "manufacturing_name"]

    def serve_image(self, obj):
        return get_image_tag(obj.get_image())
    serve_image.short_description = 'Image'
    serve_image.allow_tags = True


@admin.register(Laptop)
class LaptopAdmin(BaseCategoryProductAdmin):
    fieldsets = BaseCategoryProductAdmin.fieldsets
    fieldsets.append(
        ("Specifications", {
            "fields": [
                "battery_time",
                "weight",
                "processor",
                "graphics_card",
                "storage_size",
                "storage_type",
                "ram",
                "panel_type",
                "refresh_rate",
                "resolution",
                "screen_size"
            ]
        })
    )
