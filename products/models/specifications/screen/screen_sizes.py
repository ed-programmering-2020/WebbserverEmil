from products.models.specifications.base import DynamicSpecification
from django.db import models


class ScreenSize(DynamicSpecification):
    name = "Skärmstorlek"
    no_score = True

    value = models.DecimalField(max_digits=3, decimal_places=1)

    @property
    def formatted_value(self):
        return '%s"' % self.value

    @staticmethod
    def process_value(value):
        value = value.split(" ")[0].split('"')[0]
        value = ''.join(i for i in value if not i.isalpha())
        return float(value)

    def __str__(self):
        return "<ScreenSize %s>" % self.formatted_value
