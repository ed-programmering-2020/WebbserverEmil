from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.response import Response
from products.serializers import CategoryProductSerializer
from products.models import Laptop


class ProductAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategoryProductSerializer

    def get(self, request, category, slug, *args, **kwargs):
        try:
            category_product = Laptop.objects.get(slug=slug)
            model = category_product.content_type.model_class()
            inherited_category_product = model.objects.get(slug=slug)
            return Response(CategoryProductSerializer(inherited_category_product).data)

        except Laptop.DoesNotExist:
            return Response({})
