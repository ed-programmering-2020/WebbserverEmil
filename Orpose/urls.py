from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .views import FrontendAppView
import os


def get_file_url_path(file, content_type):
    return path(file, TemplateView.as_view(
        template_name=os.path.join(settings.STATIC_ROOT, file),
        content_type=content_type)
    )


urlpatterns = [
    path("clone-of-erik/", admin.site.urls),
    path("", include("products.urls")),
    path("api/", include("content.urls")),
    path("api/auth/", include("users.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

files = [
    ("sitemap.xml", "application/xml"),
    ("robots.txt", "text/plain"),
]


if not getattr(settings, "DEBUG", None):
    urlpatterns.append(re_path(r'.*', FrontendAppView.as_view()))
