from products.models.polymorphism import PolymorphicModel, ModelType, AlternativeModelName
from products.models.specifications import BaseSpecification
from difflib import SequenceMatcher
from collections import defaultdict
from django.db.models import Q
from django.db import models


class AlternativeCategoryName(AlternativeModelName):
    category_product_type = models.ForeignKey(
        "products.BaseCategoryProduct",
        related_name="alternative_category_names",
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return "<AlternativeCategoryName {self.name}>".format(self=self)


class BaseCategoryProduct(PolymorphicModel):
    name = models.CharField('name', max_length=128)
    manufacturing_name = models.CharField("manufacturing name", max_length=128)
    score = models.DecimalField("score", max_digits=9, decimal_places=9, null=True)
    price = models.IntegerField("price")
    is_active = models.BooleanField(default=True)
    is_ranked = models.BooleanField("is ranked", default=False)
    category_product_type = models.ForeignKey(
        "products.CategoryProductType",
        related_name="category_products",
        null=True,
        on_delete=models.SET_NULL
    )

    objects = models.Manager()

    @staticmethod
    def match(settings, **kwargs):
        """Matches the user with products based on their preferences/settings"""

        model = kwargs.get("model", None)
        if model:
            price = settings.get("price", None)
            if price:
                min_price, max_price = settings["price"]
                return model.inherited_objects.filter(Q(price__gte=min_price), Q(price__lte=max_price))

            else:
                return model.inherited_objects.all()

        return None

    def update(self):
        # Gather meta data
        data = defaultdict(default_factory=[])
        for product in self.products.all():
            data["names"].append(product.name)
            data["specifications"].append(product.get_specs())
            data["manufacturing_names"].append(product.manufacturing_name)
            data["prices"].append(product.get_price())

        # Update product
        if len(data["prices"]) >= 2:
            if self.check_price_outlier(data["prices"]):
                min_price = min(data["prices"])
                data["prices"].remove(min_price)

            self.price = min(data["prices"])

        if self.manufacturing_name is None:
            for manufacturing_name in data["manufacturing_names"]:
                if manufacturing_name:
                    self.manufacturing_name = manufacturing_name
                    break

        self.update_name(data["names"])
        self.update_specs(data["specs"])
        self.is_ranked = False
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
                            other_word = words.get(other_word, None)
                            if not other_word:
                                other_length = len(other_word)

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
        specifications = BaseSpecification.get_specification_instances(specs_list)

        for specification in specifications:
            specification_attribute_name = specification.get_attribute_like_name

            if hasattr(specification, specification_attribute_name):
                eval_string = "self.{}_id = {}".format(specification_attribute_name, specification.id)
                eval(eval_string)

    def check_price_outlier(self, prices):
        sorted_prices = sorted(prices)
        relative_min_price = sorted_prices[1] / 2

        return sorted_prices[0] >= relative_min_price

    def get_product_list(self):
        urls = []
        prices = []
        for product in self.products.all():
            urls.append(product.url)
            prices.append(product.get_price())

        if self.check_price_outlier(prices):
            i = prices.index(min(prices))
            urls.pop(i)
            prices.pop(i)

        return list(zip(urls, prices))

    def get_image(self):
        images = [mp.image for mp in self.products.all() if mp.image]
        if len(images) > 0:
            return images[0].url
        return None


class CategoryProductType(ModelType):
    model = BaseCategoryProduct
