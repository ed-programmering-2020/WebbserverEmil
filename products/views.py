from products.serializers import ProductSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics
from products.models import Product


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
