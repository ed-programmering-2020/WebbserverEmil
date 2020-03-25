from .base import SpecifiedSpecification, StandardSpecification
from django.db import models
import re


class PanelType(SpecifiedSpecification):
    name = "Paneltyp"
    types = [
        "tn",
        "va",
        ["ips", "retina"]
    ]

    def __str__(self):
        return "<PanelType %s>" % self.value


class RefreshRate(StandardSpecification):
    name = "Uppdateringsfrekvens"
    raw_value = models.PositiveSmallIntegerField()

    @StandardSpecification.value.getter
    def value(self):
        return str(self.raw_value) + " Hz"

    def __str__(self):
        return "<RefreshRate %s>" % self.value


class Resolution(StandardSpecification):
    name = "Upplösning"
    raw_value = models.PositiveSmallIntegerField()

    @property
    def value(self):
        return str(self.raw_value) + "p"

    @value.setter
    def value(self, value):
        numbers = re.findall(r'\d+', value)
        if len(numbers) >= 2:
            self.raw_value = int(numbers[1])
        elif len(numbers) == 1:
            self.raw_value = int(numbers[0])

    def __str__(self):
        return "<Resolution %s>" % self.value


class ScreenSize(StandardSpecification):
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
