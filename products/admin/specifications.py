from django.contrib import admin
from products.models import BenchmarkSpecification, SpecifiedSpecification, StandardSpecification


class SpecificationAdmin(admin.ModelAdmin):
    list_display = ["score", "content_type"]


@admin.register(BenchmarkSpecification)
class BenchmarkedSpecificationAdmin(SpecificationAdmin):
    pass


@admin.register(SpecifiedSpecification)
class SpecifiedSpecificationAdmin(SpecificationAdmin):
    pass


@admin.register(StandardSpecification)
class StandardSpecificationAdmin(SpecificationAdmin):
    pass
