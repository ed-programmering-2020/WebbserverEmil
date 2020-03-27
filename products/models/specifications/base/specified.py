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
        self.raw_value = value

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
            value = specification.value.lower()
            for i, types in enumerate(specification.types):
                if type(types) is not list:
                    types = [types]

                for value_type in types:
                    value_type = value_type.lower()

                    if value_type in value:
                        specification.score = i / len(specification.types)
                        specification.save()
                        break

    @classmethod
    def find_existing(cls, value):
        value = value.lower()

        for spec_instance in cls.objects.all():
            raw_value = spec_instance.raw_value.lower()

            if raw_value in value or value in raw_value:
                return spec_instance

        return None
