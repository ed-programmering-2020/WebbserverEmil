from products.models import Category, Product
from collections import defaultdict


class Ranker:
    def __init__(self):
        products = self.get_products()
        sorted_products = self.sort_products(products)
        self.save_products(sorted_products)

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
                                if spec_group.is_greater(value, saved_value):
                                    sorted_products[key].insert(i, [value_package])
                                    break

                                elif spec_group.is_equal(value, saved_value):
                                    sorted_products[key][i].append(value_package)
                                    break

                                elif i == (len(sorted_products[key]) - 1):
                                    sorted_products[key].append([value_package])
                                    break

        return sorted_products

    def save_products(self, products):
        sorted_products = defaultdict()
        for key, values in products.items():
            values_length = len(values)

            for pos, value_list in enumerate(values):
                for id, value in value_list:
                    id = str(id)
                    value = pos / values_length

                    if id not in sorted_products:
                        sorted_products[id] = {key: value}
                    else:
                        sorted_products[id][key] = value

        key_count = len(products)
        for id, values in sorted_products.items():
            product = Product.objects.get(id=id)
            price = product.price

            if price:
                scores = defaultdict()
                average_score = 0
                for key, value in values.items():
                    score = value / price
                    scores[key] = score
                    average_score += score / key_count

                product.scores = scores
                product.average_score = average_score
                product.save()
