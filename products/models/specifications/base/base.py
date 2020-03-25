from ...polymorphism import PolymorphicModel
from django.db import models
from decimal import Decimal


class BaseSpecification(PolymorphicModel):
    score = models.DecimalField("score", max_digits=10, decimal_places=9, null=True)

    class Meta:
        abstract = True

    @property
    def value(self):
        raise NotImplementedError

    @value.setter
    def value(self, value):
        raise NotImplementedError

    def to_attribute_name(self):
        attribute_like_name = ""
        class_name = self.__class__.__name__
        for i, letter in enumerate(class_name):
            if not letter.islower() and i != 0:
                attribute_like_name += "_"

            attribute_like_name += letter

        return attribute_like_name.lower()

    @staticmethod
    def rank():
        raise NotImplementedError

    @staticmethod
    def get_specification_instances(specifications):
        specification_instances = []

        for spec in specifications:
            key, value = spec

            # Check if the spec is a key value pair
            if len(spec) != 2:
                continue

            # Check for correlating model
            model_class = BaseSpecification.get_model_with_name(key)
            if model_class is None:
                continue

            # Process value for comparison
            temporary_specification = model_class()
            temporary_specification.value = value

            # Find existing specification instance, else create a new specification
            specification = model_class.find_existing(temporary_specification.raw_value)
            if specification is None:
                specification = temporary_specification
                specification.save()

            specification_instances.append(specification)

        return specification_instances

    @classmethod
    def find_existing(cls, value):
        if type(value) == Decimal:
            value = float(value)

        for spec_instance in cls.objects.all():
            raw_value = spec_instance.raw_value
            if type(raw_value) == Decimal:
                raw_value = float(raw_value)
            
            if raw_value == value:
                return spec_instance

        return None

    def __str__(self):
        return "<BaseSpecification>"
