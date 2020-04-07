from django.urls import path
from .views import FeedbackAPI, CategorySurveyAPI, NewslettersAPI, NewsletterAPI, FrontendErrorAPI


urlpatterns = [
    path("feedback", FeedbackAPI.as_view()),
    path("error", FrontendErrorAPI.as_view()),
    path("survey/<str:category>", CategorySurveyAPI.as_view()),
    path("newsletters", NewslettersAPI.as_view()),
    path("newsletters/<int:id>", NewsletterAPI.as_view())
]