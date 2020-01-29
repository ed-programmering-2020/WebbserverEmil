from products.models import Category, Product, SpecKey
from collections import defaultdict
import re


class Ranker:
    def __init__(self):
        self.products = self.get_products()
        self.sort_products()

    def get_products(self):
        products = Product.objects.none()

        for category in Category.objects.all():
            for meta_category in category.meta_categories.all():
                products |= meta_category.products

        return products

    def check_text_value(self, spec_value, value_list):
        val = None
        for sub_value in value_list:
            if sub_value in spec_value:
                val = sub_value
                break

        if val < 0:
            val = 1

        if val:
            return value_list.index(val)
        else:
            return None

    def get_spec_group_value(self, name):
        spec_group_values = None
        for spec_group_name, values in self.values.items():
            if spec_group_name == name:
                spec_group_values = values
                break
        return spec_group_values

    def sort_products(self):
        sorted_products = defaultdict()

        for product in self.products:
            for spec_value in product.spec_values.all():
                value = spec_value.value

                try:
                    spec_key = spec_value.spec_key
                    spec_group = spec_key.spec_group
                    key = spec_key.key

                    if spec_group:
                        self.get_spec_group_value(spec_group.name)
                        if spec_group_values:
                            if not sorted_products[key]:
                                sorted_products[key] = [(product.id, value)]

                            else:
                                for i, saved_specs in enumerate(sorted_products[spec_key.key]):
                                    saved_id, saved_value = saved_specs[0]
                                    value_package = (product.id, value)

                                    # Get value
                                    if value != []:
                                        saved_value = self.check_text_value(saved_value, spec_group_values)
                                        value = self.check_text_value(value, spec_group_values)
                                    else:
                                        saved_value = re.sub(r'[^\d.]+', '', saved_value)
                                        value = re.sub(r'[^\d.]+', '', value)

                                    # Rank with value
                                    if value > saved_value:
                                        sorted_products[key].insert(i, value_package)
                                        break
                                    elif value == saved_value:
                                        if type(sorted_products[key][i]) == list:
                                            sorted_products[key][i].append(value_package)
                                        else:
                                            sorted_products[key][i] = [sorted_products[key][i], value_package]
                                        break
                                    elif i == (len(sorted_products[key]) - 1):
                                        sorted_products[key].append([value_package])
                                        break
                except SpecKey.DoesNotExist:
                    pass

        return sorted_products

    def sort_with_price(self, products):
        sorted_products = {}

        def divide_by_price(values):
            id, price = values
            id = str(id)
            sorted_products[id] = sorted_products[id] / (price / 1000)

        for values in products:
            if type(values) == list:
                for sub_values in values:
                    divide_by_price(sub_values)
            else:
                divide_by_price(values)

        return sorted_products

    def save_scores(self):
        pass