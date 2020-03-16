from rest_framework import serializers
from .models import Feedback, CategorySurveyAnswer


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'message', "creation_date")


class CategorySurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorySurveyAnswer
        fields = ('id', 'answer', "creation_date", "category")
