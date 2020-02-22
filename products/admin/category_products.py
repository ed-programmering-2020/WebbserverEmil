from django.contrib import admin
from products.models import Laptop
from .tags import get_image_tag


class BaseCategoryProductAdmin(admin.ModelAdmin):
    # Edit page
    fields = ["name", "manufacturing_name", "price"]
    readonly_fields = ["score"]

    # List page
    list_display = ["name", "price", "score", "serve_image"]
    search_fields = ["name", "manufacturing_name"]

    def serve_image(self, obj):
        return get_image_tag(obj.get_image())
    serve_image.short_description = 'Image'
    serve_image.allow_tags = True


@admin.register(Laptop)
class LaptopAdmin(BaseCategoryProductAdmin):
    pass
