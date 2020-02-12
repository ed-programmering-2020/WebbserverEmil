from django.contrib import admin
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["message", "creation_date"]
    search_fields = ["message"]
    ordering = ["creation_date"]


admin.site.register(Feedback, FeedbackAdmin)
