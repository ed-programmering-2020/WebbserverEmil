from .base import BaseSpecification
from django.db import models


class BatteryTime(BaseSpecification):
    name = "Batteritid"
    raw_value = models.PositiveSmallIntegerField()

    @BaseSpecification.value.getter
    def value(self):
        return str(self.raw_value) + " timmar"

    def __str__(self):
        return "<BatteryTime %s>" % self.value

