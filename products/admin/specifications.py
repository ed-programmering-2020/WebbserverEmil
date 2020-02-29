from django.contrib import admin
from products.models import BaseSpecification, AlternativeSpecificationName, SpecificationType


@admin.register(SpecificationType)
class SpecificationTypeAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]


@admin.register(AlternativeSpecificationName)
class AlternativeSpecificationNameAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    fields = ["name", "specification_type", "host"]
    list_display = ["name", "specification_type", "host"]


@admin.register(BaseSpecification)
class BaseSpecificationAdmin(admin.ModelAdmin):
    fields = ["score"]

    class Meta:
        verbose_name = "Specification"
