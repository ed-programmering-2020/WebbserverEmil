from .base import BaseSpecification
from django.db import models


class SpecifiedSpecification(BaseSpecification):
    _value = models.CharField("value", null=True, max_length=128)

    class Meta:
        abstract = True

    @property
    def value(self):
        if self._value is not None:
            return self._value.capitalize()
        return None

    @value.setter
    def value(self, value):
        self._value = value

    @classmethod
    def rank(cls, *args):
        # Check if inherited
        if cls is SpecifiedSpecification:
            return

        for specification in cls.objects.all():
            # Check if specification contains a valid value
            if specification.value is None:
                specification.score = 0
                specification.save()
                continue

            # Get specification ranking
            for i, types in enumerate(specification.types):
                if type(types) is not list:
                    types = [types]

                for value_type in types:
                    value_to_compare = specification.value.lower()

                    if value_type in value_to_compare:
                        specification.score = i / len(specification.types)
                        specification.save()
                        continue

            # If no matching type was found
            specification.score = 0
            specification.save()
