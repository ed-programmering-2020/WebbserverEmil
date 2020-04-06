from products.models.specifications.base import DynamicSpecification
from django.db import models


class Height(DynamicSpecification):
    name = "Höjd"
    baseline_value = 15.0
    reverse = True

    value = models.DecimalField(max_digits=4, decimal_places=1)

    @property
    def formatted_value(self):
        return "%s mm" % self.value

    def __str__(self):
        return "<Height %s>" % self.formatted_value
