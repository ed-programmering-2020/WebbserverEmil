from django.urls import path
from products.views import ProductAPI, ProductsAPI, MatchAPI

urlpatterns = [
    path("product/<str:category>/<str:slug>", ProductAPI.as_view()),
    path("match/<str:category>", MatchAPI.as_view()),
    path("scraping/products/", ProductsAPI.as_view()),
]
