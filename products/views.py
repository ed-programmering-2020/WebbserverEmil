from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import generics, status
from products.models import Laptop, Website, MetaProduct, Image
from products.serializers import ProductSerializer
from django.db import connection
import json


def import_model(name):
    mod = __import__("products")
    for component in ["models", name]:
        mod = getattr(mod, component)
    return mod


class LaptopAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get(self, request):  # READ
        laptop_id = request.GET["id"]
        with connection.cursor() as cursor:
            cursor.execute("SELECT * from products_laptop WHERE id = %s", [laptop_id])
            laptop = cursor.fetchone()
            if laptop is not None:
                return Response(laptop)
            else:
                return Response({"FAIL": "laptop not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):  # UPDATE
        title = request.GET["title"]
        laptop_id = request.GET["id"]
        with connection.cursor() as cursor:
            cursor.execute("UPDATE products_laptop SET title = %s WHERE id = %s", [laptop_id, title])
            return Response({"SUCCESS": "updated a existing laptop"})

    def put(self, request):  # CREATE
        title = request.GET["title"]
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO products_laptop (title, is_active) VALUES (%s, false)", [title])
            return Response({"SUCCESS": "created a new laptop"})

    def delete(self, request):  # DELETE
        laptop_id = request.GET["id"]
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM products_laptop WHERE id = %s", [laptop_id])
            return Response({"SUCCESS": "deleted a existing laptop"})


class ScrapingAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        products = json.loads(request.data.get("products"))
        for product_data in products:
            host = Website.objects.get(name=product_data["host"])
            meta_product, __ = MetaProduct.objects.get_or_create(url=product_data["url"], host=host)
            meta_product.update(product_data, exclude=["url", "host"])
            meta_product.save()

            # Get parent product
            model_class = import_model(product_data["category"])
            if meta_product.product is None:
                product = model_class.objects.filter(model_number=meta_product.model_number).first()
                if product is None:
                    product = model_class.objects.create(
                        name=meta_product.name,  # Temporary name
                        manufacturing_name=meta_product.manufacturing_name
                    )

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
