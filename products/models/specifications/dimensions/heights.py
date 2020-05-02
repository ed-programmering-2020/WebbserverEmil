from products.models.specifications.base import DynamicSpecification
from django.db import models


class Height(DynamicSpecification):
    name = "Höjd"
    baseline_value = 15.0
    reverse = True

    value = models.DecimalField(max_digits=4, decimal_places=2)

    @property
    def formatted_value(self):
        return "%smm" % self.value

    @staticmethod
    def process_value(value):
        value = super(Height, Height).process_value(value)

        # Check for wrong formatting (Inet.se)
        if value > 60:
            value /= 10

        return value
