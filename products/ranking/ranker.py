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

                    if spec_group and spec_group.rank_group:
                        spec_group = spec_group.as_inherited_model()
                        value = spec_group.process_value(value)
                        key = spec_group.name

                        if key not in sorted_products:
                            sorted_products[key] = [[(product.id, value)]]
                        else:
                            for i, saved_specs in enumerate(sorted_products[key]):
                                saved_id, saved_value = saved_specs[0]
                                value_package = (product.id, value)

                                # Rank with value
                                if spec_group.is_bigger(value, saved_value):
                                    sorted_products[key].insert(i, [value_package])
                                    break

                                elif spec_group.is_equal(value, saved_value):
                                    sorted_products[key][i].append(value_package)
                                    break

                                elif i == (len(sorted_products[key]) - 1):
                                    sorted_products[key].append([value_package])
                                    break

        return sorted_products

    def sort_with_price(self, products):
        sorted_products = defaultdict()

        for key, values in products.items():
            for value_list in values:
                for value in value_list:
                    id, price = value
                    id = str(id)
                    sorted_products[id] = sorted_products[id] / (price / 1000)

        return sorted_products

    def save_products(self, value_sorted_products, price_sorted_products):
        print(value_sorted_products)
        print(price_sorted_products)
