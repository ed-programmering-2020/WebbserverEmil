from rest_framework.permissions import AllowAny
from rest_framework import generics
from .models import Feedback


class FeedbackAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        message = request.POST["message"]
        Feedback.objects.create(message=message)
