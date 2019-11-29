from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from django.http import HttpResponseBadRequest
from .serializers import WebsiteSerializer
from .models import Website
from products.models import Product, MetaProduct, Price, Spec, SpecGroup
from difflib import SequenceMatcher
import re, json


class WebsitesAPI(generics.GenericAPIView):
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]
    serializer_class = WebsiteSerializer

    def get(self, request, *args, **kwargs):
        website = Website.objects.filter(has_run=False).first()
        if not website:
            Website.objects.all().update(has_run=False)
            website = Website.objects.filter(has_run=False).first()

        website.has_run = True
        website.save()

        return Response({"website": WebsiteSerializer(website).data})


class ProductsAPI(generics.GenericAPIView):
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        website = data.get("website")

        try:
            meta_product = MetaProduct.objects.get(url=website)
        except:
            meta_product = MetaProduct(
                name=data.get("title"),
                url=website,
                host=Website.objects.get(id=data.get("host_id")),
            )

        category = data.get("category")
        if category:
            meta_product.category = category

        meta_product.is_updated = True
        meta_product.save()

        specs = data.get("specs")
        if specs:
            meta_product.set_specs(json.loads(specs))

        manufacturing_name = data.get("manufacturing_name")
        if manufacturing_name:
            meta_product.manufacturing_name = manufacturing_name

        price_obj = Price(meta_product=meta_product)
        price_obj.price = data.get("price")
        price_obj.save()

        return Response({})
