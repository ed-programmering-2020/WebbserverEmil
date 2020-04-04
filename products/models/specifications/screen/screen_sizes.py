from products.models.specifications.base import BaseSpecification
from django.db import models


class ScreenSize(BaseSpecification):
    name = "Skärmstorlek"
    raw_value = models.DecimalField(max_digits=3, decimal_places=1)

    @property
    def value(self):
        return str(self.raw_value) + '"'

    @value.setter
    def value(self, value):
        value = value.split(" ")[0]
        value = ''.join(i for i in value if not i.isalpha())
        value = value.split('"')[0]

        self.raw_value = float(value)

    def __str__(self):
        return "<ScreenSize %s>" % self.value
