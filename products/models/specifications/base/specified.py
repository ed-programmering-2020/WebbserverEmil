from .base import BaseSpecification
from django.db import models


class SpecifiedSpecification(BaseSpecification):
    raw_value = models.CharField("value", null=True, max_length=128)

    class Meta:
        abstract = True

    @property
    def value(self):
        return self.raw_value.upper()

    @value.setter
    def value(self, value):
        equivalent_value = SpecifiedSpecification.get_equivalent_value(value)
        if equivalent_value is not None:
            self.raw_value = equivalent_value["type"]

    @classmethod
    def get_equivalent_value(cls, value):
        value = value.lower()

        for i, types in enumerate(cls.types):
            if type(types) is not list:
                types = [types]

            for value_type in types:
                if value_type in value:
                    return {"type": value_type,
                            "index": i}

        return None

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
            equivalent_value = cls.get_equivalent_value(specification.value)
            if equivalent_value is not None:
                specification.score = equivalent_value["index"] / len(specification.types)
                specification.save()
