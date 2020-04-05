from products.models.specifications.base import DynamicSpecification
from django.db import models


class Ram(DynamicSpecification):
    name = "Ram minne"
    baseline_value = 8

    value = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = "Ram storage"

    @property
    def formatted_value(self):
        return "%s GB" % self.value

    def __str__(self):
        return "<Ram %s>" % self.formatted_value
