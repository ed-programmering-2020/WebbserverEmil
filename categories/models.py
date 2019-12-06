from django.db import models
from products.models import Product, Spec, SpecGroup, SpecGroupCollection
from enum import Enum


class Usages(Enum):
    General = 1
    Gaming = 2


class Category(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def find_with_price(self, products, value_range, strict=True):
        low_price, high_price = value_range
        low_price -= 1

        if strict:
            try:
                return products.filter(get_price__lte=low_price, get__gte=high_price)
            except:
                return None
        else:
            raise NotImplementedError

    def get_recommendations(self, usage):
        raise NotImplementedError

    def match(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    class Meta:
        verbose_name_plural = 'Categories'


class Laptop(Category):
    def get_recommendations(self, usage):
        if usage == Usages.General:
            return {
                "price": (3000, 11000),
                "size": (13.3, 15.6)
            }
        elif usage == Usages.Gaming:
            return {
                "price": (6000, 14000),
                "size": (14, 17.3)
            }

        raise NotImplementedError

    def find_with_size(self, products, size):
        min_size, max_size = size

        try:
            spec_groups = SpecGroupCollection.objects.get(name="screen size").spec_groups.all()
            spec_keys = [spec_group.key for spec_group in spec_groups]
        except:
            return None

        checked_products = []
        for product in products:
            for key in spec_keys:
                try:
                    screen_size = product.specs.get(key=key)
                    if min_size < screen_size.value < max_size:
                        checked_products.append(product)
                    break
                except:
                    pass

        return checked_products

    def sort_with_priorities(self, products, priorities):
        return products

    def match(self, **kwargs):
        kwargs = {
            "usage": {
                "value": "general"
            },
            "price": {
                "range": (1000, 4000),
            },
            "size": {
                "values": (13.3, 15.6)
            },
            "priorities": {
                "battery": 0,
                "performance": 0,
                "storage": 0,
                "screen": 0,
                "ports": 0
            }
        }

        all_products = []
        for meta_category in self.meta_categories:
            all_products.extend(meta_category.products)

        products_price_matched = self.find_with_price(all_products, kwargs["price"]["range"], True)
        product_size_matched = self.find_with_size(products_price_matched, kwargs["size"]["values"])
        products_prioritization_sorted = self.sort_with_priorities(product_size_matched, kwargs["priorities"])

    def __str__(self):
        return "<Laptop>"


class MetaCategory(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)
    category = models.ForeignKey(Category, related_name="meta_categories", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "<MetaCategory %s>" % self.name

    class Meta:
        verbose_name_plural = 'Meta categories'
