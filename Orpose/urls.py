from django.contrib import admin
from django.urls import path, include
from .views import index


urlpatterns = [
    # API
    path("api/", include("products.urls")),
    path("auth/", include("users.urls")),

    # Website
    path("", index),
    path("admin/", admin.site.urls),

]
