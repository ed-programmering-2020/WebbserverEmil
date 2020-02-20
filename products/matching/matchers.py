"""Matcher classes for category models

This module contains the matcher classes which contain all of the
methods required for matching products for the different category models.

"""

from products.models.products import Product, SpecValue
from products.models.spec_groups import ScreenSize
from products.matching.weights import LaptopWeights
from operator import itemgetter


class BaseMatcher:
    """Base class for the different category matching classes"""

    def find_with_price(self, products, price_range, strict=True):
        """Filters out products which is not in the price range"""

        low_price, high_price = price_range
        low_price -= 1

        if strict:
            valid_products = products.all()
            for product in products.all():
                price = product.price
                if not price or not low_price <= price <= high_price:
                    valid_products = valid_products.exclude(id=product.id)

            return valid_products

    def get_priority_group(self, key_priority):
        """Gets the group which a priority belongs to"""

        for group, priorities in self.priority_groups.items():
            for priority in priorities:
                if key_priority == priority:
                    return group
        return None

    def sort_with_bias(self, products, usage, priorities):
        """Sorts the products based on usage and priority bias"""

        sorted_products = []
        for product in products:
            usage_score, priority_score = 0, 0

            for key, score in product.scores.items():
                score = int(score)
                priority_group = self.get_priority_group(key)

                usage_score += self.usages[usage][key] * score
                priority_score += priorities[priority_group] * score

            sorted_products.append({"id": product.id, "usage": usage_score, "priority": priority_score})

        products_usage_sorted = sorted(sorted_products, key=itemgetter("usage"), reverse=True)
        top_products = products_usage_sorted[:10]
        products_priority_sorted = sorted(top_products, key=itemgetter("priority"), reverse=True)

        return products_priority_sorted

    def get_product_models(self, products):
        """Gets the models of products with id contained in the products parameter"""

        product_list = []
        for product in products:
            product_id = product["id"]
            product_instance = Product.objects.get(id=product_id)
            product_list.append(product_instance)

        return product_list


class LaptopMatcher(BaseMatcher, LaptopWeights):
    """Matcher class for the laptop model"""

    def match(self, all_products, settings):
        """Matches the user with products based on their preferences/settings"""

        price_matched = self.find_with_price(all_products, settings["price"])
        size_matched = self.find_with_size(price_matched, settings["size"])
        bias_sorted = self.sort_with_bias(size_matched, settings["usage"], settings["priorities"])
        models = self.get_product_models(bias_sorted)

        return models

    def find_with_size(self, products, size):
        """Filters out the products which are not inside the size range"""

        min_size, max_size = size
        screen_size_group = ScreenSize.objects.first()
        spec_keys = screen_size_group.spec_keys.all()

        checked_products = []
        for product in products.all():
            spec_values = product.spec_values.all()

            for key in spec_keys:
                try:
                    screen_size = spec_values.filter(spec_key=key).first()
                    if screen_size:
                        screen_size = screen_size_group.process_value(screen_size.value)
                        print(screen_size)

                        if min_size < screen_size < max_size:
                            checked_products.append(product)
                            print(product)

                        break
                except SpecValue.DoesNotExist:
                    pass

        return checked_products
