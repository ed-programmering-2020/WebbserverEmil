from products.models import Product, SpecGroup, SpecValue, SpecKey
from products.matching.values import LaptopValues
from collections import defaultdict
import operator


class BaseMatcher:
    def find_with_price(self, products, value_range, strict=True):
        low_price, high_price = value_range
        low_price -= 1

        if strict:
            valid_products = products.all()
            for product in products.all():
                price = product.price
                if not price or not low_price <= price <= high_price:
                    valid_products = valid_products.exclude(id=product.id)

            return valid_products

    def sort_with_usage(self, products, amount_of_products, usage):
        sorted_products = defaultdict()

        def get_value(products_list_length, key, product, i_inverse):
            id, __ = product
            id = str(id)

            result = self.biases[usage][key] * ((amount_of_products / products_list_length) * i_inverse)

            if id in sorted_products.keys():
                sorted_products[id] = sorted_products[id] + result
            else:
                sorted_products[id] = result

        for key, products_list in products.items():
            products_list_length = len(products_list)

            for i, product in enumerate(products_list):
                i_inverse = products_list_length - i

                if type(product) == list:
                    for sub_product in product:
                        get_value(products_list_length, key, sub_product, i_inverse)
                else:
                    get_value(products_list_length, key, product, i_inverse)

        return sorted_products

    def sort_with_priorities(self, products_with_values, amount_of_products, top_products, priorities):
        sorted_products = defaultdict()

        def save_value(id, key, product, products_list_length, i):
            product_id, __ = product

            if product_id == id:
                i_inverse = products_list_length - i
                result = ((amount_of_products / products_list_length) * i_inverse)
                sorted_products[id]["values"][key] = result

        for id, value in top_products.items():
            sorted_products[id] = {"usage_value": value, "values": {}}
            for key, products_list in products_with_values.items():
                products_list_length = len(products_list)

                for i, product in enumerate(products_list):
                    if type(product) == list:
                        for sub_product in product:
                            save_value(id, key, sub_product, products_list_length, i)
                    else:
                        save_value(id, key, product, products_list_length, i)

        priority_sorted_products = []
        for id, all_values in sorted_products.items():
            resulting_value = all_values["usage_value"]

            for group, values in self.priority_groups.items():
                key_value = 0

                for key, value in all_values["values"].items():
                    if key in values:
                        key_value += value

                resulting_value += 0.1 * priorities[group] * (key_value / len(values))

            priority_sorted_products.append((id, resulting_value))

        return priority_sorted_products

    def get_top_products(self, products):
        top_id, top_value = None, 0
        for id, value in products.items():
            if value > top_value:
                top_value = value
                top_id = id

        top_products = {
            top_id: top_value
        }
        for id, value in products.items():
            if id != top_id and value >= (top_value * 0.9):
                top_products[id] = value

        return top_products

    def get_product_models(self, products):
        product_list = []
        for product in products:
            id, value = product

            product_list.append(Product.objects.get(id=id))

        return product_list

    def products_to_json(self, products):
        if len(products) >= 1:
            main_product = products[0]

            alternative_products = None
            if len(products) >= 4:
                alternative_products = products[1:4]
            elif len(products) > 1:
                alternative_products = products[1:len(products)]

            return {
                "main": main_product,
                "alternatives": alternative_products
            }
        else:
            return None


class LaptopMatcher(BaseMatcher, LaptopValues):
    def __init__(self):
        super().__init__()

    def find_with_settings(self, all_products, settings):
        print("---")
        products_price_matched = self.find_with_price(all_products, settings["price"], True)
        products_size_matched = self.find_with_size(products_price_matched, settings["size"])
        print("price", products_price_matched)
        print("size", products_size_matched)

        products_usage_sorted = self.sort_with_usage(products_with_values, len(products_size_matched), settings["usage"])
        top_products = self.get_top_products(products_price_sorted)
        products_prioritization_sorted = self.sort_with_priorities(products_with_values, len(products_size_matched), top_products, settings["priorities"])
        ranked_products = products_prioritization_sorted.sort(key=operator.itemgetter(1), reverse=True)
        print("usage", products_usage_sorted)
        print("top", top_products)
        print("priorities", products_prioritization_sorted)
        print("ranked", ranked_products)

        product_models = self.get_product_models(ranked_products)
        print(product_models)

        return self.products_to_json(product_models)

    def find_with_size(self, products, size):
        min_size, max_size = size
        spec_keys = SpecGroup.objects.get(name="screen size").spec_keys.all()

        checked_products = []
        for product in products.all():
            spec_values = product.spec_values.all()

            for key in spec_keys:
                try:
                    screen_size = spec_values.filter(spec_key=key).first()
                    if screen_size:
                        screen_size = screen_size.value.split(" ")[0]

                        if min_size < float(screen_size) < max_size:
                            checked_products.append(product)

                        break
                except SpecValue.DoesNotExist:
                    pass

        return checked_products
