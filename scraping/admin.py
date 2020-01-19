from django.contrib import admin
from .models import Website


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "url", "country", "is_active"]
    list_filter = ["is_active", "country"]
    ordering = ["country"]
    search_fields = ["name", "url", "country"]


admin.site.register(Website, WebsiteAdmin)
