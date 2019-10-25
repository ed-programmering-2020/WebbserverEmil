from django.shortcuts import render
from django.views.generic import View
from users.models import User


class Index(View):
    def get(self, request):
        return render(request, "board.html")


class Profile(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        params = {
            "user": user
        }
        return render(request, "profile.html", params)
