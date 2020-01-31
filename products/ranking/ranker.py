from products.models import Category, Product
from collections import defaultdict


class Ranker:
    def __init__(self):
        products = self.get_products()
        value_sorted_products = self.sort_products(products)
        price_sorted_products = self.sort_with_price(value_sorted_products)
        self.save_products(value_sorted_products, price_sorted_products)

    def get_products(self):
        products = Product.objects.none()

        for category in Category.objects.all():
            for meta_category in category.meta_categories.all():
                products |= meta_category.products.all()

        return products

    def sort_products(self, products):
        sorted_products = defaultdict()

        for product in products:
            for spec_value in product.spec_values.all():
                value = spec_value.value
                spec_key = spec_value.spec_key

                if spec_key:
                    spec_group = spec_key.spec_group
                    key = spec_key.key

                    if spec_group and spec_group.rank_group:
                        print(spec_group)
                        print(type(spec_group))
                        value = spec_group.process_value(value)

                        if not sorted_products[key]:
                            sorted_products[key] = [(product.id, value)]

                        else:
                            for i, saved_specs in enumerate(sorted_products[spec_key.key]):
                                saved_id, saved_value = saved_specs[0]
                                value_package = (product.id, value)

                                # Rank with value
                                if spec_group.is_bigger(value, saved_value):
                                    sorted_products[key].insert(i, value_package)
                                    break

                                elif spec_group.is_equal(value, saved_value):
                                    sorted_products[key][i].append(value_package)
                                    break

                                elif i == (len(sorted_products[key]) - 1):
                                    sorted_products[key].append([value_package])
                                    break

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

    def save_products(self, value_sorted_products, price_sorted_products):
        print(value_sorted_products)
        print(price_sorted_products)
