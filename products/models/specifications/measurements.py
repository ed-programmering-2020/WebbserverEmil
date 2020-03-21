from .base import StandardSpecification
from django.db import models


class BatteryTime(StandardSpecification):
    # Settings
    name = "Batteritid"
    unit = " timmar"

    # Fields
    _value = models.PositiveSmallIntegerField()

    def __str__(self):
        return "<BatteryTime %sh>" % self._value


class Weight(StandardSpecification):
    name = "Vikt"
    unit = " kg"

    # Fields
    _value = models.PositiveSmallIntegerField()

    @property
    def value(self):
        return self._value

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

        self._value = number

    def is_better(self, value, **kwargs):
        """Overridden because it is better if the weight is lighter"""
        return self.value < value

    def __str__(self):
        return "<Weight %skg>" % self._value
