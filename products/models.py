from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=30, blank=True)

    def update(self):
        # check if metaproducts have the same category and manufacturer
        pass

    def __str__(self):
        return "<Product %s>" % self.name


class MetaProduct(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=30, blank=True)
    price = models.IntegerField()
    specs = models.CharField('specs', max_length=512, blank=True)
    url = models.CharField('url', max_length=128, blank=True)
    category = models.CharField("category", max_length=32, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "<MetaProduct %s>" % self.name


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

