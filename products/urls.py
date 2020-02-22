from django.urls import path
from products.views import ProductAPI, ProductsAPI, MatchAPI, RecommendedAPI, CustomizationAPI

urlpatterns = [
    path("product/<str:name>", ProductAPI.as_view()),
    path("scraping/products/", ProductsAPI.as_view()),
    path("match/<str:name>", MatchAPI.as_view()),
    path("recommended/<str:name>/<str:usage>", RecommendedAPI.as_view()),
    path("customization/<str:name>", CustomizationAPI.as_view())
]
