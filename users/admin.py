from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "joined"]
    list_filter = ["joined", ]
    ordering = ["joined"]
    search_fields = ["username", ]


admin.site.register(User, UserAdmin)
