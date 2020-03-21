from .base import BaseSpecification
from django.db import models


class SpecifiedSpecification(BaseSpecification):
    _value = models.CharField("value", null=True, max_length=128)

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
        for model in SpecifiedSpecification.objects.inherited_models():
            for specification in model.objects.all():
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

    class Meta:
        abstract = True

