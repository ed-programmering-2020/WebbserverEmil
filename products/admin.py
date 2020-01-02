from django.contrib import admin
from .models import Product, MetaProduct, Manufacturer, Spec


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "manufacturer", "meta_category", "serve_admin_image"]
    search_fields = ["name"]


class MetaProductAdmin(admin.ModelAdmin):
    list_display = ["name", "product", "serve_admin_image"]
    search_fields = ["name"]


class ManufacturerAdmin(admin.ModelAdmin):
    pass


class SpecAdmin(admin.ModelAdmin):
    list_display = ["key", "value", "spec_group"]
    search_fields = ["key", "value"]


admin.site.register(Product, ProductAdmin)
admin.site.register(MetaProduct, MetaProductAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Spec, SpecAdmin)
