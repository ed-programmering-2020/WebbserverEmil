from Orpose.models import GraphicsCard, Processor
from django.contrib import admin


@admin.register(GraphicsCard)
class GraphicsCardAdmin(admin.ModelAdmin):
    list_display = ["value", "score"]
    search_fields = ["value"]
    ordering = ["value"]


@admin.register(Processor)
class ProcessorAdmin(admin.ModelAdmin):
    list_display = ["value", "score"]
    search_fields = ["value"]
    ordering = ["value"]
