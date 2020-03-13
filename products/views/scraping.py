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
        files_list = request.FILES

        for product_data in data_list:
            host = Website.objects.get(name=product_data.get("website"))
            product = Product.create_or_get(product_data, host, files_list)

            # Find matching product
            matching_product = product.find_similar_product()

            # Create or combine into a category product
            category_product = BaseCategoryProduct.create(product, matching_product)  # May be none
            if category_product is None:
                continue

            # Assign product to category product
            product.category_product = category_product
            product.save()

            # Update category product with its given product
            category_product.update()

        return Response({})
