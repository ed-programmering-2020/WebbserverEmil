from django.http import HttpResponseForbidden
from django.views.generic import View
from users.models import User


class Index(View):
    def get(self, request):
        return HttpResponseForbidden("Forbidden")

