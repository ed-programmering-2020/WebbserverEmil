from django.contrib import admin
from .models import Category, MetaCategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    search_fields = ["name"]


class MetaCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "is_active"]
    search_fields = ["name"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(MetaCategory, MetaCategoryAdmin)
