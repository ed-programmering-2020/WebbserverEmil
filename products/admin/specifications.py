from django.contrib import admin
from products.models import BaseSpecification, AlternativeSpecificationName, SpecificationType


class AlternativeNameInline(admin.TabularInline):
    model = AlternativeSpecificationName


@admin.register(SpecificationType)
class SpecificationTypeAdmin(admin.ModelAdmin):
    inlines = [AlternativeNameInline]
    fields = ["name"]
    list_display = ["name"]


@admin.register(AlternativeSpecificationName)
class AlternativeSpecificationNameAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    fields = ["name", "specification_type", "host"]
    list_display = ["name", "specification_type", "host"]


@admin.register(BaseSpecification)
class BaseSpecificationAdmin(admin.ModelAdmin):
    pass
