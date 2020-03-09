from .base import BaseSpecification, TypeSpecification, IntegerSpecification, DecimalSpecification
import re


class PanelType(TypeSpecification, BaseSpecification):
    name = "Panel typ"
    types = [
        "tn",
        "va",
        ["ips", "retina"]
    ]

    @property
    def value(self):
        if self._value is not None:
            return self._value.capitalize()

        return None

    @value.setter
    def value(self, value):
        for panel_types in self.types:
            if type(panel_types) is not list:
                panel_types = [panel_types]

            for panel_type in panel_types:
                if panel_type in value:
                    self._value = panel_type
                    break

    def __str__(self):
        return "<PanelType %s>" % self._value


class RefreshRate(IntegerSpecification, BaseSpecification):
    name = "Uppdateringsfrekvens (Hz)"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.process_number(value)

    def __str__(self):
        return "<RefreshRate %sHz>" % self._value


class Resolution(IntegerSpecification, BaseSpecification):
    name = "Upplösning"

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
    name = "Skärmstorlek (tum)"

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
