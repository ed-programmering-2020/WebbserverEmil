"""This module holds the product model and some of its additional model"""

from django.db import models
from django.db.models import Q

import uuid
import json
import re


def get_file_path(instance, filename):
    """Generates a random unique filepath"""

    return "%s.%s" % (uuid.uuid4(), "jpg")


class Product(models.Model):
    """The primary product model which can be collected into a category product"""

    name = models.CharField('name', max_length=128)
    manufacturing_name = models.CharField("manufacturing_name", null=True, max_length=128)
    url = models.CharField('url', max_length=128)
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    category = models.CharField("category", max_length=128, null=True)
    _specifications = models.CharField("specifications", max_length=4096, default=json.dumps([]))

    host = models.ForeignKey("products.website", related_name="meta_products", on_delete=models.CASCADE, null=True)
    category_product = models.ForeignKey(
        "products.BaseCategoryProduct",
        related_name="products",
        null=True,
        on_delete=models.CASCADE
    )

    @staticmethod
    def create_or_get(data, host, files_dict):
        url = data.get("link")
        manufacturing_name = data.get("manufacturing_name")

        # Create/get product
        product = Product.objects.filter(Q(url=url) | Q(manufacturing_name=manufacturing_name), Q(host=host)).first()
        if not product:
            filename = data.get("image")
            image = files_dict.get(filename) if filename else None
            product = Product(
                name=data.get("title"),
                url=url,
                host=host,
                image=image,
                category=data.get("category"),
                manufacturing_name=manufacturing_name
            )
            product.specifications = data.get("specs")

        # Overall update
        product.save()
        product.price = data.get("price")

        return product

    def find_similar_product(self):
        """Find products with the same manufacturing name

        Returns:
            QuerySet: matching products
        """

        # If product has no manufacturing name then return None
        if not self.manufacturing_name:
            return None

        try:
            # Get other products with same manufacturing name
            return Product.objects.exclude(id=self.id).filter(manufacturing_name=self.manufacturing_name).first()
        except Product.DoesNotExist:
            return None

    @property
    def price(self):
        # Check if price history is empty
        if self.price_history.count() == 0:
            return None

        # Return latest price in price history
        price = self.price_history.latest("date_seen")
        return price.value

    @price.setter
    def price(self, price):
        # Create and save price instance
        price_instance = Price()
        price_instance.product_id = self.id
        price_instance.value = price
        price_instance.save()

    @property
    def specifications(self):
        return json.loads(self._specifications)

    @specifications.setter
    def specifications(self, specifications):
        # Remove specifications if json dump is bigger than 4096
        to_string = json.dumps(specifications)
        while len(to_string) > 4096:
            specifications = specifications[:-1]
            to_string = json.dumps(specifications)

        # Set specifications to json dump
        self._specifications = to_string

    def __str__(self):
        return "<Product {self.name} {self.host.name}>".format(self=self)


class Price(models.Model):
    """A model for holding the price of products"""

    product = models.ForeignKey(Product, related_name="price_history", null=True, on_delete=models.CASCADE)
    _value = models.PositiveIntegerField(null=True)
    date_seen = models.DateTimeField(auto_now_add=True)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, price):
        dot_pos = price.find(".")
        comma_pos = price.find(",")

        # Remove unnecessary commas and zeroes
        if 0 <= dot_pos < comma_pos:
            price = price[dot_pos:comma_pos]
        elif 0 <= comma_pos < dot_pos:
            price = price[comma_pos:dot_pos]

        # return if price string is empty
        if price == "":
            return

        # Convert price string to integer
        price = int(re.sub("\D", "", str(price)))

        # Set value with price
        if price <= 100000:
            self._value = price

    def __str__(self):
        return "<Price {self.value} {self.date_seen}>".format(self=self)
