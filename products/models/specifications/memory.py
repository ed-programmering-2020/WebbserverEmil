from .base import BaseSpecification, IntegerSpecification, TypeSpecification


class Ram(BaseSpecification, IntegerSpecification):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.process_number(value)

    def __str__(self):
        return "<Ram %s>" % self._value


class StorageSize(BaseSpecification, IntegerSpecification):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value.lower()
        number = int(value.split(" ")[0])

        if "tb" in value:
            number *= 1024

        self._value = number

    def __str__(self):
        return "<StorageSize %s>" % self._value


class StorageType(BaseSpecification, TypeSpecification):
    types = ["ssd", "hdd", "emmc"]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.process_text(value)

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return "<StorageType %s>" % self._value
