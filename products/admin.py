from django.contrib import admin
from .models import Product, MetaProduct, SpecValue, SpecKey, SpecGroup, Price


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "meta_category"]
    search_fields = ["name"]


class MetaProductAdmin(admin.ModelAdmin):
    list_display = ["name", "product", "serve_admin_image"]
    search_fields = ["name"]


class SpecValueAdmin(admin.ModelAdmin):
    list_display = ["key", "value"]
    search_fields = ["key", "value"]


class SpecKeyAdmin(admin.ModelAdmin):
    list_display = ["key", "spec_group"]
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
