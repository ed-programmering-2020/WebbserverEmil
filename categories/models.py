from django.db import models


class Category(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def find_with_price(self, products, value_range, strict=True):
        low_price, high_price = value_range
        low_price -= 1  # include all one below (999 vs 1000)

        if strict:
            try:
                return products.filter(get_price__lte=low_price, get__gte=high_price)
            except:
                return None
        else:
            raise NotImplementedError

    def match(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    class Meta:
        verbose_name_plural = 'Categories'


class Laptop(Category):
    def match(self, **kwargs):
        kwargs = {
            "usage": {
                "value": "general"
            },
            "price": {
                "range": (1000, 4000),
            },
            "size": {
                "values": ["13.3"]
            },
        }

        all_products = []
        for meta_category in self.meta_categories:
            all_products.extend(meta_category.products)

        products_by_price = self.find_with_price(all_products, kwargs["price"]["range"], True)

    def __str__(self):
        return "<Laptop>"
