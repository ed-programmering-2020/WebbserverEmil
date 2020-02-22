from django.contrib import admin
from products.models import BaseSpecification, SpecificationAlternativeName


@admin.register(BaseSpecification)
class BaseSpecificationAdmin(admin.ModelAdmin):
    list_display = ["name"]

    class Meta:
        verbose_name_plural = "Specifications"


@admin.register(SpecificationAlternativeName)
class SpecificationAlternativeNameAdmin(admin.ModelAdmin):
    list_display = ["name"]

    class Meta:
        verbose_name_plural = "Alternative specification names"
