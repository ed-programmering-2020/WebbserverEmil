from django.contrib import admin
from .models import Product, MetaProduct, Manufacturer, Category, Spec, SpecGroup, SpecGroupCollection


class ProductAdmin(admin.ModelAdmin):
    fields = ['image_tag']
    readonly_fields = ['image_tag']
    list_display = ["name", "category", "manufacturer"]
    search_fields = ["name"]

    def image_tag(self, obj):
        return u'<img src="%s" />' % obj.image
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class MetaProductAdmin(admin.ModelAdmin):
    fields = ['image_tag']
    readonly_fields = ['image_tag']
    list_display = ["name", "product"]
    search_fields = ["name"]

    def image_tag(self, obj):
        return u'<img src="%s" />' % obj.image
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


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
