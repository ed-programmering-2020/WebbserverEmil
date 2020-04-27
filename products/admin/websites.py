from products.models import Website
from django.contrib import admin
from django import forms


class WebsiteForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    model = Website


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    form = WebsiteForm
    list_display = ["id", "name", "url", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "url"]
