from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .serializers import WebsiteSerializer
from .models import Website
from products.models import Product, MetaProduct
import re


class WebsitesAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = WebsiteSerializer

    def get(self, request, *args, **kwargs):
        website = Website.objects.filter(has_run=False).first()
        print(website)
        if not website:
            print(1)
            websites = Website.objects.all()
            for site in websites:
                site.has_run = False

            website = Website.objects.filter(has_run=False).first()

        website.has_run = True
        print(website)

        return Response({"website": WebsiteSerializer(website).data})


class ProductsAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        data = request.data
        website = data.get("website")
        name = data.get("title")
        price = re.sub("\D", "", str(data.get("price")))
        image = data.get("image")
        specs = data.get("specs")
        category = data.get("category")

        # Meta product
        try:
            meta_product = MetaProduct.objects.get(url=website)
            meta_product.price = price
        except:
            meta_product = MetaProduct.objects.create(
                name=name,
                price=price,
                url=website,
                specs=specs,
                category=category
            )

        # Parent product
        if meta_product.product is None:
            try:
                other_meta_product = MetaProduct.objects.exclude(url=website).get(name=name)

                product = Product.objects.create()

                meta_product.product = product
                other_meta_product.product = product
            except:
                product = None
        else:
            product = meta_product.product

        if product is not None:
            product.update()

        return Response({})
