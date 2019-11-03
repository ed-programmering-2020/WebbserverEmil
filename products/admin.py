from django.contrib import admin
from .models import Product, MetaProduct, Group, Manufacturer, ProductLine, Category


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ["name"]
    search_fields = ["name"]


class MetaProductAdmin(admin.ModelAdmin):
    model = MetaProduct
    list_display = ["name", "product"]
    search_fields = ["name"]


class GroupAdmin(admin.ModelAdmin):
    model = Group


class ManufacturerAdmin(admin.ModelAdmin):
    model = Manufacturer


class ProductLineAdmin(admin.ModelAdmin):
    model = ProductLine


class CategoryAdmin(admin.ModelAdmin):
    model = Category


admin.site.register(Product, ProductAdmin)
admin.site.register(MetaProduct, MetaProductAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(Category, CategoryAdmin)
