from django.db import models
from statistics import mode
from scraping.models import Website
from difflib import SequenceMatcher
import json, re


class Manufacturer(models.Model):
    name = models.CharField('name', max_length=30, blank=True)

    def __str__(self):
        return "<Manufacturer %s>" % self.name


class Category(models.Model):
    name = models.CharField('name', max_length=30, blank=True)

    def __str__(self):
        return "<Category %s>" % self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True, null=True)
    _specs = models.CharField("specs", max_length=256, default=json.dumps({}))
    prices = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, null=True)
    manufacturer = models.ForeignKey(Manufacturer, related_name="products", on_delete=models.CASCADE, null=True)

    @property
    def specs(self):
        return json.loads(self._specs)

    @specs.setter
    def specs(self, specs):
        self._specs = json.dumps(self.specs.update(specs))

    def update_specs(self, specs_list):
        combined_specs = {}

        for specs in specs_list:
            combined_specs.update(specs)

        self.specs = combined_specs

    def update_name(self, names):
        words = {}
        for name in names:
            split_words = name.split(" ")

            for other_name in names:
                if name != other_name:
                    for split_word in split_words:
                        pos = other_name.find(split_word)

                        if pos >= 0:
                            if split_word in words:
                                words[split_word].append(pos)
                            else:
                                words[split_word] = [pos]

        calc_words = {}
        for word, pos_list in words.items():
            pos = sum(pos_list) / len(pos_list)
            calc_words[word] = pos

        sorted_words = sorted(calc_words.items(), key=lambda kv: kv[1])
        name = ""

        for word, pos in sorted_words:
            if len(name) > 0:
                name += " " + word
            else:
                name = word

        self.name = name

    def update_info(self):
        print(-1)
        categories, names, prices, specs_list, important_words = [], [], [], [], []
        for meta_product in self.meta_products:
            names.append(meta_product.name)
            specs_list.append(meta_product.specs)
            if meta_product.category: categories.append(meta_product.category)
            if meta_product.price: prices.append(meta_product.price)
        print(-2)

        self.price = min(prices)
        self.update_name(names)
        self.update_specs(specs_list)

        print(-3)
        # Update Category
        category_name = mode(categories)
        try:
            category = Category.objects.get(name=category_name)
        except:
            category = Category.objects.create(name=category_name)
        self.category = category

        print(-4)
        # Update Manufacturer
        first_names = [name.split(' ', 1)[0] for name in names]
        manufacturer_name = mode(first_names)
        try:
            manufacturer = Manufacturer.objects.get(name=manufacturer_name)
        except:
            manufacturer = Manufacturer.objects.create(name=manufacturer_name)
        self.manufacturer = manufacturer

        print(-5)

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
        print(specs)
        for key, value in specs.items():
            try:
                spec = Spec.objects.get(meta_product=self, key__iexact=key)
                spec.value = value
                spec.save()
            except:
                spec = Spec.objects.create(meta_product=self, key=key, value=value)

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
        last_str = categories[list_len - 1]
        self._category = categories[list_len - 2] if SequenceMatcher(None, last_str, self.name).ratio() >= 0.7 else last_str
        self.name.replace(self._category, "")

    def get_price(self):
        return self.price_history[len(self.price_history) - 1].price

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

    def __str__(self):
        return "<SpecGroup {} {}>".format(self.id, self.key)


class Spec(models.Model):
    meta_product = models.ForeignKey(MetaProduct, related_name="specs", on_delete=models.CASCADE)
    spec_group = models.ForeignKey(SpecGroup, related_name="specs", on_delete=models.CASCADE, blank=True, null=True)
    key = models.CharField('key', max_length=128, blank=True)
    value = models.CharField('value', max_length=128, blank=True)

    def __str__(self):
        return "<Spec {} {} {}>".format(self.id, self.key, self.value)

