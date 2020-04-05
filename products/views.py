from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import generics

from products.models import Laptop, Website, MetaProduct, Image, BaseProduct
from products.serializers import ProductSerializer

from django.http.response import HttpResponse
from difflib import SequenceMatcher

import json


def import_model(name):
    mod = __import__("products")
    for component in ["models", name]:
        mod = getattr(mod, component)
    return mod


def products_sitemap():
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    for laptop in Laptop.objects.all():
        sitemap_xml += "<url><loc>https://www.orpose.se/laptop/{}/{}</loc></url>".format(laptop.id, laptop.slug)
    sitemap_xml += "</urlset>"
    return HttpResponse(sitemap_xml, content_type="text/xml")


class MatchAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get(self, request, category, *args, **kwargs):
        settings = request.GET.dict()

        if settings is not None:
            model = import_model(category.capitalize())
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

    def get_or_create_product(self, meta_product, category, specifications):
        model_class = import_model(category)

        if meta_product.manufacturing_name is not None:
            try:
                return model_class.objects.get(manufacturing_name=meta_product.manufacturing_name)
            except model_class.DoesNotExist:
                pass

        for product_instance in model_class.objects.filter(is_active=True):
            name_similarity = SequenceMatcher(None, meta_product.name, product_instance.name).ratio()
            if name_similarity >= 0.5:
                for key, value in specifications.items():
                    specification_model = import_model(key)
                    attribute_name = specification_model.to_attribute_name()
                    existing = specification_model.find_existing(value)
                    if existing is None or eval("product_instance.{}.id is not {}".format(attribute_name, existing.id)):
                        break
                else:
                    meta_product.is_active = False
                    meta_product.save()
                    return product_instance

        return model_class.objects.create(manufacturing_name=meta_product.manufacturing_name)

    def post(self, request, *args, **kwargs):
        products = json.loads(request.data.get("products"))
        for product_data in products:
            host = Website.objects.get(name=product_data["host"])
            meta_product, __ = MetaProduct.objects.get_or_create(
                host=host,
                name=product_data["name"],
                url=product_data["url"],
                manufacturing_name=product_data.get("manufacturing_name", None),
            )
            if "used" in product_data:
                meta_product.used = product_data["used"]
            meta_product.update_price(product_data["price"], product_data.get("campaign", False))
            meta_product.availability = product_data.get("availability", 0)
            meta_product.shipping = product_data.get("shipping", 0)
            meta_product.rating = product_data.get("rating", None)
            meta_product.review_count = product_data.get("review_count", 0)
            meta_product.save()

            if meta_product.product is None:
                product = self.get_or_create_product(
                    meta_product,
                    product_data["category"],
                    product_data["specifications"]
                )
            else:
                product = meta_product.product

            product.update_specifications(product_data["specifications"])
            product.update_price()
            product.update_rating()
            product.save()
            meta_product.product = product
            for image_url in product_data["image_urls"]:
                Image.objects.create(url=image_url, host=host, product=product)
        return Response({})
