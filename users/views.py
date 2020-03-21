from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics

from knox.models import AuthToken
from users.models import User

from .serializers import UserSerializer, LoginUserSerializer, RegisterUserSerializer


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class TokenAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, requests, *args, **kwargs):
        user = self.request.user
        AuthToken.objects.filter(user=user).delete()
        return Response({"token": AuthToken.objects.create(user)[1]})


class RegistrationAPI(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LogoutAPI(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.GET.get("user_id"))
        AuthToken.objects.filter(user=user).delete()

        return Response({})
