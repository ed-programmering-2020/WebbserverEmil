from django.contrib import admin
from django.urls import path, include

from .views import Index


urlpatterns = [
    path("", Index.as_view()),
    path("admin/", admin.site.urls),
    path("api/", include("planning.urls")),
    path("api/auth/", include("knox.urls")),
    path("api/auth/", include("users.urls")),
]
