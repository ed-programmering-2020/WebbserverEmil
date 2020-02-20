from django.contrib import admin
from products.models import SpecGroup, Benchmark


@admin.register(Benchmark)
class BenchmarkAdmin(admin.ModelAdmin):
    list_display = ["name", "score", "spec_group"]
    search_fields = ["name"]


@admin.register(SpecGroup)
class SpecGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "verbose_name", "rank_group"]
    search_fields = ["name"]
