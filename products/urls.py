from django.urls import path
from products.views import ProductAPI, ProductsAPI, MatchAPI

urlpatterns = [
    path("product/<int:product_id>", ProductAPI.as_view()),
    path("scraping/products/", ProductsAPI.as_view()),
    path("match/<str:name>", MatchAPI.as_view()),
]
