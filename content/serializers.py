from rest_framework import serializers
from .models import Feedback, CategorySurveyAnswer, Paragraph, Newsletter


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'message', "creation_date")


class CategorySurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorySurveyAnswer
        fields = ('id', 'answer', "creation_date", "category")


class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = "__all__"


class NewsletterSerializer(serializers.ModelSerializer):
    paragraphs = ParagraphSerializer(many=True, read_only=True)

    class Meta:
        model = Newsletter
        fields = ["title", "author", "creation_date", "paragraphs"]