from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.db import models
from difflib import SequenceMatcher
import importlib
import json
import uuid
import re


def get_file_path(instance, filename):
    return "%s.%s" % (uuid.uuid4(), "jpg")


class Manufacturer(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)

    def __str__(self):
        return "<Manufacturer %s>" % self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True, null=True)
    _specs = models.CharField("specs", max_length=256, default=json.dumps({}))
    meta_category = models.ForeignKey("categories.MetaCategory", related_name="products", on_delete=models.CASCADE, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, related_name="products", on_delete=models.CASCADE, blank=True, null=True)
    manufacturing_name = models.CharField('manufacturing_name', max_length=128, blank=True, null=True)

    @property
    def specs(self):
        return json.loads(self._specs)

    @specs.setter
    def specs(self, specs):
        if self.specs:
            self._specs = json.dumps(self.specs.update(specs))

    def most_frequent(self, List):
        return max(set(List), key=List.count) if List != [] else None

    def update(self):
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
        category_name = self.most_frequent(categories)
        if category_name:
            meta_category_model = importlib.import_module("categories").MetaCategory

            try:
                meta_category = meta_category_model.objects.get(name=category_name)
            except ObjectDoesNotExist:
                meta_category = meta_category_model.objects.create(name=category_name)

            if self.meta_category and self.meta_category.products.count() <= 1:
                try:
                    self.meta_category.delete()
                except ObjectDoesNotExist:
                    pass

            self.meta_category = meta_category

            self.price = min(prices) if prices else None
            self.manufacturing_name = self.most_frequent(manufacturing_names)
            self.update_name(names)
            self.update_specs(specs_list)
            self.update_manufacturer(names)

        self.save()

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

        calc_words = {word: (sum(p) / len(p)) for (word, p) in words.items()}
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

    def update_manufacturer(self, names):
        first_names = [name.split(' ', 1)[0] for name in names]
        manufacturer_name = self.most_frequent(first_names)
        if manufacturer_name:
            try:
                manufacturer = Manufacturer.objects.get(name=manufacturer_name)
            except:
                manufacturer = Manufacturer.objects.create(name=manufacturer_name)

            if self.manufacturer and self.manufacturer.products.count() <= 1:
                try:
                    self.manufacturer.delete()
                except:
                    pass
            self.manufacturer = manufacturer

    def get_websites(self):
        meta_products = [[mp.website, mp.get_price()] for mp in self.meta_products.all()]
        return meta_products

    def __str__(self):
        return "<Product {}>".format(self.name)


class MetaProduct(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True)
    category = models.CharField("category", max_length=32, blank=True, null=True)
    manufacturing_name = models.CharField('manufacturing_name', max_length=128, blank=True, null=True)
    url = models.CharField('url', max_length=128, blank=True)
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    host = models.ForeignKey("scraping.Website", related_name="meta_products", on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, related_name="meta_products", on_delete=models.CASCADE, null=True)

    def update(self, data):
        manufacturing_name = data.get("manufacturing_name")
        category_list = data.get("category")
        specs_json = data.get("specs")
        specs = json.loads(specs_json) if specs_json else None
        price = data.get("price")
        self.save()

        # Update external models
        self.update_specs(specs)
        self.save()
        price_obj = Price(meta_product=self)
        price_obj.price = price
        price_obj.save()

        # Update internals
        self.update_manufacturing_name(manufacturing_name)
        self.is_updated = True
        self.save()

    def update_specs(self, specs):
        if specs:
            updated_specs = []
            for spec in specs:
                key = spec[0]
                value = spec[1]

                try:
                    spec = Spec.objects.get(key__iexact=key, value__iexact=value)
                except ObjectDoesNotExist:
                    spec = Spec.objects.create(key=key, value=value)

                    try:
                        spec_group = SpecGroup.objects.filter(key__iexact=key).first()
                    except ObjectDoesNotExist:
                        spec_group = SpecGroup.objects.create(key=key)

                    spec.spec_group = spec_group
                    spec.save()

                updated_specs.append(spec)

                if self not in spec.meta_products.all():
                    spec.meta_products.add(self)
                    spec.save()

            # Delete non updated specs
            for spec in self.specs.all():
                if spec not in updated_specs:
                    spec.meta_products.remove(self)

                    if spec.meta_products.count() == 0:
                        spec.delete()

    def update_manufacturing_name(self, name):
        if name:
            self.manufacturing_name = name
        else:
            # Find manufacturing name in specs
            for key in ["Tillverkarens artikelnr", "Tillverkarens ArtNr", "Artikelnr", "Artnr"]:
                try:
                    self.manufacturing_name = self.specs.get(key=key).value
                    break
                except ObjectDoesNotExist:
                    pass

    def get_price(self):
        price = self.price_history.first()

        if price:
            return price.price
        else:
            return None

    def serve_admin_image(self):
        return mark_safe('<img src="/media/%s" height="50" />' % self.image)
    serve_admin_image.short_description = 'Image'
    serve_admin_image.allow_tags = True

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
        price = price[0]
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
        return "<Price %s %s>" % (self.price, self.date_seen)


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
        return "<SpecGroupCollection {}>".format(self.name)


class SpecGroup(models.Model):
    key = models.CharField('key', max_length=128, blank=True)
    spec_group_collection = models.ForeignKey(SpecGroupCollection, related_name="spec_groups", on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "<SpecGroup {}>".format(self.key)


class Spec(models.Model):
    meta_products = models.ManyToManyField(MetaProduct, related_name="specs")
    spec_group = models.ForeignKey(SpecGroup, related_name="specs", on_delete=models.CASCADE, blank=True, null=True)
    key = models.CharField('key', max_length=128, blank=True)
    value = models.CharField('value', max_length=128, blank=True)

    def __str__(self):
        return "<Spec %s %s>" % (self.key, self.value)

