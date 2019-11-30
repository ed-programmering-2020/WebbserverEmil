from django.contrib import admin
from .models import Product, MetaProduct, Manufacturer, Category, Spec, SpecGroup, SpecGroupCollection


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "manufacturer", "image_tag"]
    search_fields = ["name"]


class MetaProductAdmin(admin.ModelAdmin):
    list_display = ["name", "product", "image_tag"]
    search_fields = ["name"]


class ManufacturerAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]


class SpecAdmin(admin.ModelAdmin):
    list_display = ["key", "value", "spec_group"]
    search_fields = ["key", "value"]


class SpecGroupAdmin(admin.ModelAdmin):
    list_display = ["key", "spec_group_collection"]
    search_fields = ["key"]


class SpecGroupCollectionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


admin.site.register(Product, ProductAdmin)
admin.site.register(MetaProduct, MetaProductAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Spec, SpecAdmin)
admin.site.register(SpecGroup, SpecGroupAdmin)
admin.site.register(SpecGroupCollection, SpecGroupCollectionAdmin)
