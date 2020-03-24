from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from products.models import AlternativeName


@admin.register(AlternativeName)
class AlternativeNameAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "model_type"]

    fields = ["name", "model_type"]


class AlternativeNameInline(admin.TabularInline):
    model = AlternativeName


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ["app_label", "model"]

    inlines = [AlternativeNameInline]
    readonly_fields = ["app_label", "model"]
