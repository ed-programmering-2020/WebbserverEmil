from django.contrib import admin
from .models import Website, DataType, SearchGroup, SearchList, FetchInfo


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "url", "country", "is_active"]
    list_filter = ["is_active", "country"]
    ordering = ["country"]
    search_fields = ["name", "url", "country"]


class DataTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


class SearchGroupAdmin(admin.ModelAdmin):
    list_display = ["id", "website", "group_type"]


class SearchListAdmin(admin.ModelAdmin):
    list_display = ["id", "search_group"]
    search_fields = ["search_group"]


class FetchInfoAdmin(admin.ModelAdmin):
    list_display = ["id", "search_list"]
    ordering = ["time"]


admin.site.register(Website, WebsiteAdmin)
admin.site.register(DataType, DataTypeAdmin)
admin.site.register(SearchGroup, SearchGroupAdmin)
admin.site.register(SearchList, SearchListAdmin)
admin.site.register(FetchInfo, FetchInfoAdmin)
