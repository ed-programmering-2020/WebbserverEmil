from .base import BaseSpecification
from django.db import models


class Ram(BaseSpecification):
    name = "Ram minne"
    raw_value = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = "Ram storage"

    @BaseSpecification.value.getter
    def value(self):
        return str(self.raw_value) + " GB"

    def __str__(self):
        return "<Ram %s>" % self.value
