from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.response import Response
from products.serializers import CategoryProductSerializer
from products.models import Laptop


class LaptopAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategoryProductSerializer

    def get(self, request, laptop_id, slug, *args, **kwargs):
        try:
            laptop = Laptop.objects.get(id=laptop_id)
            return Response(CategoryProductSerializer(laptop).data)
        except Laptop.DoesNotExist:
            return Response({})
