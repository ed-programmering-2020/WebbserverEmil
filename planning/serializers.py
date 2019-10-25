from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import Board, Row, List, Task


class TaskSerializer(serializers.ModelSerializer):
    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.save()
        return instance

    class Meta:
        model = Task
        fields = ("id", "title", "created_date")


class ListSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = ("id", "title", "tasks")


class RowSerializer(serializers.ModelSerializer):
    lists = ListSerializer(many=True, read_only=True)

    class Meta:
        model = Row
        fields = ("id", "title", 'lists')


class BoardSerializer(serializers.ModelSerializer):
    rows = RowSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ("id", "title", 'rows')





