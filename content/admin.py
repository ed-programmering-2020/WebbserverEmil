from .models import Feedback, CategorySurveyAnswer, Newsletter, Paragraph

from django.contrib import admin
from django import forms


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


class ParagraphForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Paragraph


class ParagraphInline(admin.TabularInline):
    form = ParagraphForm
    model = Paragraph
    extra = 1


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "creation_date"]
    search_fields = ["title"]
    ordering = ["creation_date"]
    inlines = [ParagraphInline]
