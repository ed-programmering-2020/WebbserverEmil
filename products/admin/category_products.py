from django.contrib import admin
from products.models import Laptop
from .tags import get_image_tag


class BaseCategoryProductAdmin(admin.ModelAdmin):
    # Edit page
    fields = ["name", "manufacturing_name", "price", "meta_category"]
    readonly_fields = ["average_score", "_scores"]

    # List page
    list_display = ["name", "price", "average_score", "view_meta_product_count", "serve_image"]
    search_fields = ["name", "manufacturing_name"]

    def serve_image(self, obj):
        return get_image_tag(obj.get_image())
    serve_image.short_description = 'Image'
    serve_image.allow_tags = True

    def view_meta_product_count(self, obj):
        return obj.meta_products.count()
    view_meta_product_count.short_description = "Meta-products"


@admin.register(Laptop)
class LaptopAdmin(BaseCategoryProductAdmin):
    pass
