from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=30, blank=True)

    def __str__(self):
        return self.name


class MetaProduct(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=30, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Group(models.Model):
    pass


class Manufacturer(models.Model):
    pass


class ProductLine(models.Model):
    pass


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

