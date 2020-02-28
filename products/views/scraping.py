from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import generics
from products.models import Product, Website, BaseCategoryProduct, BaseSpecification, AlternativeCategoryName
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

            # Get matching meta-product/product
            matching_product = product.find_similar_product()
            if matching_product:
                category_product = BaseCategoryProduct.create_or_combine(product, matching_product)

            else:
                matching_category_product = BaseCategoryProduct.find_matching_category_product(product)

                if matching_category_product:
                    product.category_product = matching_category_product

                category_product = product.category_product

            # Update product
            if category_product:
                category_product.update()

        return Response({})
