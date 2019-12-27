from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from products.models import Category
from products.serializers import ProductSerializer
import json


def import_category(name):
    name = "products.models." + name
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
        print(request.GET)
        settings = json.loads(request.GET["settings"])
        print(settings)
        print(type(settings))
        print(settings["price"])
        products = category.match(settings)

        if products:
            serialized_alternatives = []
            if products["alternatives"]:
                for product in products["alternatives"]:
                    serialized_alternatives.append(ProductSerializer(product).data)

            return Response({
                "main": ProductSerializer(products["main"]).data,
                "alternatives": serialized_alternatives
            })
        else:
            return Response({"main": None})


class RecommendedAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, name, usage, *args, **kwargs):
        category = import_category(name).objects.get(name=name)
        print("recommendations get")

        recommendations = category.get_recommendations(usage)
        print(recommendations)
        return Response({"recommendations": recommendations})


class CustomizationAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, name, *args, **kwargs):
        category = import_category(name).objects.get(name=name)
        return Response({
            "settings": category.customization_settings,
            "category": {
                "subHeader": category.sub_header
            }
        })
