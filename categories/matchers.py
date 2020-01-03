"""from products.models import Product, SpecGroupCollection"""
from collections import defaultdict
import re


class BaseMatcher:
    def find_with_price(self, products, value_range, strict=True):
        low_price, high_price = value_range
        low_price -= 1

        if strict:
            try:
                return products.filter(get_price__lte=low_price, get_price__gte=high_price)
            except:  # TODO fix this danger
                return None

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

    def sort_with_values(self, products):
        sorted_products = defaultdict()
        """
        for product in products:
            specs = product.specs.all()
            id = product.id

            for key, value in self.values.items():
                sgc = SpecGroupCollection.objects.get(name=key)

                spec_value = None
                for spec in specs:
                    if spec.spec_group and spec.spec_group.spec_group_collection and spec.spec_group.spec_group_collection == sgc:
                        spec_value = spec.value
                        break

                if not sorted_products[key]:
                    sorted_products[key] = [(id, spec_value)]
                else:
                    for saved_index, saved_value in enumerate(sorted_products[key]):
                        if type(saved_value) == list:
                            saved_value = saved_value[0]

                        saved_id, saved_spec_value = saved_value
                        value_package = (id, spec_value)

                        if value != []:
                            saved_spec_value = self.check_text_value(saved_spec_value, value)
                            spec_value = self.check_text_value(spec_value, value)
                        else:
                            saved_spec_value = re.sub(r'[^\d.]+', '', saved_spec_value)
                            spec_value = re.sub(r'[^\d.]+', '', spec_value)

                        if spec_value > saved_spec_value:
                            sorted_products[key].insert(saved_index, value_package)
                            break
                        elif spec_value == saved_spec_value:
                            if type(sorted_products[key][saved_index]) == list:
                                sorted_products[key][saved_index].append(value_package)
                            else:
                                sorted_products[key][saved_index] = [sorted_products[key][saved_index], value_package]
                            break
                        elif saved_index == (len(sorted_products[key]) - 1):
                            sorted_products[key].append([value_package])
                            break
"""
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
        """
        for product in products:
            id, value = product

            product_list.append(Product.objects.get(id=id))
        """


        return product_list

    def match(self, settings):
        raise NotImplementedError

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


class LaptopMatcher:
    def find_with_size(self, products, size):
        min_size, max_size = size

        try:
            pass
            """spec_groups = SpecGroupCollection.objects.get(name="screen size").spec_groups.all()
            spec_keys = [spec_group.key for spec_group in spec_groups]"""
        except:
            return None

        checked_products = []
        """
        for product in products:
            for key in spec_keys:
                try:
                    screen_size = product.specs.get(key=key)
                    if min_size < screen_size.value < max_size:
                        checked_products.append(product)
                    break
                except:
                    
        """

        return checked_products

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
