"""This module contains everything need to create and maintain different category products"""

from products.models.polymorphism import PolymorphicModel, ModelType, AlternativeModelName
from products.models.specifications import BaseSpecification

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from django.db.models import Q
from django.db import models

from operator import itemgetter
from difflib import SequenceMatcher
from collections import defaultdict
import string
import json


class AlternativeCategoryName(AlternativeModelName):
    """Model containing alternative names for categories from different websites"""

    category_product_type = models.ForeignKey(
        "products.CategoryProductType",
        related_name="alternative_category_names",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return "<AlternativeCategoryName {self.name}>".format(self=self)


class BaseCategoryProduct(PolymorphicModel):
    """Base class for all category product models"""

    name = models.CharField('name', max_length=128)
    manufacturing_name = models.CharField("manufacturing name", max_length=128, null=True, blank=True)
    price = models.IntegerField("price", null=True, blank=True)
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
    def match(settings, model):
        """Matches the user with products based on their preferences/settings

        Args:
            settings (dict): settings with matching preferences
            model (class): category product model

        Returns:
            queryset: category products of a given model
        """

        # Query for active model instances with price value
        model_instances = model.objects.exclude(price=None).filter(is_active=True)

        # Get price range or else return instances without filtering
        price_range = json.loads(settings.get("price", None))
        if price_range is not None:
            return model_instances

        # Return price filtered model instances
        return model_instances.filter(Q(price__gte=price_range["min"]), Q(price__lte=price_range["max"]))

    @classmethod
    def create(cls, product, another_product=None):
        """Creates a new category product with either one or two products

        Args:
            product (Product): main product
            another_product (Product): additional product to combine with

        Returns:
            CategoryProduct: created or matching category product
        """

        # When 2 products were given, return the combined category product
        if another_product is not None:
            return cls.combine(product, another_product)

        # Find similar category product
        similar_category_product = cls.find_similar(product)
        if similar_category_product is not None:
            return similar_category_product

        # Create a new category product with only 1 product
        if product.category:
            category_model, category_type = cls.get_category_model(product.category)
            if category_model is not None:
                print(product)
                return category_model.polymorphic_create(category_product_type=category_type)

        return None

    @classmethod
    def create_dummy(cls):
        """Creates a dummy category product based on (non)inherited model """

        try:
            # Get dummy category product if it exists
            cls.objects.get(name="dummy")
        except cls.DoesNotExist:
            # Create dummy category product
            category_product_type = cls.get_category_product_type()
            cls.polymorphic_create(name="dummy", price=0, category_product_type=category_product_type, is_active=False)

    @classmethod
    def combine(cls, first, second):
        """Combines products into category products

        Args:
            first (Product): first product
            second: (Product): second product

        Returns:
            CategoryProduct: combination for the 2 products

        """

        first_category_product = first.category_product
        second_category_product = second.category_product

        # Both products have category products
        if first_category_product and second_category_product:
            category_product = first_category_product

            # Combine all products into one queryset
            first_query_set = category_product.products.all()
            second_query_set = second_category_product.products.all()
            combined_query_set = first_query_set.union(second_query_set)

            # Add products to one of the category products while deleting the other
            category_product.products.set(combined_query_set)
            second_category_product.delete()

            return category_product

        # Only the first product has a category product
        if first_category_product:
            category_product = first_category_product
            category_product.products.add(second)
            return category_product

        # Only the second product has a category product
        if second_category_product:
            category_product = second_category_product
            category_product.products.add(first)
            return category_product

        # Both products have category names
        if first.category or second.category:
            if first.category:
                category_name = first.category
            else:
                category_name = second.category

            # Create new category product
            category_model, category_type = cls.get_category_model(category_name)
            if category_model is not None:
                category_product = category_model.polymorphic_create(category_product_type=category_type)
                category_product.products.set([first, second])
                return category_product

        return None

    @classmethod
    def find_similar(cls, product):
        """Finds a similar category product to a product

        Args:
            product (Product): the product to find similar products with

        Returns:
            CategoryProduct: similar category product
        """

        price = product.price
        if price is None:
            return

        # Calculate min and max price range
        min_price = price / 2.5
        max_price = price * 2.5

        # Get name and specifications
        name = cls.clean_string(product.name)
        specs = product.specifications

        # Find similar category products
        matching_category_products = []
        for category_product in BaseCategoryProduct.objects.all().iterator():
            # Check if the category is fit for being
            no_manufacturing_name = not category_product.manufacturing_name or not product.manufacturing_name
            if not (no_manufacturing_name and category_product.is_active):
                break

            # Check if price is acceptable and specs match
            prices = [product.price for product in category_product.products.all() if product.price is not None]
            average_price = (sum(prices) / len(prices)) / 2
            if not (min_price <= average_price <= max_price) and not cls.matching_specs(specs, category_product):
                break

            # Get top meta-product name similarity
            names = [cls.clean_string(product.name) for product in category_product.products.all()]
            name_similarity = cls.name_similarity(name, names)
            matching_category_products.append((name_similarity, category_product))

        # Return top meta product that is over the threshold
        if len(matching_category_products) != 0:
            top_category_products = max(matching_category_products, key=itemgetter(0))
            name_similarity, category_product = top_category_products
            return category_product

        return None

    @staticmethod
    def get_category_model(category_name):
        """Finds the category model belonging to a certain category name

        Args:
            category_name (str): the given category name

        Returns:
            CategoryProduct: resulting category product model
            CategoryProductType: resulting category product type
        """

        try:
            alternative_category_name = AlternativeCategoryName.objects.get(name=category_name)
            category_product_type = alternative_category_name.category_product_type

            # Get category product model
            if category_product_type is not None:
                category_product_model = category_product_type.get_model()
                return category_product_model, category_product_type

        except AlternativeCategoryName.DoesNotExist:
            AlternativeCategoryName.objects.create(name=category_name)

        return None, None

    @classmethod
    def get_category_product_type(cls):
        """Finds the category product type belonging to category product

        Returns:
            CategoryProductType: resulting category product type
        """

        try:
            # Return existing category product type
            return CategoryProductType.objects.get(name=cls.__name__)
        except CategoryProductType.DoesNotExist:
            return None

    @staticmethod
    def name_similarity(name, names):
        similarity_list = []

        for meta_name in names:
            # Sequence similarity metric
            sequence_sim = SequenceMatcher(None, name, meta_name).ratio()

            # Cosine similarity metric
            names = [name, meta_name]
            vectorizer = CountVectorizer().fit_transform(names)
            vectors = vectorizer.toarray()

            vec1 = vectors[0].reshape(1, -1)
            vec2 = vectors[1].reshape(1, -1)
            cosine_sim = cosine_similarity(vec1, vec2)[0][0]

            # Add highest similarity
            top_similarity = max([sequence_sim, cosine_sim])
            similarity_list.append(top_similarity)

        return max(similarity_list)

    @staticmethod
    def matching_specs(specifications, product):
        if specifications is None:
            return False

        specification_instances = BaseSpecification.get_specification_instances(specifications)
        matches = 0

        for specification in specification_instances:
            specification_attribute_name = specification.to_attribute_name

            if hasattr(specification, specification_attribute_name):
                product_specification = getattr(product, specification_attribute_name)

                if product_specification.id != specification.id:
                    return False

                matches += 1

        if matches > 0:
            return True
        else:
            return False

    @staticmethod
    def clean_string(text):
        text = "".join([word for word in text if word not in string.punctuation])
        text.lower()
        return text

    def update(self):
        # Gather meta data
        data = defaultdict(list)
        for product in self.products.all():
            # Identification
            data["names"].append(product.name)
            data["manufacturing_names"].append(product.manufacturing_name)

            # Specifications
            specifications = product.specifications
            if specifications is not None:
                data["specifications"].append((product.host, specifications))

            # Pricing
            price = product.price
            if price is not None:
                data["prices"].append(price)

        # Update price
        if len(data["prices"]) >= 2:
            if self.check_price_outlier(data["prices"]):
                min_price = min(data["prices"])
                data["prices"].remove(min_price)

            self.price = min(data["prices"])

        # Update manufacturing name
        if self.manufacturing_name is None:
            for manufacturing_name in data["manufacturing_names"]:
                if manufacturing_name:
                    self.manufacturing_name = manufacturing_name
                    break

        # Update specifications
        specifications_caught = 0
        for host, specifications in data["specifications"]:
            specification_instances = BaseSpecification.get_specification_instances(specifications, host)

            for specification in specification_instances:
                specification_attribute_name = specification.to_attribute_name()

                exec("self.{}_id = {}".format(specification_attribute_name, specification.id))
                specifications_caught += 1

        if specifications_caught <= 2:
            self.delete()
            return

        # Update the rest of the category product
        self.update_name(data["names"])
        self.is_ranked = False
        self.save()

    def update_name(self, names):
        if len(names) >= 3:
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
        else:
            name = names[0]

        self.name = name

    def check_price_outlier(self, prices):
        sorted_prices = sorted(prices)
        relative_min_price = sorted_prices[1] / 2

        return sorted_prices[0] >= relative_min_price

    def get_websites(self):
        urls, prices = [], []
        for product in self.products.all():
            urls.append(product.url)

            price = product.price
            if price is not None:
                prices.append(price)

        if len(prices) >= 2 and self.check_price_outlier(prices):
            i = prices.index(min(prices))
            urls.pop(i)
            prices.pop(i)

        return list(zip(urls, prices))

    def get_image(self):
        images = [p.image for p in self.products.all() if p.image]
        if len(images) > 0:
            return images[0].url
        return None

    def __str__(self):
        return "<CategoryProduct {self.name}>".format(self=self)


class CategoryProductType(ModelType):
    """Model used to identify which category product a category belongs to"""

    def get_model(self):
        """Gets the model of its respective category product

        Returns:
            class: Category product model class
        """

        model_instance = BaseCategoryProduct.objects.filter(category_product_type_id=self.id).first()
        return model_instance.get_model()

    def __str__(self):
        return "<CategoryProductType {self.name}>".format(self=self)

