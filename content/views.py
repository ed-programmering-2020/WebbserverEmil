from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics
from .serializers import FeedbackSerializer, CategorySurveyAnswerSerializer
from .models import Feedback, CategorySurveyAnswer


class FeedbackAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = FeedbackSerializer

    def post(self, request, *args, **kwargs):
        Feedback.objects.create(message=request.POST["message"])
        return Response({"message": "success"})


class CategorySurveyAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySurveyAnswerSerializer

    def post(self, request, category, *args, **kwargs):
        CategorySurveyAnswer.objects.create(
            answer=request.POST["answer"],
            category=category
        )
        return Response({"message": "success"})

