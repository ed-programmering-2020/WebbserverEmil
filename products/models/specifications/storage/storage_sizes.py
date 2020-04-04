from products.models.specifications.base import BaseSpecification
from django.db import models


class StorageSize(BaseSpecification):
    name = "Hårddiskkapacitet"
    raw_value = models.PositiveSmallIntegerField()

    @property
    def value(self):
        return str(self.raw_value) + " GB"

    @value.setter
    def value(self, value):
        value.lower()
        number = int(value.split(" ")[0].split(".")[0])

        # Convert to gigabyte
        if "tb" in value or number <= 4:
            number *= 1000  # Not 1024 because a few websites formats it that way already

        self.raw_value = number

    def __str__(self):
        return "<StorageSize %s>" % self.value


