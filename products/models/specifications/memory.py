from .base import BaseSpecification, IntegerSpecification, TypeSpecification


class Ram(BaseSpecification, IntegerSpecification):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.process_number(value)

    def __str__(self):
        return "<Ram %sGb>" % self._value


class StorageSize(BaseSpecification, IntegerSpecification):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value.lower()
        number = int(value.split(" ")[0])

        # Convert to gigabyte
        if "tb" in value or value <= 4:
            number *= 1024

        self._value = number

    def __str__(self):
        return "<StorageSize %sGb>" % self._value


class StorageType(BaseSpecification, TypeSpecification):
    types = ["ssd", "hdd", "emmc"]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.process_text(value)

    def __str__(self):
        return "<StorageType %s>" % self._value.capitalize()
