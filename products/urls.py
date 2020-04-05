from django.urls import path
from products.views import LaptopAPI, ScrapingAPI, MatchAPI, SearchAPI, products_sitemap

urlpatterns = [
    path("api/laptop/<int:laptop_id>/<str:slug>", LaptopAPI.as_view()),
    path("api/scraping/products/", ScrapingAPI.as_view()),
    path("api/match/<str:category>", MatchAPI.as_view()),
    path("api/search/<str:query>", SearchAPI.as_view()),
    path("products-sitemap", products_sitemap)
]
