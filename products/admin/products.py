from products.models import Product, MetaProduct, SpecValue, SpecKey, Price, Website, MetaCategory
from .tags import get_image_tag, get_url_tag
from django.contrib import admin


class MetaProductInline(admin.TabularInline):
    model = MetaProduct
    extra = 0
    verbose_name = "Meta-product"
    verbose_name_plural = "Meta-products"

    exclude = ["manufacturing_name", "_specs", "host", "image"]
    classes = ["collapse"]


class SpecValueInline(admin.TabularInline):
    model = Product.spec_values.through
    extra = 0
    verbose_name = "Spec-value"
    verbose_name_plural = "Specifications"

    classes = ["collapse"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Edit page
    fields = ["name", "manufacturing_name", "price", "meta_category"]
    readonly_fields = ["average_score", "_scores"]
    inlines = [MetaProductInline, SpecValueInline]

    # List page
    list_display = ["name", "price", "average_score", "view_meta_product_count", "serve_image"]
    search_fields = ["name", "manufacturing_name"]

    def serve_image(self, obj):
        return get_image_tag(obj.get_image())
    serve_image.short_description = 'Image'
    serve_image.allow_tags = True

    def view_meta_product_count(self, obj):
        return obj.meta_products.count()
    view_meta_product_count.short_description = "Meta-products"


@admin.register(MetaProduct)
class MetaProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": ["name", "manufacturing_name", "url", "category", "_specs"]
        }),
        ("More", {
            "classes": ["collapse"],
            "fields": ["product", "host"]
        })
    ]

    list_display = [
        "name",
        "view_price",
        "serve_url",
        "serve_image",
    ]

    search_fields = ["name", "manufacturing_name"]

    def serve_url(self, obj):
        return get_url_tag(obj.url)
    serve_url.short_description = 'Url'
    serve_url.allow_tags = True

    def serve_image(self, obj):
        return get_image_tag(obj.image)
    serve_image.short_description = 'Image'
    serve_image.allow_tags = True

    def view_price(self, obj):
        return "%s kr" % obj.get_price()
    view_price.short_description = "Price"


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
