from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import generics

from products.models import Product, Website, BaseCategoryProduct

import json


class ProductsAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data_list = json.loads(request.data.get("products"))
        for product_data in data_list:
            host = Website.objects.get(name=product_data.get("website"))
            product = Product.create_or_get(product_data, host)

            matching_product = product.find_similar_product()

            category_product = BaseCategoryProduct.create(product, matching_product)
            if category_product is None:
                continue

            product.category_product = category_product
            product.save()
            category_product.update()
            category_product.save()

        return Response({})
