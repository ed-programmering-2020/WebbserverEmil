from products.models.specifications.base import DynamicSpecification
from django.db import models
import re


class Resolution(DynamicSpecification):
    name = "Upplösning"
    shortened_values = {2: 1080, 4: 2160, 5: 2880, 6: 3160, 8: 4320}
    baseline_value = 1080

    value = models.PositiveSmallIntegerField()

    @property
    def formatted_value(self):
        return "%sp" % self.value

    @staticmethod
    def process_value(value):
        numbers = re.findall(r'\d+', value)

        if len(numbers) >= 2:
            value = numbers[1]  # 1920x1080
        elif len(numbers) == 1:
            value = numbers[0]  # 1080p

        value = int(value)
        if value in Resolution.shortened_values:
            return Resolution.shortened_values[value]
        else:
            return value