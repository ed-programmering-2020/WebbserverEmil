from products.models.specifications.base import BaseSpecification
from django.db import models


class Weight(BaseSpecification):
    name = "Vikt"
    raw_value = models.DecimalField(max_digits=3, decimal_places=2)

    @property
    def value(self):
        return str(self.raw_value) + " kg"

    @value.setter
    def value(self, value):
        value = value.split(" ")[0]
        value = ''.join(i for i in value if not i.isalpha())

        # Change commas to dots for later float parsing
        if "," in value:
            value = value.replace(",", ".")

        # Check if value is valid
        if value is "":
            return

        # Convert number into the correct format
        number = float(value)
        if number >= 10:
            number = number / 1000

        self.raw_value = number

    def is_better(self, value, **kwargs):
        return self.raw_value < value

    def __str__(self):
        return "<Weight %s>" % self.value