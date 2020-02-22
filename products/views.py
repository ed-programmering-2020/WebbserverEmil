from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from products.serializers import ProductSerializer
from products.scraping.product_combiner import Combiner
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from products.models import Product
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

        print("bapp")

        if products:
            # serialized_alternatives = []
            # if products["alternatives"]:
            #     for product in products["alternatives"]:
            #         serialized_alternatives.append(ProductSerializer(product).data)

            print("here")
            return Response({
                "main": ProductSerializer(products[0]).data,
            })
        else:
            return Response({"main": None})


class RecommendedAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, name, usage, *args, **kwargs):
        category = import_category(name).objects.get(name=name)
        return Response({"recommendations": category.get_recommendations(usage)})


class CustomizationAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, name, *args, **kwargs):
        category = import_category(name).objects.get(name=name)
        return Response({
            "settings": category.get_settings(),
            "category": category.get_info()
        })


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


class ProductsAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.data.get("products"))
        files = request.FILES

        Combiner(data, files)
        return Response({})
