from django.contrib import admin
from django.urls import path, include

from .views import FrontendAppView


urlpatterns = [
    path("", FrontendAppView.as_view()),
    path("admin/", admin.site.urls),
    path("api/", include("products.urls")),
    path("api/scraping/", include("scraping.urls")),
    path("api/localization/", include("localization.urls")),
    path("api/content/", include("content.urls")),
    path("api/auth/", include("users.urls")),
]
