from django.contrib import admin
from products.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "product_count", "is_active"]
    search_fields = ["name"]
