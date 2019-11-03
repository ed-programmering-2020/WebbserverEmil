from django.urls import path
from .views import WebsitesAPI, ProductsAPI

urlpatterns = [
    path("websites/", WebsitesAPI.as_view()),
    path("products/", ProductsAPI.as_view()),
]