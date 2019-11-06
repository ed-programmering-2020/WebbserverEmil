from django.contrib import admin
from .models import InfoPanel


class InfoPanelAdmin(admin.ModelAdmin):
    list_display = ["name", "is_first"]
    list_filter = ["is_first"]
    search_fields = ["name"]


admin.site.register(InfoPanel, InfoPanelAdmin)
