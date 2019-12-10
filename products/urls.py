from django.urls import path
from .views import MatchAPI

urlpatterns = [
    path("match/<str:name>", MatchAPI.as_view()),
]