from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.response import Response
from products.serializers import CategoryProductSerializer
from products.models import BaseCategoryProduct


class ProductAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategoryProductSerializer

    def get(self, request, product_id, *args, **kwargs):
        try:
            category_product = BaseCategoryProduct.objects.get(id=product_id)
            model = category_product.get_model()
            inherited_category_product = model.objects.get(id=product_id)
            return Response(CategoryProductSerializer(inherited_category_product).data)
        except BaseCategoryProduct.DoesNotExist:
            return Response({})
