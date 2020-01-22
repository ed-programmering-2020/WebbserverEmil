from products.matching.matchers import LaptopMatcher
from django.db import models


class Category(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)
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


class Laptop(Category, LaptopMatcher):
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

    def __str__(self):
        return "<Laptop>"
