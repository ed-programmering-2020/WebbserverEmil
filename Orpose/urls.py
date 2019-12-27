from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from .views import FrontendAppView
import os, Orpose.settings.base


urlpatterns = [
    path("knacka-på-eriks-klon/", admin.site.urls),
    path("api/", include("products.urls")),
    path("api/scraping/", include("scraping.urls")),
    path("api/localization/", include("localization.urls")),
    path("api/content/", include("content.urls")),
    path("api/auth/", include("users.urls")),
    path("/sitemap.xml", TemplateView.as_view(template_name=os.path.join(Orpose.settings.base.REACT_BUILD_DIR, "sitemap.xml"))),
    path("/robots.txt", TemplateView.as_view(template_name=os.path.join(Orpose.settings.base.REACT_BUILD_DIR, "robots.txt"))),
    path("/serviceWorker.js", TemplateView.as_view(template_name=os.path.join(Orpose.settings.base.REACT_BUILD_DIR, "serviceWorker.js"))),
    re_path(r'.*', FrontendAppView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
