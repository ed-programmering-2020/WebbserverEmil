from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from difflib import SequenceMatcher
from django.db import models
import importlib
import json
import uuid
import re


def get_file_path(instance, filename):
    return "%s.%s" % (uuid.uuid4(), "jpg")


class Country(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=64, blank=True)
    currency = models.CharField('currency', max_length=64, blank=True)
    currency_short = models.CharField('currency_short', max_length=16, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return "<Country %s>" % self.name


class Website(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True)
    url = models.CharField('url', max_length=256, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "<Website {} {} {}>".format(self.id, self.name, self.country.name)


class Product(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True, null=True)
    meta_category = models.ForeignKey("products.MetaCategory", related_name="products", on_delete=models.CASCADE, blank=True, null=True)
    manufacturing_name = models.CharField('manufacturing_name', max_length=128, blank=True, null=True)

    def most_frequent(self, List):
        return max(set(List), key=List.count) if List != [] else None

    def update(self):
        categories, names, prices, manufacturing_names, specs_list, important_words = [], [], [], [], [], []
        for meta_product in self.meta_products.all():
            names.append(meta_product.name)
            specs_list.append(meta_product.get_specs())
            manufacturing_names.append(meta_product.manufacturing_name)
            if meta_product.category:
                categories.append(meta_product.category.rstrip())

            price = meta_product.get_price()
            if price:
                prices.append(price)

        # Update Meta Category
        category_name = self.most_frequent(categories)
        if category_name:
            meta_category_model = importlib.import_module("products.models").MetaCategory

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
            if self.meta_category.category:
                self.update_specs(specs_list)

        self.save()

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
                                if word in words:
                                    words[word].append(pos)
                                else:
                                    words[word] = [pos]

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

    def update_specs(self, specs_list):
        updated_specs = []
        category = self.meta_category.category
        
        for specs in specs_list:
            for spec in specs:
                key = spec[0]
                value = spec[1]

                # Get key
                try:
                    spec_key = SpecKey.objects.get(key__iexact=key, category=category)
                except SpecKey.DoesNotExist:
                    spec_key = SpecKey.objects.create(key=key, category=category)
                    spec_key.save()

                # Get value
                try:
                    self.spec_values.get(value__iexact=value, spec_key=spec_key)
                except SpecValue.DoesNotExist:
                    spec_value = SpecValue.objects.create(value=value, spec_key=spec_key)
                    spec_value.products.add(self)
                    spec_value.save()
                    updated_specs.append(spec_value)

        # Delete old spec values
        for spec_value in self.spec_values.all():
            if spec_value not in updated_specs:
                if spec_value.products.count == 1:
                    spec_value.delete()
                else:
                    spec_value.remove(self)

    def get_websites(self):
        meta_products = [[mp.url, mp.get_price()] for mp in self.meta_products.all() if mp.get_price()]
        return meta_products

    def get_image(self):
        images = [mp.image for mp in self.meta_products.all() if mp.image]
        if len(images) > 0:
            return images[0].url
        return None

    def get_price(self):
        prices = [mp.get_price() for mp in self.meta_products.all() if mp.get_price()]
        if len(prices) > 0:
            return min(prices)
        return None

    def __str__(self):
        return "<Product {}>".format(self.name)


class MetaProduct(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True)
    manufacturing_name = models.CharField('manufacturing_name', max_length=128, blank=True, null=True)
    category = models.CharField("category", max_length=32, blank=True, null=True)
    url = models.CharField('url', max_length=128, blank=True)
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    _specs = models.CharField("specs", max_length=4096, default=json.dumps([]))
    host = models.ForeignKey(Website, related_name="meta_products", on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, related_name="meta_products", on_delete=models.CASCADE, null=True)

    def update(self, data):
        # Update external models
        self.save()
        price_obj = Price(meta_product=self)
        price_obj.price = data.get("price")
        price_obj.save()

        # Update internals
        specs = data.get("specs")
        if specs:
            self._specs = json.dumps(specs)
        self.save()

    def get_price(self):
        price = self.price_history.first()

        if price:
            return price.price
        return None

    def get_specs(self):
        return json.loads(self._specs)

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


class SpecGroup(models.Model):
    name = models.CharField('name', max_length=128, blank=True, null=True)

    def __str__(self):
        return "<SpecGroup %s>" % self.name


class SpecKey(models.Model):
    spec_group = models.ForeignKey(SpecGroup, related_name="spec_keys", on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey("products.Category", related_name="spec_keys", on_delete=models.CASCADE, blank=True, null=True)
    key = models.CharField('key', max_length=128, blank=True)

    def __str__(self):
        return "<SpecKey %s %s>" % (self.key, self.category)


class SpecValue(models.Model):
    products = models.ManyToManyField(Product, related_name="spec_values")
    spec_key = models.ForeignKey(SpecKey, related_name="spec_values", on_delete=models.CASCADE, blank=True, null=True)
    value = models.CharField('value', max_length=128, blank=True)

    def __str__(self):
        return "<SpecValue %s>" % self.value

