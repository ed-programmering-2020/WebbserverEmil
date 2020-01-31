from django.contrib import admin
from .models import Product, MetaProduct, SpecValue, SpecKey, SpecGroup, Price, Website, Category, MetaCategory


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "meta_category", "average_score", "_scores"]
    search_fields = ["name"]


class MetaProductAdmin(admin.ModelAdmin):
    list_display = ["name", "product", "category", "manufacturing_name", "serve_admin_image"]
    search_fields = ["name"]


class SpecValueAdmin(admin.ModelAdmin):
    list_display = ["value", "spec_key"]
    search_fields = ["value"]


class SpecKeyAdmin(admin.ModelAdmin):
    list_display = ["key", "spec_group", "category"]
    search_fields = ["key"]


class PriceAdmin(admin.ModelAdmin):
    list_display = ["price", "meta_product"]
    search_fields = ["meta_product"]


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "url", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "url"]


class MetaCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "created_date"]
    search_fields = ["name"]


admin.site.register(MetaCategory, MetaCategoryAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(MetaProduct, MetaProductAdmin)
admin.site.register(SpecValue, SpecValueAdmin)
admin.site.register(SpecKey, SpecKeyAdmin)
admin.site.register(Price, PriceAdmin)
