from products.models.specifications.base import BaseSpecification
from django.db import models


class RefreshRate(BaseSpecification):
    name = "Uppdateringsfrekvens"
    raw_value = models.PositiveSmallIntegerField()

    @BaseSpecification.value.getter
    def value(self):
        return str(self.raw_value) + " Hz"

    def __str__(self):
        return "<RefreshRate %s>" % self.value
