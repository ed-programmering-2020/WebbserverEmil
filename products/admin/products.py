from django.contrib import admin
from products.models import Product, MetaProduct, SpecValue, SpecKey, Price, Website, MetaCategory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "meta_category",
        "average_score",
        "_scores",
        "id"
    ]
    search_fields = ["name"]


@admin.register(MetaProduct)
class MetaProductAdmin(admin.ModelAdmin):
    fields = [
        [
            "name",
            "manufacturing_name"
        ], [
            "view_url",
            "host",
        ], 
    ]
    list_display = [
        "name",
        "view_price",
        "manufacturing_name",
        "serve_admin_image",
        "category",
        "product",
        "id"
    ]
    search_fields = ["name"]



    def view_url(self, obj):
        return "<a href=%s>source</a>" % obj.url

    def view_price(self, obj):
        return obj.get_price()


@admin.register(SpecValue)
class SpecValueAdmin(admin.ModelAdmin):
    list_display = ["value", "spec_key"]
    search_fields = ["value"]


@admin.register(SpecKey)
class SpecKeyAdmin(admin.ModelAdmin):
    list_display = ["key", "spec_group", "category"]
    search_fields = ["key"]


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ["price", "meta_product"]
    search_fields = ["meta_product"]


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "url", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "url"]


@admin.register(MetaCategory)
class MetaCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "created_date"]
    search_fields = ["name"]
