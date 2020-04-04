from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics
from products.serializers import CategoryProductSerializer


def import_model(name):
    name = "products.models." + name.capitalize()
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


class MatchAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategoryProductSerializer

    def get(self, request, category, *args, **kwargs):
        settings = request.GET.dict()

        if settings is not None:
            model = import_model(category)
            products = model.match(settings)

            if products:
                serialized_products = []
                for product, __ in products:
                    serialized_products.append(CategoryProductSerializer(product).data)

                return Response({
                    "products": serialized_products,
                })

        return Response({"products": []})
