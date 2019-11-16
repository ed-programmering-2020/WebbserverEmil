from django.db import models
from statistics import mode
import json


class Manufacturer(models.Model):
    name = models.CharField('name', max_length=30, blank=True)

    def __str__(self):
        return "<Manufacturer %s>" % self.name


class Category(models.Model):
    name = models.CharField('name', max_length=30, blank=True)

    def __str__(self):
        return "<Category %s>" % self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=30, blank=True)
    _specs = models.CharField("specs", max_length=256, default=json.dumps({}))
    prices = models.IntegerField()
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, related_name="products", on_delete=models.CASCADE)

    @property
    def specs(self):
        return json.loads(self._specs)

    @specs.setter
    def specs(self, specs):
        self._specs = json.dumps(self.specs.update(specs))

    def update_specs(self, specs_list):
        combined_specs = {}

        for specs in specs_list:
            combined_specs.update(specs)

        self.specs = combined_specs

    def update(self):
        categories, names, prices, specs_list = [], [], [], []
        for meta_product in self.meta_producs:
            names.append(meta_product.name)
            specs_list.append(meta_product.specs)

            if meta_product.category:
                categories.append(meta_product.category)

            if meta_product.price:
                prices.append(meta_product.price)

        first_names = [name.split(' ', 1)[0] for name in names]

        self.name = mode(names)
        self.price = min(prices)
        self.update_specs(specs_list)

        # Update Category
        category_name = mode(categories)
        try:
            category = Category.objects.get(name=category_name)
        except:
            category = Category.objects.create(name=category_name)
        self.category = category

        # Update Manufacturer
        manufacturer_name = mode(first_names)
        try:
            manufacturer = Manufacturer.objects.get(name=manufacturer_name)
        except:
            manufacturer = Manufacturer.objects.create(name=manufacturer_name)
        self.manufacturer = manufacturer

    def __str__(self):
        return "<Product %s>" % self.name


class MetaProduct(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=30, blank=True)
    price = models.IntegerField()
    _specs = models.CharField('specs', max_length=256, default=json.dumps({}))
    url = models.CharField('url', max_length=128, blank=True)
    category = models.CharField("category", max_length=32, blank=True, null=True)
    product = models.ForeignKey(Product, related_name="meta_producs", on_delete=models.CASCADE)

    @property
    def specs(self):
        return json.loads(self._specs)

    @specs.setter
    def specs(self, specs):
        self._specs = json.dumps(specs)

    def __str__(self):
        return "<MetaProduct %s>" % self.name
