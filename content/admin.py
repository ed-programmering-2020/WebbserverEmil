from django.contrib import admin
from .models import Feedback, CategorySurveyAnswer, Newsletter


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["message", "creation_date"]
    search_fields = ["message"]
    ordering = ["creation_date"]


@admin.register(CategorySurveyAnswer)
class CategorySurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ["answer", "creation_date", "category"]
    search_fields = ["answer"]
    ordering = ["creation_date"]


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "creation_date"]
    search_fields = ["title"]
    ordering = ["creation_date"]
