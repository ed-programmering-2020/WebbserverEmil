from django.urls import path
from .views import ProductAPI

urlpatterns = [
    path("product/<str:name>", ProductAPI.as_view()),
]
