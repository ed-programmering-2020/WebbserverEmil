from products.models.specifications.base import DynamicSpecification
from django.db import models


class StorageSize(DynamicSpecification):
    name = "Hårddiskkapacitet"
    baseline_value = 256

    value = models.PositiveSmallIntegerField()

    @property
    def formatted_value(self):
        return "%s GB" % self.value

    @staticmethod
    def process_value(value):
        value = value.lower()
        number = int(value.split(" ")[0].split(".")[0])
        # Convert to gigabyte
        if "tb" in value or number <= 4:
            number *= 1000  # Not 1024 because a few websites formats it that way already
        return number

    def __str__(self):
        return "<StorageSize %s>" % self.formatted_value


