from .base import BaseSpecification, IntegerSpecification


class BatteryTime(BaseSpecification, IntegerSpecification):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.process_number(value)

    def __str__(self):
        return "<BatteryTime %s>" % self._value


class Weight(BaseSpecification, IntegerSpecification):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        number = self.process_number(value)
        if " g" in value:
            number = number / 1000

        self._value = number

    @staticmethod
    def is_better(first, second):
        return first < second

    def __str__(self):
        return "<Weight %skg>" % self._value
