from django.contrib import admin
from .models import Product, MetaProduct, SpecValue, SpecKey, SpecGroup, Price, Website, Country, Category, MetaCategory


class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "currency", "currency_short"]
    list_filter = ["is_active"]
    search_fields = ["name"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "meta_category", "manufacturing_name"]
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


class SpecGroupAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class PriceAdmin(admin.ModelAdmin):
    list_display = ["price", "meta_product"]
    search_fields = ["meta_product"]


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "url", "country", "is_active"]
    list_filter = ["is_active", "country"]
    ordering = ["country"]
    search_fields = ["name", "url", "country"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "product_count", "is_active"]
    search_fields = ["name"]


class MetaCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "created_date"]
    search_fields = ["name"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(MetaCategory, MetaCategoryAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(MetaProduct, MetaProductAdmin)
admin.site.register(SpecValue, SpecValueAdmin)
admin.site.register(SpecKey, SpecKeyAdmin)
admin.site.register(SpecGroup, SpecGroupAdmin)
admin.site.register(Price, PriceAdmin)
