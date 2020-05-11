from django.urls import path
from products.views import LaptopAPI, ScrapingAPI

urlpatterns = [
    path("laptop/<int:laptop_id>/<str:slug>", LaptopAPI.as_view()),
    path("scraping/products/", ScrapingAPI.as_view()),
]
