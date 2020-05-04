from Orpose.models import Laptop, Image, MetaProduct, Website
from tabbed_admin import TabbedModelAdmin
from django.contrib import admin
from django.db.models import F
from django.utils.safestring import mark_safe
from django import forms


class WebsiteForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    model = Website


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    form = WebsiteForm
    list_display = ["id", "name", "url", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "url"]


def get_url_tag(url):
    return mark_safe('<a href="%s" target="_blank">go to</a>' % url)


class MetaProductInline(admin.TabularInline):
    model = MetaProduct

    can_delete = False
    extra = 0

    readonly_fields = ["url_tag", "host"]
    exclude = ["manufacturing_name", "category", "shipping", "rating", "review_count", "url"]


class ImageInline(admin.TabularInline):
    model = Image

    can_delete = False
    extra = 0

    readonly_fields = ["thumbnail", "host"]
    exclude = ["url"]

    def get_queryset(self, request):
        qs = super(ImageInline, self).get_queryset(request)
        return qs.order_by("-is_active", F("placement").desc(nulls_last=True))


class BaseProductAdmin(TabbedModelAdmin):
    tab_overview = [
        (None, {
            "fields": ["name", "disclaimer", "is_active"]
        }),
        ("Measurements", {
            "classes": ["collapse"],
            "fields": ["weight", "height", "width", "depth"]
        })
    ]
    tab_info = [
        (None, {
            "fields": ["manufacturing_name", "active_price", "effective_price", "slug", "rating", ]
        }),
    ]
    tabs = [
        ("Overview", tab_overview),
        ("Images", [ImageInline]),
        ("Meta products", [MetaProductInline]),
        ("Info", tab_info)
    ]
    readonly_fields = ["slug", "manufacturing_name", "rating", "active_price", "effective_price"]

    list_display = ["name", "active_price", "rating", "serve_image", "serve_url", "is_active"]
    list_filter = ["is_active", "active_price"]
    search_fields = ["name", "manufacturing_name"]

    def serve_image(self, obj):
        images = obj.images.filter(is_active=True)
        if images.count() == 0:
            return None
        return images.filter(placement=1).first().thumbnail()
    serve_image.short_description = 'Image'
    serve_image.allow_tags = True

    def serve_url(self, obj):
        return get_url_tag("https://www.orpose.se/laptop/{obj.id}/{obj.slug}".format(obj=obj))
    serve_url.short_description = "Url"
    serve_url.allow_tags = True


@admin.register(Laptop)
class LaptopAdmin(BaseProductAdmin):
    tab_overview = BaseProductAdmin.tab_overview
    tab_overview.extend([
        ("Screen", {
            "classes": ["collapse"],
            "fields": ["screen_size", "resolution", "refresh_rate", "panel_type"]
        }),
        ("Storage", {
            "classes": ["collapse"],
            "fields": ["storage_size", "storage_type"]
        }),
        ("Processing", {
            "classes": ["collapse"],
            "fields": ["processor", "graphics_card"]
        }),
        ("Other", {
            "classes": ["collapse"],
            "fields": ["ram_capacity", "battery_time", "guarantee", "color", "operating_system"]
        }),
    ])

    autocomplete_fields = ["processor", "graphics_card"]


@admin.register(MetaProduct)
class MetaProductAdmin(admin.ModelAdmin):
    list_display = ["name", "active_price", "url", "host"]
    list_filter = ["host"]
    search_fields = ["name", "manufacturing_name"]
    ordering = ["name"]
