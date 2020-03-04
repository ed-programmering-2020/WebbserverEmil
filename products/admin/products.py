from products.models import Product, Price
from .tags import get_image_tag, get_url_tag
from django.contrib import admin


class PriceInline(admin.TabularInline):
    model = Price
    verbose_name_plural = "Price history"
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": ["name", "manufacturing_name", "url", "category", "_specifications"]
        }),
        ("More", {
            "classes": ["collapse"],
            "fields": ["category_product", "host"]
        })
    ]
    inlines = [PriceInline]

    list_display = [
        "name",
        "view_price",
        "serve_url",
        "serve_image",
        "host",
    ]
    list_filter = [
        "host"
    ]
    search_fields = ["name", "manufacturing_name"]

    def serve_url(self, obj):
        return get_url_tag(obj.url)
    serve_url.short_description = 'Url'
    serve_url.allow_tags = True

    def serve_image(self, obj):
        return get_image_tag(obj.image)
    serve_image.short_description = 'Image'
    serve_image.allow_tags = True

    def view_price(self, obj):
        return "%s kr" % obj.price
    view_price.short_description = "Price"


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ["_value", "date_seen", "product"]
    ordering = ["date_seen"]
