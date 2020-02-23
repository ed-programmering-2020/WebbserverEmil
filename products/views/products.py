from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from products.serializers import ProductSerializer
from products.models import Product
from rest_framework import generics


class ProductAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get(self, request, name, *args, **kwargs):
        try:
            product = Product.objects.get(name=name)

            return Response({
                "main": ProductSerializer(product).data,
            })
        except Product.DoesNotExist:
            return Response({"main": None})


