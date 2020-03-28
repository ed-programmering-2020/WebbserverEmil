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

    list_display = ["name", "price", "url", "host"]
    list_filter = ["host"]
    search_fields = ["name", "manufacturing_name"]

