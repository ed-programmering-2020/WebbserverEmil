from django.contrib import admin
from products.models import BaseSpecification, AlternativeName


class AlternativeNameInline(admin.TabularInline):
    model = AlternativeName


@admin.register(BaseSpecification)
class BaseSpecificationAdmin(admin.ModelAdmin):
    list_display = ["score", "content_type"]
