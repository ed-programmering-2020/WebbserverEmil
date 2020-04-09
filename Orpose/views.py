from django.http import HttpResponse
from django.views.generic import View
import Orpose.settings.base
import os


class FrontendAppView(View):
    def get(self, request):
        try:
            with open(os.path.join(Orpose.settings.base.BASE_DIR, 'static', 'index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse("501 Server error", status=501)
