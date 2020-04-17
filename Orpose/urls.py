from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index


urlpatterns = [
    # API
    path("", include("products.urls")),
    path("api/", include("content.urls")),
    path("api/auth/", include("users.urls")),

    # Website
    path("", index),
    path("clone-of-erik/", admin.site.urls),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
