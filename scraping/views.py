from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from django.http import HttpResponseBadRequest
from .serializers import WebsiteSerializer
from .models import Website
from products.models import Product, MetaProduct, Price, Spec, SpecGroup
from difflib import SequenceMatcher
import re, json


class WebsitesAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = WebsiteSerializer

    def get(self, request, *args, **kwargs):
        website = Website.objects.filter(has_run=False).first()
        print(website)
        if not website:
            print(1)
            Website.objects.all().update(has_run=False)
            website = Website.objects.filter(has_run=False).first()

        website.has_run = True
        website.save()
        print(website)

        return Response({"website": WebsiteSerializer(website).data})


class ProductsAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        def match_specs(possible_specs, other_meta_product):
            for other_key, other_value in other_meta_product.specs.items():
                for value, keys in possible_specs.items():
                    if other_key in keys:
                        if other_value == value:
                            break
                        else:
                            return False
            return True

        def check_meta_product(numbers, meta_product):
            if SequenceMatcher(None, m_product.name, meta_product.name).ratio() <= 0.7:
                other_numbers = [int(s) for s in m_product.name.split() if s.isdigit()]
                for number in numbers:
                    if number not in other_numbers:
                        return None
            return meta_product

        data = request.data

        price = data.get("price")
        website = data.get("website")
        name = data.get("title")
        image = data.get("image")
        specs = data.get("specs")
        category = data.get("category")
        host_id = data.get("host_id")

        try:
            meta_product = MetaProduct.objects.get(url=website)
        except:
            meta_product = MetaProduct(name=name, url=website, host=Website.objects.get(id=host_id))

        print(specs)
        meta_product.set_specs(specs)
        meta_product.category = category
        meta_product.save()

        price_obj = Price(meta_product=meta_product)
        price_obj.price = price
        price_obj.save()

        if meta_product.product is None:
            print("finding other meta products")
            try:
                other_meta_products = []
                words = meta_product.name.split(" ")
                for i in range(len(words) - 1):
                    combo = words[i] + " " + words[i + 1]
                    other_meta_products.append(MetaProduct.objects.exclude(url=website).filter(name__icontains=combo).all())

                numbers = [int(s) for s in meta_product.name.split() if s.isdigit()]
                checked_meta_products = []
                for m_product in other_meta_products:
                    m_product = check_meta_product(numbers, m_product)
                    if m_product != None: checked_meta_products.append(m_product)

                possible_specs = {}
                for key, value in meta_product.specs.items():
                    try:
                        spec = Spec.objects.get(key=key)
                        spec_group = spec.spec_group

                        if spec_group:
                            possible_keys = [spec.key for spec in spec_group.specs]
                        else:
                            possible_keys = [key]
                    except:
                        possible_keys = [key]

                    possible_specs[value] = possible_keys

                other_meta_product = None
                for other in checked_meta_products:
                    result = match_specs(possible_specs, other)
                    if result == True: other_meta_product = other
            except:
                other_meta_product = None

            print(other_meta_product)

            if other_meta_product != None:
                product = Product.objects.create()
                print(product)
                meta_product.product = product
                meta_product.save()
                print(1)
                other_meta_product.product = product
                other_meta_product.save()
                print(2)
            else:
                product = None
        else:
            product = meta_product.product

        if product != None:
            print(3)
            product.update_info()
            print(4)

            product.save()

        return Response({})
