from products.models.specifications.base import DynamicSpecification
from django.db import models


class Weight(DynamicSpecification):
    name = "Vikt"
    baseline_value = 1.5
    reverse = True

    value = models.DecimalField(max_digits=3, decimal_places=2)

    @property
    def formatted_value(self):
        return "%s kg" % self.formatted_value

    @staticmethod
    def process_value(value):
        value = value.split(" ")[0]
        value = ''.join(i for i in value if not i.isalpha())

        # Change commas to dots for later float parsing
        if "," in value:
            value = value.replace(",", ".")

        # Convert number into the correct format
        number = float(value)
        if number >= 10:
            number = number / 1000

        return number

    def __str__(self):
        return "<Weight %s>" % self.formatted_value