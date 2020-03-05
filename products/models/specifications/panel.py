from .base import BaseSpecification, TypeSpecification, IntegerSpecification, DecimalSpecification
import re


class PanelType(TypeSpecification, BaseSpecification):
    types = [
        "tn",
        "va",
        ["ips", "retina"]
    ]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.process_text(value)

    def __str__(self):
        return "<PanelType %s>" % self._value


class RefreshRate(IntegerSpecification, BaseSpecification):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.process_number(value)

    def __str__(self):
        return "<RefreshRate %sHz>" % self._value


class Resolution(IntegerSpecification, BaseSpecification):
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
        return "<Resolution %sp>" % self._value


class ScreenSize(DecimalSpecification, BaseSpecification):
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
        return "<ScreenSize %s\">" % self._value
