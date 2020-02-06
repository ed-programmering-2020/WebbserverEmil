from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics
from .serializers import FeedbackSerializer
from .models import Feedback


class FeedbackAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = FeedbackSerializer

    def post(self, request, *args, **kwargs):
        message = request.POST["message"]
        Feedback.objects.create(message=message)
        return Response({"message": "success"})
