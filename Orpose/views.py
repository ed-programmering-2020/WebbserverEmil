from django.http import HttpResponse
from django.views.generic import View
from users.models import User
import os, Orpose.settings.base


class FrontendAppView(View):
    def get(self, request):
        try:
            with open(os.path.join(Orpose.settings.base.REACT_APP_DIR, 'build', 'index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse(
                """
                This URL is only used when you have built the production
                version of the app. Visit http://localhost:3000/ instead, or
                run `yarn run build` to test the production version.
                """,
                status=501,
            )
