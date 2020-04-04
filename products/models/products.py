"""This module holds the product model and some of its additional model"""

from django.db import models
from django.db.models import Q

import uuid
import json
import re


class Price(models.Model):
    product = models.ForeignKey("products.Product", related_name="price_history", null=True, on_delete=models.CASCADE)
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

        if price == "":
            return

        price = int(re.sub("\D", "", str(price)))
        if price <= 100000:
            self._value = price

    def __str__(self):
        return "<Price {self.value} {self.date_seen}>".format(self=self)


class ImageUrl(models.Model):
    url = models.CharField(max_length=256)
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="image_urls"
    )

    def __str__(self):
        return "<ImageUrl {}>".format(self.url)


class Product(models.Model):
    name = models.CharField('name', max_length=128)
    manufacturing_name = models.CharField("manufacturing_name", null=True, max_length=128)
    url = models.CharField('url', max_length=128)
    category = models.CharField("category", max_length=128, null=True)
    _specifications = models.CharField("specifications", max_length=4096, default=json.dumps([]))
    host = models.ForeignKey("products.website", related_name="meta_products", on_delete=models.CASCADE, null=True)
    category_product = models.ForeignKey(
        "products.BaseCategoryProduct",
        related_name="products",
        null=True,
        on_delete=models.CASCADE
    )

    @property
    def price(self):
        if self.price_history.count() == 0:
            return None

        price = self.price_history.latest("date_seen")
        return price.value

    @price.setter
    def price(self, price):
        price_instance = Price(product_id=self.id)
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

    @staticmethod
    def create_or_get(data, host):
        """Create/get and update a product based on the data collected"""
        url = data.get("link")
        manufacturing_name = data.get("manufacturing_name")

        product = Product.objects.filter(Q(url=url) | Q(manufacturing_name=manufacturing_name), Q(host=host)).first()
        if product is None:
            product = Product(
                name=data.get("title"),
                url=url,
                host_id=host.id,
                category=data.get("category"),
                manufacturing_name=manufacturing_name
            )
            product.specifications = data.get("specs")
            product.save()

        product.price = data.get("price")
        for image_url in data.get("image_urls"):
            ImageUrl.objects.create(url=image_url, host_id=host.id, product_id=product.id)
        return product

    def find_similar_product(self):
        """Find products with the same manufacturing name"""
        if not self.manufacturing_name:
            return None

        try:
            return Product.objects.exclude(id=self.id).filter(manufacturing_name=self.manufacturing_name).first()
        except Product.DoesNotExist:
            return None

    def __str__(self):
        return "<Product {self.name} {self.host.name}>".format(self=self)
