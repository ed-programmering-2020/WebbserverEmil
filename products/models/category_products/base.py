"""This module contains everything need to create and maintain different category products"""

from products.models.polymorphism import PolymorphicModel
from products.models.specifications import BaseSpecification

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from django.utils.text import slugify
from django.db.models import Q
from django.db import models

from operator import itemgetter
from difflib import SequenceMatcher
from collections import defaultdict
from decimal import Decimal
import string
import json


class BaseCategoryProduct(PolymorphicModel):
    """Base class for all category product models"""

    name = models.CharField('name', max_length=128)
    slug = models.SlugField()
    manufacturing_name = models.CharField("manufacturing name", max_length=128, null=True, blank=True)
    price = models.PositiveIntegerField("price", null=True, blank=True)
    is_active = models.BooleanField(default=False)

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
        price_range = settings.get("price", None)
        if price_range is None:
            return model_instances

        # Return price filtered model instances
        price_range_dict = json.loads(price_range)
        return model_instances.filter(Q(price__gte=price_range_dict["min"]), Q(price__lte=price_range_dict["max"]))

    def calculate_score(self, score, price_range):
        """Calculates score with a bias towards prices closer to the upper 75% line of the price range given

        Args:
            score: a Decimal score
            price_range: a dict with min and max values for price range

        Returns:
            Decimal: resulting score
        """

        absolute_delta = price_range["max"] - price_range["min"]
        upper_mid = absolute_delta * 0.5 + price_range["min"]
        delta_price = abs(self.price - upper_mid)
        relative_distance = (1 - (delta_price / absolute_delta))**2

        score = score * Decimal(relative_distance)
        return score / self.price

    @classmethod
    def create(cls, product, another_product=None):
        """Creates a new category product with either one or two products"""

        # When 2 products were given, return the combined category product
        if another_product is not None:
            return cls.combine(product, another_product)

        # Find similar category product
        similar_category_product = cls.find_similar(product)
        if similar_category_product is not None:
            return similar_category_product

        # Check if product has a category name
        if not product.category:
            return

        # Check if the category name belongs to a category product type and model
        category_model = cls.get_model_with_name(product.category)
        if category_model is None:
            return

        # Return new category product
        return category_model.objects.create()

    @classmethod
    def combine(cls, first, second):
        """Combines products into category products"""

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
            category_model = cls.get_model_with_name(category_name)
            if category_model is not None:
                category_product = category_model.objects.create()
                category_product.products.set([first, second])
                return category_product

        return None

    @classmethod
    def find_similar(cls, product):
        """Finds a similar category product to a product"""

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
                continue

            # Check if category product has any prices
            prices = [product.price for product in category_product.products.all() if product.price is not None]
            if len(prices) == 0:
                continue

            # Check if price is acceptable and specs match
            average_price = (sum(prices) / len(prices)) / 2
            if not (min_price <= average_price <= max_price) and not cls.matching_specs(specs, category_product):
                continue

            # Get top meta-product name similarity
            names = [cls.clean_string(product.name) for product in category_product.products.all()]
            name_similarity = cls.name_similarity(name, names)
            matching_category_products.append((name_similarity, category_product))

        # Return top meta product that is over the threshold
        if len(matching_category_products) != 0:
            top_category_product = max(matching_category_products, key=itemgetter(0))
            name_similarity, category_product = top_category_product

            if name_similarity >= 0.8:
                return category_product

        return None

    @staticmethod
    def name_similarity(name, other_names):
        """Get the similarity between different names"""

        similarity_list = []
        for other_name in other_names:
            # Sequence similarity metric
            sequence_sim = SequenceMatcher(None, name, other_name).ratio()

            # Cosine similarity metric
            names = [name, other_name]
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
    def matching_specs(specifications, category_product):
        """Check if a category product has a matching set of specifications"""

        # If no specifications are given return false
        if specifications is None:
            return False

        # Iterate trough specifications
        matches = 0
        specification_instances = BaseSpecification.get_specification_instances(specifications)
        for specification in specification_instances:
            specification_attribute_name = specification.to_attribute_name

            # Check if product has specification attribute
            if not hasattr(specification, specification_attribute_name):
                continue

            # Check if specifications match
            product_specification = getattr(category_product, specification_attribute_name)
            if product_specification.id != specification.id:
                return False

            matches += 1

        # If no matching specification where found return false
        if matches == 0:
            return False

        return True

    @staticmethod
    def clean_string(text):
        """Prepare a string to be compared"""

        # Clean string
        text = "".join([word for word in text if word not in string.punctuation])
        text.lower()

        return text

    def update(self):
        """Updates the category product with all of data from all of its belonging products"""

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
        elif len(data["prices"]) == 1:
            self.price = data["prices"][0]

        # Update manufacturing name
        if self.manufacturing_name is None:
            for manufacturing_name in data["manufacturing_names"]:
                if manufacturing_name:
                    self.manufacturing_name = manufacturing_name
                    break

        # Update specifications
        if self.is_active is False:
            specifications_caught = 0
            for host, specifications in data["specifications"]:
                specification_instances = BaseSpecification.get_specification_instances(specifications)
                if specifications_caught < len(specification_instances):
                    specifications_caught = len(specification_instances)

                for specification in specification_instances:
                    specification_attribute_name = specification.to_attribute_name()
                    exec("self.{}_id = {}".format(specification_attribute_name, specification.id))

            # Delete category product if no specification were found
            if specifications_caught <= 2:
                self.delete()
                return

        self.save()

    def has_ranked_specification(self, specification_name):
        """Checks if the category product has a given specification and if that specification is ranked"""

        # Check if the self has a specification
        has_specification = eval("self.%s is not None" % specification_name)
        if not has_specification:
            return False

        # Check if specification is ranked
        is_ranked = eval("self.%s.score is not None" % specification_name)
        return is_ranked

    def check_price_outlier(self, prices):
        """Checks if the smallest price in a list is not disproportionate to the other prices"""

        sorted_prices = sorted(prices)
        relative_min_price = sorted_prices[1] / 2

        return sorted_prices[0] >= relative_min_price

    @property
    def specifications(self):
        """Returns a list specification key value pairs"""

        # When called from base category product return a exception
        if type(self) == BaseCategoryProduct:
            raise TypeError

        # Collect all specifications
        specifications = {}
        for specification in self.specification_info:
            attribute_name = specification["name"]
            instance = eval("self."+attribute_name)

            if instance is None:
                continue
            if instance.value is None:
                continue

            value = str(instance.value)
            if hasattr(instance, "unit"):
                value += instance.unit

            specifications[instance.name] = value

        return specifications

    @property
    def websites(self):
        """Returns a sorted list of websites and its required attributes"""

        # Gather all websites and its data
        websites = []
        for product in self.products.all():
            url = product.url
            name = product.host.name
            price = product.price

            if price is None:
                continue

            websites.append({
                "website_name": name,
                "url": url,
                "price": price
            })

        # return sorted website list
        sorted_list = sorted(websites, key=itemgetter("price"))
        return sorted_list

    @property
    def images(self):
        """Returns a list of image urls"""

        # Gather image urls
        image_urls = [p.image.url for p in self.products.all() if p.image]

        # Return image urls
        return image_urls

    def __str__(self):
        return "<CategoryProduct {self.name}>".format(self=self)
