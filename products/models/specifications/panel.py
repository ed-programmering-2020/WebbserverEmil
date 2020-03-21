from .base import SpecifiedSpecification, StandardSpecification
from django.db import models
import re


class PanelType(SpecifiedSpecification):
    # Settings
    name = "Paneltyp"
    types = [
        "tn",
        "va",
        ["ips", "retina"]
    ]

    def __str__(self):
        return "<PanelType %s>" % self._value


class RefreshRate(StandardSpecification):
    # Settings
    name = "Uppdateringsfrekvens"
    unit = " Hz"

    # Fields
    _value = models.PositiveSmallIntegerField()

    def __str__(self):
        return "<RefreshRate %sHz>" % self.value


class Resolution(StandardSpecification):
    # Settings
    name = "Upplösning"
    unit = "p"

    # Fields
    _value = models.PositiveSmallIntegerField()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        numbers = re.findall(r'\d+', value)
        if len(numbers) >= 2:
            self._value = int(numbers[1])
        elif len(numbers) == 1:
            self._value = int(numbers[0])

    def __str__(self):
        return "<Resolution %sp>" % self.value


class ScreenSize(StandardSpecification):
    # Settings
    name = "Skärmstorlek"
    unit = "\""

    # Fields
    _value = models.DecimalField(max_digits=3, decimal_places=1)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value = value.split(" ")[0]
        value = ''.join(i for i in value if not i.isalpha())
        value = value.split('"')[0]

        self._value = float(value)

    def __str__(self):
        return "<ScreenSize %s\">" % self.value
