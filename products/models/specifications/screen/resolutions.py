from products.models.specifications.base import BaseSpecification
from django.db import models
import re


class Resolution(BaseSpecification):
    name = "Upplösning"
    raw_value = models.PositiveSmallIntegerField()

    @property
    def value(self):
        return str(self.raw_value) + "p"

    @value.setter
    def value(self, value):
        numbers = re.findall(r'\d+', value)

        # Check formatting, for example 1080p vs 1920x1080
        if len(numbers) >= 2:
            self.raw_value = self.format(numbers[1])
        elif len(numbers) == 1:
            self.raw_value = self.format(numbers[0])

    def format(self, value):
        value = int(value)

        if value == 2:
            return 1080
        elif value == 4:
            return 2160
        elif value == 5:
            return 2880
        elif value == 6:
            return 3160
        elif value == 8:
            return 4320

        return value

    def __str__(self):
        return "<Resolution %s>" % self.value