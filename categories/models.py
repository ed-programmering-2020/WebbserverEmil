from django.db import models


class Category(models.Model):
    name = models.CharField('name', max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def match(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

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
        verbose_name_plural = 'Meta categories'
