from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from products.serializers import ProductSerializer
from rest_framework import generics
import json


def import_category(name):
    name = "products.models.categories." + name
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


class MatchAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get(self, request, name, *args, **kwargs):
        category = import_category(name).objects.get(name=name)
        settings = json.loads(request.GET["settings"])
        products = category.match(settings)

        if products:
            # serialized_alternatives = []
            # if products["alternatives"]:
            #     for product in products["alternatives"]:
            #         serialized_alternatives.append(ProductSerializer(product).data)

            top_product = products[0]
            serialized_product = ProductSerializer(top_product).data

            return Response({
                "main": serialized_product,
            })
        else:
            return Response({"main": None})