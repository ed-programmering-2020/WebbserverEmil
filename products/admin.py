from django.contrib import admin
from .models import Product, MetaProduct, Manufacturer, Category


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


admin.site.register(Product, ProductAdmin)
admin.site.register(MetaProduct, MetaProductAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Category, CategoryAdmin)
