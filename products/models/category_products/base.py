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
from decimal import Decimal
from PIL import Image as PilImage

import requests
import json
import uuid
import io


def create_file_path(instance, filename):
    """Generates a random unique filepath"""
    return "%s.%s" % (uuid.uuid4(), "jpg")


class Image(models.Model):
    image = models.ImageField(upload_to=create_file_path, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    host = models.ForeignKey("products.Website", on_delete=models.CASCADE)
    category_product = models.ForeignKey(
        "products.BaseCategoryProduct",
        on_delete=models.CASCADE,
        related_name="images"
    )


class BaseCategoryProduct(PolymorphicModel):
    name = models.CharField('name', max_length=128)
    slug = models.SlugField(null=True, blank=True)
    manufacturing_name = models.CharField("manufacturing name", max_length=128, null=True, blank=True)
    active_price = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    @property
    def specifications(self):
        """Returns a list specification key value pairs"""
        if type(self) == BaseCategoryProduct:
            return None

        instances = [eval("self."+specification["name"]) for specification in self.specification_info]
        serialized = {instance.name: str(instance.value) for instance in instances if instance is not None}
        return serialized

    @property
    def websites(self):
        """Returns a sorted list of websites and its required attributes"""
        websites = [{"website_name": product.name, "url": product.url, "price": product.price}
                    for product in self.products.all() if product.price is not None]
        sorted_list = sorted(websites, key=itemgetter("price"))
        return sorted_list

    @property
    def images(self):
        """Returns a list of image urls"""
        image_urls = []
        for instance in self.images:
            url = instance.image.url

            if instance.is_primary is True:
                image_urls.index(url, 0)
            else:
                image_urls.append(url)

        return image_urls

    def save(self, *args, **kwargs):
        """Overridden save method to automatically update slug field"""
        self.slug = slugify(self.name)
        super(BaseCategoryProduct, self).save(*args, **kwargs)

    def calculate_score(self, score, price_range):
        """Calculates score with a bias towards prices closer to the upper 75% line of the price range given"""
        absolute_delta = price_range["max"] - price_range["min"]
        upper_mid = absolute_delta * 0.5 + price_range["min"]
        delta_price = abs(self.lowest_price - upper_mid)
        relative_distance = (1 - (delta_price / absolute_delta))**2

        score = score * Decimal(relative_distance)
        return score / self.lowest_price

    def has_ranked_specification(self, specification_name):
        """Checks if the category product has a given specification and if that specification is ranked"""
        has_specification = eval("self.%s is not None" % specification_name)
        if not has_specification:
            return False

        is_ranked = eval("self.%s.score is not None" % specification_name)
        return is_ranked

    def check_price_outlier(self, prices):
        """Checks if the smallest price in a list is not disproportionate to the other prices"""
        sorted_prices = sorted(prices)
        return sorted_prices[0] >= (sorted_prices[1] / 2)

    def update(self):
        """Updates the category product with all of data from all of its belonging products"""
        names = manufacturing_names = specifications = prices = image_urls = []
        for product in self.products.all():
            names.append(product.name)
            manufacturing_names.append(product.manufacturing_name)
            specifications.append(specifications)

            price = product.price
            if price is not None:
                prices.append(price)

            image_urls = product.image_urls
            if image_urls.count() is not 0:
                image_urls.extend([(image_url.url, image_url.host.id) for image_url in image_urls])

        # Update price
        if len(prices) >= 2:
            self.lowest_price = min(prices)
        elif len(prices) == 1:
            self.lowest_price = prices[0]

        # Update manufacturing name
        if self.manufacturing_name is None:
            for manufacturing_name in manufacturing_names:
                if manufacturing_name:
                    self.manufacturing_name = manufacturing_name
                    break

        if self.is_active is False:
            specifications_caught = 0
            for specifications in specifications:
                specification_instances = BaseSpecification.get_specification_instances(specifications)

                for specification in specification_instances:
                    specification_attribute_name = specification.to_attribute_name()
                    exec("self.{}_id = {}".format(specification_attribute_name, specification.id))
                    specifications_caught += 1

            # Delete category product if no specification were found
            if specifications_caught <= 2:
                self.delete()
                return

            # Update images
            image_count = self.images.count()
            if image_count < 5 and len(image_urls) is not 0:
                images_needed = 5 - image_count

                for i in range(images_needed):
                    image_url, host_id = image_urls[i]
                    r = requests.get(image_url)
                    image_data = io.BytesIO(r.read())
                    image = PilImage.open(image_data)
                    Image.objects.create(image=image, host_id=host_id, category_product_id=self.id)

    @staticmethod
    def match(settings, model):
        """Matches the user with products based on their preferences/settings"""
        model_instances = model.objects.exclude(price=None).filter(is_active=True)

        # Get price range or else return instances without filtering
        price_range = settings.get("price", None)
        if price_range is None:
            return model_instances

        # Return price filtered model instances
        price_range_dict = json.loads(price_range)
        return model_instances.filter(Q(price__gte=price_range_dict["min"]), Q(price__lte=price_range_dict["max"]))

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
        name = product.name.lower()
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
            names = [product.name.lower() for product in category_product.products.all()]
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
        if specifications is None:
            return False

        matches = 0
        specification_instances = BaseSpecification.get_specification_instances(specifications)
        for specification in specification_instances:
            matches += 1

            specification_attribute_name = specification.to_attribute_name
            if not hasattr(specification, specification_attribute_name):
                continue

            product_specification = getattr(category_product, specification_attribute_name)
            if product_specification.id != specification.id:
                return False

        if matches == 0:
            return False

        return True

    def __str__(self):
        return "<CategoryProduct {self.name}>".format(self=self)
