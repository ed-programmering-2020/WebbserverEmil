from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import generics

from products.models import Laptop, Website, MetaProduct, Image, BaseProduct
from products.serializers import ProductSerializer

from difflib import SequenceMatcher

import json


def import_model(name):
    mod = __import__("products")
    for component in ["models", name]:
        mod = getattr(mod, component)
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


class SearchAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get(self, request, query, *args, **kwargs):
        products = BaseProduct.objects.filter(name__icontains=query)[:8]
        return Response(ProductSerializer(products, many=True).data)


class ScrapingAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        products = json.loads(request.data.get("products"))
        for product_data in products:
            host = Website.objects.get(name=product_data["host"])
            meta_product = MetaProduct.objects.get_or_create(
                host=host,
                name=product_data["name"],
                url=product_data["url"],
                shipping=product_data["shipping"],
                manufacturing_name=product_data.get("manufacturing_name", None),
            )
            if product_data["campaign"] is True:
                meta_product.campaign_price = product_data["price"]
            else:
                meta_product.standard_price = product_data["price"]
                meta_product.campaign_price = None
            meta_product.availability = product_data["availability"]
            meta_product.save()

            if meta_product.product is None:
                model_class = import_model(product_data["category"])
                product = None

                if meta_product.manufacturing_name is not None:
                    product = model_class.objects.filter(manufacturing_name=meta_product.manufacturing_name).first()

                if product is None:
                    for product_instance in model_class.objects.all():
                        name_similarity = SequenceMatcher(None, meta_product.name, product_instance.name).ratio()
                        if name_similarity < 0.5:
                            continue

                        for key, value in product_data["specifications"].items():
                            specification_model = import_model(key)
                            attribute_name = specification_model.to_attribute_name()
                            existing = specification_model.find_existing(value)
                            if existing is None or eval("self.{}.id is not {}".format(attribute_name, existing.id)):
                                break
                        else:
                            continue

                        meta_product.is_active = False
                        product = product
                        break

                if product is None:
                    product = model_class.objects.create(manufacturing_name=meta_product.manufacturing_name)

            else:
                product = meta_product.product

            product.update_specifications(product_data["specifications"])
            product.update_price()
            product.save()
            meta_product.product = product
            for image_url in product_data["image_urls"]:
                Image.objects.create(url=image_url, host=host, product=product)
        return Response({})
