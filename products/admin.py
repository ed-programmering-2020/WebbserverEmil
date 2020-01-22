from django.contrib import admin
from .models import Product, MetaProduct, SpecValue, SpecKey, SpecGroup, Price


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "meta_category", "manufacturing_name"]
    search_fields = ["name"]


class MetaProductAdmin(admin.ModelAdmin):
    list_display = ["name", "product", "category", "manufacturing_name", "serve_admin_image"]
    search_fields = ["name"]


class SpecValueAdmin(admin.ModelAdmin):
    list_display = ["value", "spec_key"]
    search_fields = ["value", "spec_key"]


class SpecKeyAdmin(admin.ModelAdmin):
    list_display = ["key", "spec_group", "category"]
    search_fields = ["key"]


class SpecGroupAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class PriceAdmin(admin.ModelAdmin):
    list_display = ["price", "meta_product"]
    search_fields = ["meta_product"]


admin.site.register(Product, ProductAdmin)
admin.site.register(MetaProduct, MetaProductAdmin)
admin.site.register(SpecValue, SpecValueAdmin)
admin.site.register(SpecKey, SpecKeyAdmin)
admin.site.register(SpecGroup, SpecGroupAdmin)
admin.site.register(Price, PriceAdmin)
