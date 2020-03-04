from .base import BaseSpecification, IntegerSpecification, DecimalSpecification


class BatteryTime(BaseSpecification, IntegerSpecification):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.process_number(value)

    def __str__(self):
        return "<BatteryTime %sh>" % self._value


class Weight(BaseSpecification, DecimalSpecification):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        number = self.process_value(value)
        if number is not None:
            if number >= 10:
                number = number / 1000

            self._value = number

    def is_better(self, value):
        return self.value < value

    def __str__(self):
        return "<Weight %skg>" % self._value
