from products.models import Product, MetaProduct, SpecValue, SpecKey, Price, Website, MetaCategory
from django.utils.safestring import mark_safe
from django.contrib import admin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "meta_category",
        "average_score",
        "_scores",
        "id"
    ]
    search_fields = ["name"]


@admin.register(MetaProduct)
class MetaProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": ["name", "manufacturing_name" "view_url", "host"]
        }),
        ("Advanced options", {
            "classes": ["collapse"],
            "fields": ["specs"]
        })
    ]

    list_display = [
        "serve_admin_image",
        "name",
        "manufacturing_name",
        "view_price",
        "serve_url",
        "id"
    ]

    search_fields = ["name"]

    def serve_url(self, obj):
        return mark_safe('<a href="%s">source</a>' % obj.url)
    serve_url.short_description = 'Url'
    serve_url.allow_tags = True

    def serve_admin_image(self, obj):
        return mark_safe('<img src="/media/%s" height="50" />' % obj.image)
    serve_admin_image.short_description = 'Image'
    serve_admin_image.allow_tags = True

    def view_price(self, obj):
        return obj.get_price()


@admin.register(SpecValue)
class SpecValueAdmin(admin.ModelAdmin):
    list_display = ["value", "spec_key"]
    search_fields = ["value"]


@admin.register(SpecKey)
class SpecKeyAdmin(admin.ModelAdmin):
    list_display = ["key", "spec_group", "category"]
    search_fields = ["key"]


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ["price", "meta_product"]
    search_fields = ["meta_product"]


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "url", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "url"]


@admin.register(MetaCategory)
class MetaCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "created_date"]
    search_fields = ["name"]
