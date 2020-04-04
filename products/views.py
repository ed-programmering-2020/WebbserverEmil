from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import generics

from products.models import Laptop, Website, BaseProduct, MetaProduct, Image
from products.serializers import ProductSerializer

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

    def get(self, request, category, *args, **kwargs):
        settings = request.GET.dict()

        if settings is not None:
            model = import_model(category)
            products = model.match(settings)

            if products:
                serialized_products = [ProductSerializer(product).data for product, __ in products]
                return Response({"products": serialized_products})

        return Response({"products": []})


class LaptopAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get(self, request, laptop_id, slug, *args, **kwargs):
        try:
            laptop = Laptop.objects.get(id=laptop_id)
            return Response(ProductSerializer(laptop).data)
        except Laptop.DoesNotExist:
            return Response({})


class ProductsAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        products = json.loads(request.data.get("products"))
        for product_data in products:
            host = Website.objects.get(name=product_data["host"])
            try:
                meta_product = MetaProduct.objects.get(manufacturing_name=product_data["manufacturing_name"], host=host)
            except MetaProduct.DoesNotExist:
                meta_product = MetaProduct(
                    host=host,
                    name=product_data["name"],
                    url=product_data["url"],
                    manufacturing_name=product_data.get("manufacturing_name", None),
                )

                if meta_product.product is None:
                    model_class = import_model()

                    if meta_product.manufacturing_name is not None:
                        BaseProduct.objects

            if product_data["campaign"] is True:
                meta_product.campaign_price = product_data["price"]
            else:
                meta_product.standard_price = product_data["price"]
                meta_product.campaign_price = None
            meta_product.save()


            for image_url in product_data["image_urls"]:
                ImageUrl.objects.create(url=image_url, host=host, meta_product=meta_product)


            matching_product = product.find_similar_product()

            category_product = BaseCategoryProduct.create(product, matching_product)
            if category_product is None:
                continue

            product.category_product = category_product
            product.save()
            category_product.update()
            category_product.save()

        return Response({})
