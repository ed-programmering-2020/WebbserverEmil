from django.urls import path
from .views import WebsitesAPI, ProductsAPI, AllWebsitesAPI

urlpatterns = [
    path("websites/", WebsitesAPI.as_view()),
    path("products/", ProductsAPI.as_view()),
    path("all-websites/", AllWebsitesAPI.as_view())
]
