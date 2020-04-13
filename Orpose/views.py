from react_render.django.render import render_component
from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings
from django.shortcuts import render
import requests
import os


class FrontendAppView(View):
    html_dir = os.path.join(settings.BASE_DIR, 'static/index.html')
    bot_user_agents = ["Googlebot", "Bingbot", "Slurp",
                       "DuckDuckBot", "Baiduspider", "YandexBot",
                       "facebot", "is_archiver"]

    def check_for_bot(self, user_agent):
        for bot_user_agent in self.bot_user_agents:
            if bot_user_agent in user_agent:
                return True
        return False

    def get(self, request):
        user_agent = request.META['HTTP_USER_AGENT']

        component = render_component()
        return HttpResponse()

        if self.check_for_bot(user_agent) is True:

            return HttpResponse()
        else:
            with open(self.html_dir) as f:
                return HttpResponse(f.read())
