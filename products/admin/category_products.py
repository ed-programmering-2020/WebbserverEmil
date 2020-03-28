from django.utils.safestring import mark_safe
from django.contrib import admin

from products.models import Laptop, Product, Image
from .tags import get_image_tag


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    exclude = ["manufacturing_name", "category"]


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class BaseCategoryProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Main info", {
            "fields": ["name", "manufacturing_name", "active_price", "is_active"]
        })
    ]
    inlines = [ImageInline, ProductInline]

    list_display = ["name", "active_price", "serve_image", "serve_url", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "manufacturing_name"]

    def serve_image(self, obj):
        images = obj.images
        if len(images) == 0:
            return None

        return get_image_tag(images[0]["url"])
    serve_image.short_description = 'Image'
    serve_image.allow_tags = True

    def serve_url(self, obj):
        return mark_safe('<a href="/laptop/{obj.id}/{obj.slug}" target="_blank">Go to</a>'.format(obj=obj))
    serve_url.short_description = "Url"
    serve_url.allow_tags = True


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
