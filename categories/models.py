from categories.matchers import LaptopMatcher
from categories.customizers import LaptopCustomizer
from categories.values import LaptopValues
from django.db import models
import operator

class Category(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def get_all_products(self):
        all_products = []
        for meta_category in self.meta_categories.all():
            all_products.extend(meta_category.products.all())

        return all_products

    def __str__(self):
        return "<Category %s>" % self.name

    class Meta:
        verbose_name_plural = 'Categories'


class MetaCategory(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)
    category = models.ForeignKey(Category, related_name="meta_categories", on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<MetaCategory %s>" % self.name

    class Meta:
        verbose_name_plural = 'Meta categories'


class Laptop(Category, LaptopMatcher, LaptopCustomizer, LaptopValues):
    def match(self, settings):
        all_products = self.get_all_products()
        return super().find_with_settings(all_products, settings)

    def __str__(self):
        return "<Laptop>"
