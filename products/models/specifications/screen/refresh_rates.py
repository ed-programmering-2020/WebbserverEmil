from products.models.specifications.base import DynamicSpecification
from django.db import models


class RefreshRate(DynamicSpecification):
    name = "Uppdateringsfrekvens"
    baseline_value = "60"

    value = models.PositiveSmallIntegerField()

    @property
    def formatted_value(self):
        return "%s Hz" % self.value

    def __str__(self):
        return "<RefreshRate %s>" % self.formatted_value
