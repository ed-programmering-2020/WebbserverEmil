from products.models.specifications.base import DynamicSpecification
from django.db import models


class BatteryTime(DynamicSpecification):
    name = "Batteritid"
    baseline_value = 8

    value = models.PositiveSmallIntegerField()

    @property
    def formatted_value(self):
        return "%s timmar" % self.value

    def __str__(self):
        return "<BatteryTime %s>" % self.formatted_value

