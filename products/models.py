from django.db import models
from scraping.models import Website
from difflib import SequenceMatcher
import json, re


class Manufacturer(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)

    def __str__(self):
        return "<Manufacturer %s>" % self.name


class Category(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)

    def __str__(self):
        return "<Category %s>" % self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True, null=True)
    _specs = models.CharField("specs", max_length=256, default=json.dumps({}))
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, related_name="products", on_delete=models.CASCADE, blank=True, null=True)

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

        words_copy = words
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

        categories, names, prices, specs_list, important_words = [], [], [], [], []
        for meta_product in self.meta_products.all():
            names.append(meta_product.name)
            specs_list.append(meta_product.specs.all())
            if meta_product.category: categories.append(meta_product.category)

            price = meta_product.get_price()
            if price: prices.append(price)

        self.price = min(prices) if prices else None
        self.update_name(names)
        self.update_specs(specs_list)

        # Update Category
        category_name = most_frequent(categories)
        if category_name:
            try: category = Category.objects.get(name=category_name)
            except: category = Category.objects.create(name=category_name)

            if self.category and self.category.products.count() <= 1: self.category.delete()
            self.category = category

        # Update Manufacturer
        first_names = [name.split(' ', 1)[0] for name in names]
        manufacturer_name = most_frequent(first_names)
        if manufacturer_name:
            try: manufacturer = Manufacturer.objects.get(name=manufacturer_name)
            except: manufacturer = Manufacturer.objects.create(name=manufacturer_name)

            if self.manufacturer and self.manufacturer.products.count() <= 1: self.manufacturer.delete()
            self.manufacturer = manufacturer

    def get_price(self):
        return min([mp.get_price() for mp in self.meta_products.all()])

    def __str__(self):
        return "<Product {}>".format(self.name)


class MetaProduct(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True)
    _category = models.CharField("category", max_length=32, blank=True, null=True)
    url = models.CharField('url', max_length=128, blank=True)
    host = models.ForeignKey(Website, related_name="meta_products", on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, related_name="meta_products", on_delete=models.CASCADE, null=True)

    def set_specs(self, specs):
        for key, value in specs.items():
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
        self._category = categories[:-2] if SequenceMatcher(None, last_str, self.name).ratio() >= 0.7 else last_str
        self.name.replace(self._category, "")

    def get_price(self):
        price_history = self.price_history.first()
        if price_history:
            return price_history.price
        else:
            return None

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

        price = int(re.sub("\D", "", str(price)))
        self._price = None if price >= 10 ** 6 else price

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

