from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import generics

from products.models import Laptop, Website, MetaProduct, Image, BaseProduct
from products.serializers import ProductSerializer

from django.http.response import HttpResponse

import json


def import_model(name):
    mod = __import__("products")
    for component in ["models", name]:
        mod = getattr(mod, component)
    return mod


def products_sitemap(request):
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    for laptop in Laptop.objects.all():
        if laptop.is_active is True:
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
    queryset = BaseProduct.objects.all()

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
            meta_product, __ = MetaProduct.objects.get_or_create(url=product_data["url"])
            meta_product.host = host
            meta_product.update(product_data, exclude=["url", "host"])
            meta_product.save()

            # Get parent product
            model_class = import_model(product_data["category"])
            if meta_product.product is None:
                product, __ = model_class.objects.get_or_create(manufacturing_name=meta_product.manufacturing_name)
                meta_product.product = product
                meta_product.save()
            else:
                product = meta_product.product

            # Update parent product
            product.update(product_data, exclude=["name", "rating", "processor", "graphics_card"])
            product.save()

            # Add images to parent product
            for image_url in product_data["image_urls"]:
                Image.objects.get_or_create(url=image_url, host=host, product=product)

        return Response({})
