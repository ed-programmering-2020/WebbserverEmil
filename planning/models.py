from django.db import models
from users.models import User


class Board(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="boards")
    title = models.CharField(max_length=256)
    created_date = models.DateTimeField(auto_now_add=True)


class Row(models.Model):
    id = models.AutoField(primary_key=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="rows")
    title = models.CharField(max_length=256)


class List(models.Model):
    id = models.AutoField(primary_key=True)
    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name="lists")
    title = models.CharField(max_length=256)


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=256)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
