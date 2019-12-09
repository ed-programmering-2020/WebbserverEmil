from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from products.models import Category
from products.serializers import ProductSerializer


class MatchAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get(self, request, name, *args, **kwargs):
        def import_category(name):
            name = "products.models." + name
            components = name.split('.')
            mod = __import__(components[0])
            for comp in components[1:]:
                mod = getattr(mod, comp)
            return mod

        category = import_category(name).objects.get(name=name)

        settings = {
            "usage": {
                "value": "gaming"
            },
            "price": {
                "range": (1000, 4000),
            },
            "size": {
                "values": (13.3, 15.6)
            },
            "priorities": {
                "battery": 5,
                "performance": 3,
                "storage": 7,
                "screen": 5,
            }
        }

        products = category.match(settings)

        serialized_alternatives = []
        if products["alternatives"]:
            for product in products["alternatives"]:
                serialized_alternatives.append(ProductSerializer(product).data)

        return Response({
            "main": ProductSerializer(products["main"]).data,
            "alternatives": serialized_alternatives
        })
