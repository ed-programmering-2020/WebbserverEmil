from django.contrib import admin
from .models import Task, List, Row, Board


class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "created_date", "list"]
    list_filter = ["created_date", ]
    ordering = ["created_date"]
    search_fields = ["title"]


class ListAdmin(admin.ModelAdmin):
    list_display = ["title", "row"]
    search_fields = ["title"]


class RowAdmin(admin.ModelAdmin):
    list_display = ["title", "board"]
    search_fields = ["title"]


class BoardAdmin(admin.ModelAdmin):
    list_display = ["title", "created_date"]
    list_filter = ["created_date", ]
    ordering = ["created_date"]
    search_fields = ["title"]


admin.site.register(Task, TaskAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(Row, RowAdmin)
admin.site.register(Board, BoardAdmin)
