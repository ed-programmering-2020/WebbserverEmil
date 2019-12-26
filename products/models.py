from django.utils.safestring import mark_safe
from scraping.models import Website
from difflib import SequenceMatcher
from collections import defaultdict
from django.db import models
from enum import Enum
from products import specs
from .customizers import LaptopCustomizer
import json, re, uuid, operator


def get_file_path(instance, filename):
    return "%s.%s" % (uuid.uuid4(), "jpg")


class Category(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    values = {}  # to be overridden

    def find_with_price(self, products, value_range, strict=True):
        low_price, high_price = value_range
        low_price -= 1

        if strict:
            try:
                return products.filter(get_price__lte=low_price, get__gte=high_price)
            except:
                return None

    def sort_with_values(self, products):
        def check_text_value(spec_value, value_list):
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

        sorted_products = defaultdict()
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
                            saved_spec_value = check_text_value(saved_spec_value, value)
                            spec_value = check_text_value(spec_value, value)
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
        for product in products:
            id, value = product

            product_list.append(Product.objects.get(id=id))

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

    def __str__(self):
        return "<Category %s>" % self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Laptop(Category, LaptopCustomizer):
    values = {
        "battery capacity": [],
        "processor": specs.processors,
        "graphics card": specs.graphics_cards,
        "memory": [],
        "disk type": specs.disk_types,
        "storage size": [],
        "resolution": [],
        "panel type": specs.panel_types,
        "refresh rate": []
    }

    biases = {
        Usages.General: {
            "battery capacity": 1,
            "processor": 1,
            "graphics card": 1,
            "memory": 1,
            "disk type": 1,
            "storage size": 1,
            "resolution": 1,
            "panel type": 1,
            "refresh rate": 1
        }, Usages.Gaming: {
            "battery capacity": 1,
            "processor": 1,
            "graphics card": 1,
            "memory": 1,
            "disk type": 1,
            "storage size": 1,
            "resolution": 1,
            "panel type": 1,
            "refresh rate": 1
        }
    }

    priority_groups = {
        "battery": [
            "battery capacity"
        ], "performance": [
            "processor",
            "graphics card",
            "memory",
            "disk type"
        ], "storage": [
            "storage size"
        ], "screen": [
            "resolution",
            "panel type",
            "refresh rate"
        ]
    }

    @staticmethod
    def get_recommendations(usage):
        print(usage)
        if usage == "general":
            return {
                "price": [3000, 11000],
                "size": [13.3, 15.6]
            }
        elif usage == "gaming":
            return {
                "price": [6000, 14000],
                "size": [14, 17.3]
            }
        else:
            return None

    def find_with_size(self, products, size):
        min_size, max_size = size

        try:
            spec_groups = SpecGroupCollection.objects.get(name="screen size").spec_groups.all()
            spec_keys = [spec_group.key for spec_group in spec_groups]
        except:
            return None

        checked_products = []
        for product in products:
            for key in spec_keys:
                try:
                    screen_size = product.specs.get(key=key)
                    if min_size < screen_size.value < max_size:
                        checked_products.append(product)
                    break
                except:
                    pass

        return checked_products

    def sort_with_usage(self, products, amount_of_products, usage):
        sorted_products = defaultdict()
        def get_value(products_list_length, key, product, i_inverse):
            id, value = product
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
            product_id, value = product
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

    def match(self, settings):
        all_products = []
        for meta_category in self.meta_categories.all():
            all_products.extend(meta_category.products.all())

        products_price_matched = self.find_with_price(all_products, settings["price"]["range"], True)
        if products_price_matched:
            products_size_matched = self.find_with_size(products_price_matched, settings["size"]["values"])

            if products_price_matched is None:
                return None
        else:
            return None

        products_with_values = self.sort_with_values(products_size_matched)

        products_usage_sorted = self.sort_with_usage(products_with_values, len(products_size_matched), settings["usage"]["value"])
        products_price_sorted = self.sort_with_price(products_usage_sorted)

        top_products = self.get_top_products(products_price_sorted)
        products_prioritization_sorted = self.sort_with_priorities(products_with_values, len(products_size_matched), top_products, settings["priorities"])

        ranked_products = products_prioritization_sorted.sort(key=operator.itemgetter(1), reverse=True)
        product_models = self.get_product_models(ranked_products)

        return self.products_to_json(product_models)


class Manufacturer(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)

    def __str__(self):
        return "<Manufacturer %s>" % self.name


class MetaCategory(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)
    category = models.ForeignKey(Category, related_name="meta_categories", on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<MetaCategory %s>" % self.name

    class Meta:
        verbose_name_plural = 'Meta categories'


class Product(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True, null=True)
    _specs = models.CharField("specs", max_length=256, default=json.dumps({}))
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    meta_category = models.ForeignKey(MetaCategory, related_name="products", on_delete=models.CASCADE, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, related_name="products", on_delete=models.CASCADE, blank=True, null=True)
    manufacturing_name = models.CharField('manufacturing_name', max_length=128, blank=True, null=True)

    @property
    def specs(self):
        return json.loads(self._specs)

    @specs.setter
    def specs(self, specs):
        if self.specs:
            self._specs = json.dumps(self.specs.update(specs))

    def update_specs(self, specs_list):
        specs_set_list = []
        for specs in specs_list:
            specs_set = {}

            for spec in specs:
                specs_set[spec.key] = spec.value

            specs_set_list.append(specs_set)

        combined_specs = {}
        for specs in specs_set_list:
            if specs: combined_specs.update(specs)

        self.specs = combined_specs

    def update_name(self, names):
        words = {}
        for name in names:
            split_words = name.split(" ")

            for other_name in names:
                if other_name != name:
                    other_split_words = other_name.split(" ")

                    for pos, word in enumerate(other_split_words):
                        for split_word in split_words:
                            if SequenceMatcher(None, split_word, word).ratio() >= 0.9 and pos >= 0:
                                if word in words: words[word].append(pos)
                                else: words[word] = [pos]

        words_copy = words.copy()
        removed_words = []
        for word in words_copy:
            if word not in removed_words:
                for other_word in words_copy:
                    if word != other_word:
                        if SequenceMatcher(None, other_word, word).ratio() >= 0.9:
                            length = len(words[word])
                            other_length = len(words[other_word])

                            if length >= other_length:
                                words.pop(other_word, None)
                                removed_words.append(other_word)
                            else:
                                words.pop(word, None)
                                removed_words.append(word)

        calc_words = {}
        for word, pos_list in words.items(): calc_words[word] = sum(pos_list) / len(pos_list)

        sorted_words = sorted(calc_words.items(), key=lambda kv: kv[1])
        name = ""
        for word, pos in sorted_words:
            if len(name) > 0:
                name += " " + word
            else:
                name = word

        if name == "" and names != []:
            name = names[0]

        self.name = name

    def update_info(self):
        def most_frequent(List):
            return max(set(List), key=List.count) if List != [] else None

        categories, names, prices, manufacturing_names, specs_list, important_words = [], [], [], [], [], []
        for meta_product in self.meta_products.all():
            names.append(meta_product.name)
            specs_list.append(meta_product.specs.all())
            manufacturing_names.append(meta_product.manufacturing_name)
            if meta_product.category:
                categories.append(meta_product.category.rstrip())

            price = meta_product.get_price()
            if price:
                prices.append(price)

        # Update Meta Category
        category_name = most_frequent(categories)
        if category_name:
            try:
                meta_category = MetaCategory.objects.get(name=category_name)
            except:
                meta_category = MetaCategory.objects.create(name=category_name)

            try:
                if self.meta_category and self.meta_category.products.count() <= 1: self.meta_category.delete()
            except:
                pass
            self.meta_category = meta_category

            if self.meta_category.category:
                self.price = min(prices) if prices else None
                self.manufacturing_name = most_frequent(manufacturing_names)
                self.update_name(names)
                self.update_specs(specs_list)

                # Update Manufacturer
                first_names = [name.split(' ', 1)[0] for name in names]
                manufacturer_name = most_frequent(first_names)
                if manufacturer_name:
                    try: manufacturer = Manufacturer.objects.get(name=manufacturer_name)
                    except: manufacturer = Manufacturer.objects.create(name=manufacturer_name)

                    if self.manufacturer and self.manufacturer.products.count() <= 1:
                        try:
                            self.manufacturer.delete()
                        except:
                            pass
                    self.manufacturer = manufacturer

                try:
                    meta_product_with_image = self.meta_products.get(image != None)
                    if meta_product_with_image:
                        self.image = meta_product_with_image.image
                except:
                    pass

    def get_websites(self):
        metaproducts = [[mp.website, mp.get_price()] for mp in self.meta_products.all()]
        return metaproducts

    def image_tag(self):
        return mark_safe('<img src="/media/%s" height="50" />' % self.image)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return "<Product {}>".format(self.name)


class MetaProduct(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True)
    _category = models.CharField("category", max_length=32, blank=True, null=True)
    _manufacturing_name = models.CharField('manufacturing_name', max_length=128, blank=True, null=True)
    url = models.CharField('url', max_length=128, blank=True)
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    host = models.ForeignKey(Website, related_name="meta_products", on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, related_name="meta_products", on_delete=models.CASCADE, null=True)

    def set_specs(self, specs):
        for key, value in specs.items():
            try:
                spec = self.specs.get(key__iexact=key, value__iexact=value)
            except:
                try:
                    spec = Spec.objects.get(key__iexact=key, value__iexact=value)
                    spec.meta_products.add(self)
                    self.save()
                    spec.save()
                except:
                    spec = Spec.objects.create(key=key, value=value)

            try:
                other_spec = Spec.objects.get(key__iexact=key)
            except:
                other_spec = None

            if other_spec:
                if other_spec.spec_group:
                    spec.spec_group = other_spec.spec_group
                    spec.save()
                else:
                    spec_group = SpecGroup.objects.create(key=spec.key)
                    spec.spec_group = spec_group
                    spec.save()
                    other_spec.spec_group = spec_group
                    other_spec.save()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, categories):
        list_len = len(categories)
        last_str = categories[:-1]
        self._category = categories[:-2].rstrip() if SequenceMatcher(None, last_str, self.name).ratio() >= 0.7 else last_str
        self.name.replace(self._category, "")

    @property
    def manufacturing_name(self):
        return self._manufacturing_name

    @manufacturing_name.setter
    def manufacturing_name(self, name):
        if name is None:
            try:
                for key in ["Tillverkarens artikelnr", "Tillverkarens ArtNr", "Artikelnr", "Artnr"]:
                    try:
                        self._manufacturing_name = self.specs.get(key=key).value
                        break
                    except:
                        pass
            except:
                pass
        else:
            self._manufacturing_name = name

    def get_price(self):
        price_history = self.price_history.first()
        if price_history:
            return price_history.price
        else:
            return None

    def image_tag(self):
        return mark_safe('<img src="/media/%s" height="50" />' % self.image)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return "<MetaProduct {} {} {}>".format(self.name, self.category, self.get_price())


class Price(models.Model):
    meta_product = models.ForeignKey(MetaProduct, related_name="price_history", on_delete=models.CASCADE)
    _price = models.IntegerField(blank=True, null=True)
    date_seen = models.DateTimeField(auto_now_add=True)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        dot_pos = price.find(".")
        comma_pos = price.find(",")

        if 0 <= dot_pos < comma_pos:
            price = price[dot_pos:comma_pos]
        elif 0 <= comma_pos < dot_pos:
            price = price[comma_pos:dot_pos]

        if price != "" and price != None:
            price = int(re.sub("\D", "", str(price)))
            self._price = None if price >= 10 ** 6 else price
        else:
            self._price = None

    def __str__(self):
        return "<Price {} {} {}>".format(self.id, self.price, self.date_seen)


class SpecGroupCollection(models.Model):
    _name = models.CharField('name', max_length=128, blank=True, null=True)

    @property
    def name(self):
        if self._name == "" or self._name == None:
            try:
                return self.spec_groups[0].key
            except:
                return ""
        else:
            return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def __str__(self):
        return "<SpecGroupCollection {} {}>".format(self.id, self.name)


class SpecGroup(models.Model):
    key = models.CharField('key', max_length=128, blank=True)
    spec_group_collection = models.ForeignKey(SpecGroupCollection, related_name="spec_groups", on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "<SpecGroup {} {}>".format(self.id, self.key)


class Spec(models.Model):
    meta_products = models.ManyToManyField(MetaProduct, related_name="specs")
    spec_group = models.ForeignKey(SpecGroup, related_name="specs", on_delete=models.CASCADE, blank=True, null=True)
    key = models.CharField('key', max_length=128, blank=True)
    value = models.CharField('value', max_length=128, blank=True)

    def __str__(self):
        return "<Spec {} {} {}>".format(self.id, self.key, self.value)

