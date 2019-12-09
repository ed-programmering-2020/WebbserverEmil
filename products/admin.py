from django.contrib import admin
from .models import Product, MetaProduct, Manufacturer, MetaCategory, Spec, SpecGroup, SpecGroupCollection, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "manufacturer", "category", "image_tag"]
    search_fields = ["name"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    search_fields = ["name"]


class MetaCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "is_active", "created_date"]
    search_fields = ["name"]


class MetaProductAdmin(admin.ModelAdmin):
    list_display = ["name", "product", "image_tag"]
    search_fields = ["name"]


class ManufacturerAdmin(admin.ModelAdmin):
    pass


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
admin.site.register(MetaCategory, MetaCategoryAdmin)
admin.site.register(Spec, SpecAdmin)
admin.site.register(SpecGroup, SpecGroupAdmin)
admin.site.register(SpecGroupCollection, SpecGroupCollectionAdmin)
