from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import WebsiteSerializer
from .models import Website
from django.db.models import Q
from products.models import Product, MetaProduct, Price
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

    def match_specs(self, possible_specs, other_meta_product):
        def check(other_spec):
            other_key = other_spec.key
            other_value = other_spec.value

            if "artikelnr" not in other_key:
                for value, keys in possible_specs.items():
                    if other_key in keys:
                        if bool(re.search(r'\d', value)):
                            test_other_value = re.sub(r'\D', "", other_value)
                            test_value = re.sub(r'\D', "", other_value)

                            if test_other_value == test_value:
                                break
                            else:
                                return False
                        else:
                            if SequenceMatcher(None, other_value, value).ratio() >= 0.9:
                                return True
                            else:
                                test_other_values = other_value.strip(" ")
                                for test_other_value in test_other_values:
                                    if test_other_value in value:
                                        return True

        for other_spec in other_meta_product.specs.all():
            result = check(other_spec)
            if result == False:
                return False
        return True

    def find_similar_meta_products(self, meta_product):
        words = meta_product.name.split(" ")
        other_meta_products = []
        # numbers = [int(s) for s in meta_product.name.split() if s.isdigit()]

        for i in range(len(words) - 1):
            combo = words[i] + " " + words[i + 1]
            other_meta_products += MetaProduct.objects.exclude(url=meta_product.url).filter(name__icontains=combo).all()

        return other_meta_products

    def find_specs(self, specs):
        possible_specs = {}
        for spec in specs:
            key = spec.key
            value = spec.value

            spec_group = spec.spec_group
            if spec_group and spec_group.is_active:
                possible_keys = [spec.key for spec in spec_group.specs.all()]
            else:
                possible_keys = [key]

            for i in range(len(possible_keys)):
                if len(possible_keys[i]) > 32:
                    possible_keys.pop(i)

            possible_specs[value] = possible_keys

        return possible_specs

    def post(self, request, *args, **kwargs):
        data_list = json.loads(request.data.get("products"))
        files = request.FILES

        count = 0
        updated_meta_products = []

        print(request.data)
        print(data_list)

        for data in data_list:
            website = data.get("website")
            image = files.get(data["filename"]) if "filename" in data else None

            try:
                meta_product = MetaProduct.objects.get(url=website)
            except:
                meta_product = MetaProduct(
                    name=data.get("title"),
                    url=website,
                    host=Website.objects.get(id=data.get("host_id")),
                    image=image
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

            if meta_product not in updated_meta_products:
                updated_meta_products.append(meta_product)
                other_meta_product = None
                count += 1

                try:
                    other_meta_products = MetaProduct.objects.exclude(url=meta_product.url)
                    if meta_product.manufacturing_name != None:
                        other_meta_product = other_meta_products.get(
                            Q(name=meta_product.name) |
                            Q(_manufacturing_name=meta_product.manufacturing_name)
                        )
                    else:
                        other_meta_product = other_meta_products.get(name=meta_product.name)
                except:
                    other_meta_products = self.find_similar_meta_products(meta_product)
                    possible_specs = self.find_specs(meta_product.specs.all())
                    checked_meta_products = []
                    for other in other_meta_products:

                        if other not in checked_meta_products:
                            result = self.match_specs(possible_specs, other)

                            if result == True:
                                other_meta_product = other
                                break

                            checked_meta_products.append(other)

                if other_meta_product != None:
                    updated_meta_products.append(other_meta_product)

                    if other_meta_product.product == None:
                        product = Product.objects.create()
                        meta_product.product = product
                        meta_product.save()
                        other_meta_product.product = product
                        other_meta_product.save()
                    else:
                        product = other_meta_product.product
                        meta_product.product = product
                        meta_product.save()

                elif meta_product.product:
                    product = meta_product.product

                else:
                    product = None

                meta_product.save()

                if product != None:
                    product.update_info()
                    product.save()

                print(" -- %s (%s)" % (meta_product, count))

        return Response({})
