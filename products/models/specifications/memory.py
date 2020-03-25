from .base import StandardSpecification, SpecifiedSpecification
from django.db import models


class Ram(StandardSpecification):
    name = "Ram minne"
    raw_value = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = "Ram storage"

    @StandardSpecification.value.getter
    def value(self):
        return str(self.raw_value) + " GB"

    def __str__(self):
        return "<Ram %s>" % self.value


class StorageSize(StandardSpecification):
    name = "Hårddiskkapacitet"
    raw_value = models.PositiveSmallIntegerField()

    @property
    def value(self):
        return str(self.raw_value) + " GB"

    @value.setter
    def value(self, value):
        value.lower()
        number = int(value.split(" ")[0].split(".")[0])

        # Convert to gigabyte
        if "tb" in value or number <= 4:
            number *= 1000  # Not 1024 because a few websites formats it that way already

        self.raw_value = number

    def __str__(self):
        return "<StorageSize %s>" % self.value


class StorageType(SpecifiedSpecification):
    name = "Hårddisktyp"
    types = ["ssd", "hdd", "emmc"]

    def __str__(self):
        return "<StorageType %s>" % self.value
