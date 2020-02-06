from products.models.products import Product, SpecValue
from products.models.spec_groups import ScreenSize
from products.matching.weights import LaptopWeights
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

    def sort_with_usage(self, products, usage):
        sorted_products = defaultdict()
        for product in products:
            usage_score = 0
            priority_score = 0

            for key, score in product.scores.items():


                priority = None
                for group, priorities in self.priority_groups.items():
                    pass


                usage_score += self.usages[usage][key] * int(score)
                priority_score += self.priorities[]

            sorted_products[product.id] = {"usage": usage_score, "priority": priority_score}

        for id, value in products.items():
            sorted_products[id] = {"usage_value": value, "values": {}}

            for key, products_list in products_with_values.items():
                products_list_length = len(products_list)

                for i, product in enumerate(products_list):
                    product_id, __ = product

                    if product_id == id:
                        i_inverse = products_list_length - i
                        result = ((amount_of_products / products_list_length) * i_inverse)
                        sorted_products[id]["values"][key] = result

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


        return sorted_products

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


class LaptopMatcher(BaseMatcher, LaptopWeights):
    def __init__(self):
        super().__init__()

    def find_with_settings(self, all_products, settings):
        # Filter products
        products_price_matched = self.find_with_price(all_products, settings["price"])
        products_size_matched = self.find_with_size(products_price_matched, settings["size"])
        print("price", products_price_matched)
        print("size", products_size_matched)

        # Sort products
        products_sorted = self.sort_with_usage(products_size_matched, settings["usage"])
        top_products = self.get_top_products(products_sorted)
        ranked_products = top_products.sort(key=operator.itemgetter(1), reverse=True)
        print("ranked", ranked_products)

        # Retrieve & return products
        product_models = self.get_product_models(ranked_products)
        return self.products_to_json(product_models)

    def find_with_size(self, products, size):
        min_size, max_size = size
        spec_keys = ScreenSize.objects.first().spec_keys.all()

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
