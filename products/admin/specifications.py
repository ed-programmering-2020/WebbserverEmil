from django.contrib import admin
from products.models import BaseSpecification, AlternativeSpecificationName


@admin.register(BaseSpecification)
class BaseSpecificationAdmin(admin.ModelAdmin):

    class Meta:
        verbose_name_plural = "Specifications"


@admin.register(AlternativeSpecificationName)
class AlternativeSpecificationNameAdmin(admin.ModelAdmin):

    class Meta:
        verbose_name_plural = "Alternative specification names"
