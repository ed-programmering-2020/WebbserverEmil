from .base import BaseSpecification, IntegerSpecification, TypeSpecification


class Ram(IntegerSpecification, BaseSpecification):
    name = "Ram minne (Gb)"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.process_number(value)

    def __str__(self):
        return "<Ram %sGb>" % self._value


class StorageSize(IntegerSpecification, BaseSpecification):
    name = "Hårddiskkapacitet (Gb)"

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
    name = "Hårddisktyp"
    types = ["ssd", "hdd", "emmc"]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        for storage_types in self.types:
            if type(storage_types) is not list:
                storage_types = [storage_types]

            for storage_type in storage_types:
                if storage_type in value:
                    self._value = storage_type
                    break

    def __str__(self):
        return "<StorageType %s>" % (self.value.capitalize() if self.value is not None else None)
