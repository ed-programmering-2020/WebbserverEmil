from django.urls import path
from products.views import LaptopAPI, ProductsAPI, MatchAPI

urlpatterns = [
    path("laptop/<int:laptop_id>/<str:slug>", LaptopAPI.as_view()),
    path("match/<str:category>", MatchAPI.as_view()),
    path("scraping/products/", ProductsAPI.as_view()),
]
