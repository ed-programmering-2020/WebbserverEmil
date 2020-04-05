from products.models.specifications.base import DynamicSpecification
from django.db import models


class Height(DynamicSpecification):
    name = "Höjd"
    baseline_value = 150
    reverse = True

    value = models.PositiveSmallIntegerField()

    @property
    def formatted_value(self):
        return "%s mm" % self.formatted_value

    @staticmethod
    def process_value(value):
        number = float(value)
        if number <= 40:
            number *= 10

        return number

    def __str__(self):
        return "<Height %s>" % self.formatted_value
