from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from .serializers import BoardSerializer, TaskSerializer
from .models import Board, Row, List, Task


class BoardsDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        board = Board.objects.first()
        serializer = BoardSerializer(board, context={'request': request})

        print(serializer.data)
        return Response({'data': serializer.data})

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TasksDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        task = Task.objects.get(id=id)
        serializer = TaskSerializer(task, context={'request': request})

        print(serializer.data)
        return Response({'data': serializer.data})

    def update(self, request, id):
        pass

    def post(self, request, id):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            data["list"] = List.objects.get(id=id)
            serializer.create(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
