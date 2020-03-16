from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics
from .models import Feedback, CategorySurveyAnswer


class FeedbackAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        Feedback.objects.create(message=request.POST["message"])
        return Response({"message": "success"})


class CategorySurveyAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, category, *args, **kwargs):
        CategorySurveyAnswer.objects.create(
            answer=request.POST["answer"],
            category=category
        )
        return Response({"message": "success"})
