from products.models import BaseCategory
from .matchers import LaptopMatcher
from .customizers import LaptopCustomizer
from .values import LaptopValues
import operator


class Laptop(BaseCategory, LaptopMatcher, LaptopCustomizer, LaptopValues):
    def match(self, settings):
        all_products = self.get_all_products()

        products_price_matched = self.find_with_price(all_products, settings["price"], True)
        products_size_matched = self.find_with_size(products_price_matched, settings["size"])

        products_with_values = self.sort_with_values(products_size_matched)
        products_usage_sorted = self.sort_with_usage(products_with_values, len(products_size_matched), settings["usage"])
        products_price_sorted = self.sort_with_price(products_usage_sorted)

        top_products = self.get_top_products(products_price_sorted)
        products_prioritization_sorted = self.sort_with_priorities(products_with_values, len(products_size_matched), top_products, settings["priorities"])
        ranked_products = products_prioritization_sorted.sort(key=operator.itemgetter(1), reverse=True)
        product_models = self.get_product_models(ranked_products)

        return self.products_to_json(product_models)

    def __str__(self):
        return "<Laptop>"
