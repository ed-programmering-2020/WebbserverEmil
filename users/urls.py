from django.contrib import admin
from django.urls import path, include

from .views import RegistrationAPI, LoginAPI, UserAPI, LogoutAPI


urlpatterns = [
    path("register/", RegistrationAPI.as_view()),
    path("login/", LoginAPI.as_view()),
    path("logout/", LogoutAPI.as_view()),
    path("user/", UserAPI.as_view())
]
