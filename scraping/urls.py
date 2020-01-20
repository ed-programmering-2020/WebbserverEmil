from django.urls import path
from .views import ProductsAPI

urlpatterns = [
    path("products/", ProductsAPI.as_view()),
]
