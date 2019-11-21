from django.contrib import admin
from .models import Product, MetaProduct, Manufacturer, Category, Spec, SpecGroup, SpecGroupCollection


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class MetaProductAdmin(admin.ModelAdmin):
    list_display = ["name", "product"]
    search_fields = ["name"]


class ManufacturerAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class SpecAdmin(admin.ModelAdmin):
    list_display = ["key", "value"]


class SpecGroupAdmin(admin.ModelAdmin):
    list_display = ["key"]


class SpecGroupCollectionAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(Product, ProductAdmin)
admin.site.register(MetaProduct, MetaProductAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Spec, SpecAdmin)
admin.site.register(SpecGroup, SpecGroupAdmin)
admin.site.register(SpecGroupCollection, SpecGroupCollectionAdmin)
