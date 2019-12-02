from django.db import models
from abc import ABCMeta, abstractmethod


class Category(models.Model, metaclass=ABCMeta):
    name = models.CharField('name', max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    @abstractmethod
    def match(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    class Meta:
        verbose_name_plural = 'Categories'


class Laptop(Category):
    def match(self, **kwargs):
        kwargs = {
            "price": (999, 4000),
            "performance": 7,
            "weight": 5,
            "size": 7
        }

    def __str__(self):
        return "<Laptop>"


class MetaCategory(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)
    category = models.ForeignKey(Category, related_name="meta_categories", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "<MetaCategory %s>" % self.name

    class Meta:
        verbose_name_plural = 'MetaCategories'
