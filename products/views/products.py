from rest_framework.permissions import AllowAny
from rest_framework import generics


class ProductAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, name, *args, **kwargs):
        pass
