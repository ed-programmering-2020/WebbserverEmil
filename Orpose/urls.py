from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from .views import FrontendAppView
import os


urlpatterns = [
    path("clone-of-erik", admin.site.urls),
    path("", include("products.urls")),
    path("api/", include("content.urls")),
    path("api/auth/", include("users.urls")),
    re_path(r"^sitemap.xml$", TemplateView.as_view(template_name=os.path.join(settings.BASE_DIR, "static", "sitemap.xml"), content_type="application/xml")),
    re_path(r"^robots.txt$", TemplateView.as_view(template_name=os.path.join(settings.BASE_DIR, "static", "robots.txt"), content_type="text/plain")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not getattr(settings, "DEBUG", None):
    urlpatterns.append(re_path(r'.*', FrontendAppView.as_view()))