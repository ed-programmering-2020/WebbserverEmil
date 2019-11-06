from rest_framework.response import Response
from rest_framework import generics
from .serializers import WebsiteSerializer
from .models import Website
from products.models import Product, MetaProduct
import re


class WebsitesAPI(generics.GenericAPIView):
    serializer_class = WebsiteSerializer

    def get(self, request, *args, **kwargs):
        website = Website.objects.get(has_run=False)
        if not website:
            websites = Website.objects.all()
            for site in websites:
                site.has_run = False

            website = Website.objects.get(has_run=False)
        
        return Response({"website": WebsiteSerializer(website).data})


class ProductsAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        website = data.get("website")
        name = data.get("title")
        price = re.sub("\D", "", str(data.get("price")))
        image = data.get("image")
        specs = data.get("specs")
        category = data.get("category")

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

        product.update()

        return Response({})
