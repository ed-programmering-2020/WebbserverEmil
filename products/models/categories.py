from products.matching.matchers import LaptopMatcher
from django.db import models


class Category(models.Model):
    name = models.CharField('name', max_length=32)
    is_active = models.BooleanField(default=True)

    def get_all_products(self):
        all_products = None
        for meta_category in self.meta_categories.all():
            products = meta_category.products.all()

            if all_products:
                all_products = all_products | products
            else:
                all_products = products

        return all_products

    def product_count(self):
        total = 0
        for meta_category in self.meta_categories.all():
            total += meta_category.products.count()

        return total

    def __str__(self):
        return "<Category %s>" % self.name

    class Meta:
        verbose_name_plural = 'Categories'
        abstract = True


class Laptop(Category, LaptopMatcher):
    @classmethod
    def create(cls):
        return cls(name="Laptop").save()

    @staticmethod
    def get_recommendations(usage):
        if usage == "general":
            return {
                "price": [3000, 11000],
                "size": [13.3, 15.6]
            }
        elif usage == "gaming":
            return {
                "price": [6000, 14000],
                "size": [14, 17.3]
            }
        else:
            return None

    def match(self, settings):
        all_products = self.get_all_products()
        return super().find_with_settings(all_products, settings)
