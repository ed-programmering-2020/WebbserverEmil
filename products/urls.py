from django.urls import path
from .views import CategoriesAPI, ProductsAPI

urlpatterns = [
    path("categories/", CategoriesAPI.as_view()),
    path("products/", ProductsAPI.as_view()),
]