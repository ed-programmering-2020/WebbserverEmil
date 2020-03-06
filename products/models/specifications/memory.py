from .base import BaseSpecification, IntegerSpecification, TypeSpecification


class Ram(IntegerSpecification, BaseSpecification):
    name = "ram minne"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.process_number(value)

    def __str__(self):
        return "<Ram %sGb>" % self._value


class StorageSize(IntegerSpecification, BaseSpecification):
    name = "hårddiskkapacitet"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value.lower()
        number = int(value.split(" ")[0].split(".")[0])

        # Convert to gigabyte
        if "tb" in value or number <= 4:
            number *= 1000  # Not 1024 because a few websites formats that way already

        self._value = number

    def __str__(self):
        return "<StorageSize %sGb>" % self._value


class StorageType(TypeSpecification, BaseSpecification):
    name = "hårddisktyp"
    types = ["ssd", "hdd", "emmc"]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.process_text(value)

    def __str__(self):
        return "<StorageType %s>" % (self.value.capitalize() if self.value is not None else None)
