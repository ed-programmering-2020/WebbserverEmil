from django.contrib import admin
from products.models import Website


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "url", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "url"]
