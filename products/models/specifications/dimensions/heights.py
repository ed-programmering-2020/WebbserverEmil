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

    @staticmethod
    def process_value(value):
        value = value.split(" ")[0]
        value = ''.join(i for i in value if not i.isalpha())

        # Change commas to dots for later float parsing
        if "," in value:
            value = value.replace(",", ".")

        # Convert number into the correct format
        number = float(value)

        return number

    def __str__(self):
        return "<Height %s>" % self.formatted_value
