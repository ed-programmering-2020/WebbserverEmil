from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from products.serializers import ProductSerializer
from rest_framework import generics
import json


def import_model(name):
    name = "products.models." + name.capitalize()
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


class MatchAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get(self, request, name, *args, **kwargs):
        settings_json = request.GET

        print(settings_json)
        if settings_json is not None:
            settings = json.loads(settings_json)
            print(settings)
            model = import_model(name)
            print(model)
            products = model.match(settings)
            print(products)

            if products:
                print("here")
                serialized_products = []
                for product in products:
                    serialized_products.append(ProductSerializer(product).data)

                return Response({
                    "products": serialized_products,
                })

        return Response({"products": []})
