from ...polymorphism import PolymorphicModel
from django.db import models


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
            processed_spec = model_class()
            processed_spec.value = value

            # Find existing specification instance, else create a new specification
            for spec_instance in model_class.objects.all():
                if spec_instance.value is not None and spec_instance.is_equal(processed_spec.value):
                    specification = spec_instance
                    break
            else:
                specification = model_class.objects.create()
                specification.value = value
                specification.save()

            specification_instances.append(specification)

        return specification_instances

    def to_attribute_name(self):
        attribute_like_name = ""
        class_name = self.__class__.__name__
        for i, letter in enumerate(class_name):
            if not letter.islower() and i != 0:
                attribute_like_name += "_"

            attribute_like_name += letter

        return attribute_like_name.lower()

    def __str__(self):
        return "<BaseSpecification>"
