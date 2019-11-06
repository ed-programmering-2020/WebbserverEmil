from django.contrib import admin
from .models import Country


class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "currency", "currency_short"]
    list_filter = ["is_active"]
    search_fields = ["name"]


admin.site.register(Country, CountryAdmin)
