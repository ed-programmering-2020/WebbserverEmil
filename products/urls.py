from django.urls import path
from .views import MatchAPI

urlpatterns = [
    path("match/<string:name>", MatchAPI.as_view()),
]