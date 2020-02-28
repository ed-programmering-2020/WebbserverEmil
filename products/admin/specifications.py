from django.contrib import admin
from products.models import BaseSpecification, AlternativeSpecificationName, SpecificationType


@admin.register(SpecificationType)
class SpecificationTypeAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]


@admin.register(AlternativeSpecificationName)
class AlternativeSpecificationNameAdmin(admin.ModelAdmin):
    search_fields = ["name", "specification_type"]
    fields = ["name", "specification_type"]
    list_display = ["name"]


@admin.register(BaseSpecification)
class BaseSpecificationAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = "Specifications"
