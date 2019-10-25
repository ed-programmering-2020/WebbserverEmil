from django.urls import path
from .views import BoardsDetail, TasksDetail


urlpatterns = [
    path("boards/", BoardsDetail.as_view()),
    path("task/<int:id>", TasksDetail.as_view()),
]
