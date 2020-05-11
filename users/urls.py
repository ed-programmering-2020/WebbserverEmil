from django.urls import path
from .views import RegistrationAPI, LoginAPI, UserAPI, LogoutAPI, TokenAPI


urlpatterns = [
    path("register/", RegistrationAPI.as_view()),
    path("login/", LoginAPI.as_view()),
    path("logout/", LogoutAPI.as_view()),
    path("user/", UserAPI.as_view()),
    path("token/", TokenAPI.as_view())
]
