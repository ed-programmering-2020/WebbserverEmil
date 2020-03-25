from .base import StandardSpecification, SpecifiedSpecification
from django.db import models


class Ram(StandardSpecification):
    # Settings
    name = "Ram minne"
    unit = " GB"

    # Fields
    raw_value = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = "Ram storage"

    def __str__(self):
        return "<Ram %sGb>" % self._value


class StorageSize(StandardSpecification):
    # Settings
    name = "Hårddiskkapacitet"
    unit = " GB"

    # Fields
    raw_value = models.PositiveSmallIntegerField

    @property
    def value(self):
        return self.raw_value

    @value.setter
    def value(self, value):
        value.lower()
        number = int(value.split(" ")[0].split(".")[0])

        # Convert to gigabyte
        if "tb" in value or number <= 4:
            number *= 1000  # Not 1024 because a few websites formats it that way already

        self.raw_value = number

    def __str__(self):
        return "<StorageSize %sGb>" % self._value


class StorageType(SpecifiedSpecification):
    # Settings
    name = "Hårddisktyp"
    types = ["ssd", "hdd", "emmc"]

    @property
    def value(self):
        return self.raw_value.upper()

    def __str__(self):
        return "<StorageType %s>" % self.value
