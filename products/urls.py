from django.urls import path
from .views import MatchAPI, RecommendedAPI, CustomizationAPI

urlpatterns = [
    path("match/<str:name>", MatchAPI.as_view()),
    path("recommended/<str:name>/<str:usage>", RecommendedAPI.as_view()),
    path("customization/<str:name>", CustomizationAPI.as_view())
]