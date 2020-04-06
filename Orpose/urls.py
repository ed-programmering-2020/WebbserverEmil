from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import FrontendAppView


urlpatterns = [
    path("clone-of-erik", admin.site.urls),
    path("", include("products.urls")),
    path("api/", include("content.urls")),
    path("api/auth/", include("users.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if not getattr(settings, "DEBUG", None):
    urlpatterns.append(re_path(r'.*', FrontendAppView.as_view()))
