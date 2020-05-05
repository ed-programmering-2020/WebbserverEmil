from django.urls import path
from products.views import LaptopAPI, ScrapingAPI, MatchAPI, SearchAPI, products_sitemap

urlpatterns = [
    path("laptop/<int:laptop_id>/<str:slug>", LaptopAPI.as_view()),
    path("scraping/products/", ScrapingAPI.as_view()),
    path("match/<str:category>", MatchAPI.as_view()),
    path("search/<str:query>", SearchAPI.as_view()),
    path("products-sitemap", products_sitemap)
]
