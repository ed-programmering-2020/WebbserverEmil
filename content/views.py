from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics
from .serializers import FeedbackSerializer, CategorySurveyAnswerSerializer, NewsletterSerializer
from .models import Feedback, CategorySurveyAnswer, Newsletter


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


class NewslettersAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = NewsletterSerializer

    def get(self, *args, **kwargs):
        newsletters = Newsletter.objects.all().order_by("creation_date")
        return Response({"newsletters": NewsletterSerializer(newsletters, many=True).data})


class NewsletterAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = NewsletterSerializer

    def get(self, id, *args, **kwargs):
        return Response({"newsletter": NewsletterSerializer(Newsletter.objects.get(id=id)).data})
