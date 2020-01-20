from django.contrib import admin
from .models import Product, MetaProduct, Spec, SpecGroup, SpecGroupCollection


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "meta_category"]
    search_fields = ["name"]


class MetaProductAdmin(admin.ModelAdmin):
    list_display = ["name", "product", "serve_admin_image"]
    search_fields = ["name"]


class SpecGroupAdmin(admin.ModelAdmin):
    list_display = ["key", "spec_group_collection"]
    search_fields = ["key"]


class SpecGroupCollectionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class SpecAdmin(admin.ModelAdmin):
    list_display = ["key", "value", "spec_group"]
    search_fields = ["key", "value"]


admin.site.register(Product, ProductAdmin)
admin.site.register(MetaProduct, MetaProductAdmin)
admin.site.register(Spec, SpecAdmin)
admin.site.register(SpecGroup, SpecGroupAdmin)
admin.site.register(SpecGroupCollection, SpecGroupCollectionAdmin)
