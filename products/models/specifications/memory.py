from .base import StandardSpecification, SpecifiedSpecification
from django.db import models


class Ram(StandardSpecification):
    # Settings
    name = "Ram minne"
    unit = " GB"

    # Fields
    _value = models.PositiveSmallIntegerField()

    def __str__(self):
        return "<Ram %sGb>" % self._value


class StorageSize(StandardSpecification):
    # Settings
    name = "Hårddiskkapacitet"
    unit = " GB"

    # Fields
    _value = models.PositiveSmallIntegerField

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value.lower()
        number = int(value.split(" ")[0].split(".")[0])

        # Convert to gigabyte
        if "tb" in value or number <= 4:
            number *= 1000  # Not 1024 because a few websites format the value in that way already

        self._value = number

    def __str__(self):
        return "<StorageSize %sGb>" % self._value


class StorageType(SpecifiedSpecification):
    # Settings
    name = "Hårddisktyp"
    types = ["ssd", "hdd", "emmc"]

    def __str__(self):
        return "<StorageType %s>" % (self.value.capitalize() if self.value is not None else None)
