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
        if not website:
            Website.objects.all().update(has_run=False)
            website = Website.objects.filter(has_run=False).first()

        website.has_run = True
        website.save()

        return Response({"website": WebsiteSerializer(website).data})


class ProductsAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        def match_specs(possible_specs, other_meta_product):
            for spec in other_meta_product.specs:
                other_key = spec.key
                other_value = spec.value

                if "artikelnr" not in other_key:
                    other_key = other_key.rstrip()
                    for value, keys in possible_specs.items():
                        if other_key in keys:
                            other_value = other_value.rstrip()
                            value = value.rstrip()

                            if bool(re.search(r'\d', value)):
                                test_other_value = re.sub(r'\D', "", other_value)
                                test_value = re.sub(r'\D', "", other_value)

                                if test_other_value == test_value:
                                    break
                                else:
                                    return False
                            else:
                                test_other_values = other_value.strip(" ")
                                match = False

                                if SequenceMatcher(None, other_value, value).ratio() >= 0.9:
                                    match = True
                                else:
                                    for test_other_value in test_other_values:
                                        if test_other_value in value:
                                            match = True
                                            break

                                return match
            return True

        def check_meta_product(numbers, meta_product):
            if SequenceMatcher(None, meta_product.name, meta_product.name).ratio() <= 0.7:
                other_numbers = [int(s) for s in meta_product.name.split() if s.isdigit()]
                for number in numbers:
                    if number not in other_numbers:
                        return None
            return meta_product

        def find_similar_meta_products(meta_product):
            words = meta_product.name.split(" ")
            checked_meta_products, other_meta_products = [], []
            numbers = [int(s) for s in meta_product.name.split() if s.isdigit()]

            for i in range(len(words) - 1):
                combo = words[i] + " " + words[i + 1]
                other_meta_products += MetaProduct.objects.exclude(url=website).filter(name__icontains=combo).all()

            for m_product in other_meta_products:
                m_product = check_meta_product(numbers, m_product)
                if m_product == True: checked_meta_products.append(m_product)

            return checked_meta_products

        def find_specs(specs):
            possible_specs = {}
            for spec in specs:
                key = spec.key
                value = spec.value

                try:
                    spec = Spec.objects.get(key__iexact=key)
                    spec_group = spec.spec_group

                    if spec_group and spec_group.is_active:
                        possible_keys = [spec.key for spec in spec_group.specs]
                    else:
                        possible_keys = [key]
                except:
                    possible_keys = [key]

                for i in range(len(possible_keys)):
                    if len(possible_keys[i]) > 32:
                        possible_keys.pop(i)

                possible_specs[value] = possible_keys

            return possible_specs

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

        if category: meta_product.category = category
        meta_product.save()
        if specs: meta_product.set_specs(json.loads(specs))

        price_obj = Price(meta_product=meta_product)
        price_obj.price = price
        price_obj.save()

        if meta_product.product is None:
            try:
                other_meta_products = [MetaProduct.objects.exclude(url=website).get(name=name)]
            except:
                other_meta_products = find_similar_meta_products(meta_product)

            possible_specs = find_specs(meta_product.specs.all())
            other_meta_product = None
            for other in other_meta_products:
                result = match_specs(possible_specs, other)
                if result == True:
                    other_meta_product = other

            if other_meta_product != None:
                product = Product.objects.create()
                meta_product.product = product
                meta_product.save()
                other_meta_product.product = product
                other_meta_product.save()
            else:
                product = None
        else:
            product = meta_product.product

        if product != None:
            product.update_info()
            product.save()

        return Response({})
