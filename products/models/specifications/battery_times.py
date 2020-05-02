from products.models.specifications.base import DynamicSpecification
from django.db import models


class BatteryTime(DynamicSpecification):
    name = "Batteritid"
    baseline_value = 8

    value = models.DecimalField(max_digits=3, decimal_places=1)

    @property
    def formatted_value(self):
        return "%s timmar" % self.value
