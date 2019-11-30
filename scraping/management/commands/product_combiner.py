from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from products.models import Product, MetaProduct, Spec, SpecGroup
from difflib import SequenceMatcher
import re


class Command(BaseCommand):
    help = 'Combines updated meta-products into products'

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

    def check_meta_product(self, numbers, meta_product):
        if SequenceMatcher(None, meta_product.name, meta_product.name).ratio() <= 0.7:
            other_numbers = [int(s) for s in meta_product.name.split() if s.isdigit()]
            for number in numbers:
                if number not in other_numbers:
                    return None
        return meta_product

    def find_similar_meta_products(self, meta_product):
        words = meta_product.name.split(" ")
        checked_meta_products, other_meta_products = [], []
        numbers = [int(s) for s in meta_product.name.split() if s.isdigit()]

        for i in range(len(words) - 1):
            combo = words[i] + " " + words[i + 1]
            other_meta_products += MetaProduct.objects.exclude(url=meta_product.url).filter(name__icontains=combo).all()

        for m_product in other_meta_products:
            m_product = self.check_meta_product(numbers, m_product)
            if m_product == True: checked_meta_products.append(m_product)

        return checked_meta_products

    def find_specs(self, specs):
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

    def handle(self, *args, **options):
        count = 0
        updated_meta_products = []
        products = []
        print("Combining meta-products")
        for meta_product in MetaProduct.objects.filter(is_updated=True):
            if meta_product not in updated_meta_products:
                updated_meta_products.append(meta_product)
                other_meta_product = None
                count += 1

                try:
                    other_meta_product = MetaProduct.objects.exclude(url=meta_product.url).get(
                        Q(name=meta_product.name) |
                        Q(manufacturing_name=meta_product.manufacturing_name)
                    )
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
                    other_meta_product.is_updated = False
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

                meta_product.is_updated = False
                meta_product.save()

                if product != None:
                    products.append(product)

                print("-- %s updated (%s)" % (meta_product, count))

        print("Updating products")
        count = 0
        for product in products:
            count += 1
            product.update_info()
            product.save()

            print("-- %s updated (%s)" % (product, count))

        self.stdout.write(self.style.SUCCESS("Successfully combined meta-products and updated the products"))