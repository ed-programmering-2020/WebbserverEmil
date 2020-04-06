from products.models import Laptop, Image, MetaProduct
from django.contrib import admin
from django.utils.safestring import mark_safe


def get_url_tag(url):
    return mark_safe('<a href="%s" target="_blank">go to</a>' % url)


def get_image_tag(image):
    if type(image) != str:
        image = "/media/%s" % image
    return mark_safe('<img src="%s" height="50" />' % image)


class MetaProductInline(admin.TabularInline):
    model = MetaProduct
    extra = 0
    exclude = ["manufacturing_name", "category", "shipping", "rating", "review_count", "url"]


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class BaseProductAdmin(admin.ModelAdmin):
    exclude = ["rating", "effective_price", "slug"]
    inlines = [ImageInline, MetaProductInline]

    list_display = ["name", "active_price", "rating", "serve_image", "serve_url", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "manufacturing_name"]

    def serve_image(self, obj):
        images = obj.images.filter(is_active=True)
        if images.count() == 0:
            return None
        return get_image_tag(images.get(placement=1).url)
    serve_image.short_description = 'Image'
    serve_image.allow_tags = True

    def serve_url(self, obj):
        return get_url_tag("https://www.orpose.se/laptop/{obj.id}/{obj.slug}".format(obj=obj))
    serve_url.short_description = "Url"
    serve_url.allow_tags = True


@admin.register(Laptop)
class LaptopAdmin(BaseProductAdmin):
    autocomplete_fields = [
        "battery_time",
        "weight",
        "processor",
        "graphics_card",
        "storage_size",
        "storage_type",
        "ram",
        "panel_type",
        "refresh_rate",
        "resolution",
        "screen_size",
        "height"
    ]


@admin.register(MetaProduct)
class MetaProductAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "manufacturing_name",
        "standard_price",
        "campaign_price",
        "shipping",
        "availability",
        "url",
        "product",
        "host"
    ]
    list_display = ["name", "active_price", "url", "host"]
    list_filter = ["host"]
    search_fields = ["name", "manufacturing_name"]
    ordering = ["name"]
