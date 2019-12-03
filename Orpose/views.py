from django.http import HttpResponse
from django.views.generic import View
from users.models import User
import os, Orpose.settings.base


class FrontendAppView(View):
    def get(self, request):
        try:
            print(os.path.join(Orpose.settings.base.REACT_APP_DIR, 'build', 'index.html'))
            with open(os.path.join(Orpose.settings.base.REACT_APP_DIR, 'build', 'index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse("501 Server error", status=501)
