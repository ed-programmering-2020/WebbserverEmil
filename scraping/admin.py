from django.contrib import admin
from .models import Website, DataType, SearchGroup, SearchList, FetchInfo


class WebsiteAdmin(admin.ModelAdmin):
    model = Website
    list_display = ["name", "url", "country", "is_active"]
    list_filter = ["is_active", "country"]
    ordering = ["country"]
    search_fields = ["name", "url", "country"]


class DataTypeAdmin(admin.ModelAdmin):
    model = DataType
    list_display = ["name"]
    search_fields = ["name"]


class SearchGroupAdmin(admin.ModelAdmin):
    model = SearchGroup
    list_display = ["website", "group_type"]


class SearchListAdmin(admin.ModelAdmin):
    model = SearchList
    list_display = ["search_group"]
    search_fields = ["search_group"]


class FetchInfoAdmin(admin.ModelAdmin):
    model = FetchInfo
    list_display = ["search_list"]
    ordering = ["time"]


admin.site.register(Website, WebsiteAdmin)
admin.site.register(DataType, DataTypeAdmin)
admin.site.register(SearchGroup, SearchGroupAdmin)
admin.site.register(SearchList, SearchListAdmin)
admin.site.register(FetchInfo, FetchInfoAdmin)
