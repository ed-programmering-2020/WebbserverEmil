from django.contrib import admin
from products.models import BaseSpecification, AlternativeSpecificationName, SpecificationType


@admin.register(SpecificationType)
class SpecificationTypeAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]


@admin.register(AlternativeSpecificationName)
class AlternativeSpecificationNameAdmin(admin.ModelAdmin):
    fields = ["name"]
    list_display = ["name"]


@admin.register(BaseSpecification)
class BaseSpecificationAdmin(admin.ModelAdmin):
    pass
