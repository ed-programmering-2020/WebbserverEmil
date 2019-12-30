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
        verbose_name_plural = 'Meta models'


class Laptop(Category, LaptopMatcher, LaptopCustomizer, LaptopValues):
    def match(self, settings):
        all_products = self.get_all_products()

        products_price_matched = self.find_with_price(all_products, settings["price"], True)
        products_size_matched = self.find_with_size(products_price_matched, settings["size"])

        products_with_values = self.sort_with_values(products_size_matched)
        products_usage_sorted = self.sort_with_usage(products_with_values, len(products_size_matched), settings["usage"])
        products_price_sorted = self.sort_with_price(products_usage_sorted)

        top_products = self.get_top_products(products_price_sorted)
        products_prioritization_sorted = self.sort_with_priorities(products_with_values, len(products_size_matched), top_products, settings["priorities"])
        ranked_products = products_prioritization_sorted.sort(key=operator.itemgetter(1), reverse=True)
        product_models = self.get_product_models(ranked_products)

        return self.products_to_json(product_models)

    def __str__(self):
        return "<Laptop>"
