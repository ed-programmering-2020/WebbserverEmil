from ...polymorphism import PolymorphicModel, ModelType, AlternativeModelName
from collections import defaultdict
from django.db import models
import re


class AlternativeSpecificationName(AlternativeModelName):
    specification_type = models.ForeignKey(
        "products.SpecificationType",
        related_name="alternative_specification_names",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return "<AlternativeSpecificationName {self.name}>".format(self=self)


class BaseSpecification(PolymorphicModel):
    score = models.DecimalField("score", max_digits=9, decimal_places=9, null=True)
    is_ranked = models.BooleanField("is ranked", default=False)
    specification_type = models.ForeignKey(
        "products.SpecificationType",
        related_name="specifications",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    objects = models.Manager()

    to_rank = False

    @property
    def value(self):
        raise NotImplementedError

    @value.setter
    def value(self, value):
        raise NotImplementedError

    def get_attribute_like_name(self):
        attribute_like_name = ""
        class_name = self.__class__.__name__
        for i, letter in enumerate(class_name):
            if not letter.islower() and i != 0:
                attribute_like_name += "_"

            attribute_like_name += letter

        return attribute_like_name.lower()

    @staticmethod
    def rank():
        sorted_specifications = defaultdict()

        # Sorting
        for specification in BaseSpecification.objects.all().iterator():
            if not specification.is_ranked:
                model = specification.get_model()
                inherited_specification = model.objects.get(id=specification.id)

                key = inherited_specification.__class__.__name__
                value = inherited_specification.value

                if value is not None:
                    package = (inherited_specification.id, value)

                    if key not in sorted_specifications:
                        sorted_specifications[key] = [[package]]
                    else:
                        for i, stored_specification in enumerate(sorted_specifications[key]):
                            __, saved_value = stored_specification[0]

                            # Rank with value
                            if inherited_specification.is_better(saved_value):
                                sorted_specifications[key].insert(i, [package])
                                break

                            elif inherited_specification.is_equal(saved_value):
                                sorted_specifications[key][i].append(package)
                                break

                            elif i == (len(sorted_specifications[key]) - 1):
                                sorted_specifications[key].append([package])
                                break

        # Scoring
        scored_specifications = defaultdict()
        for key, values in sorted_specifications.items():
            values_length = len(values)

            for pos, value_list in enumerate(values):
                for id, value in value_list:
                    id = str(id)
                    value = pos / values_length

                    if id not in scored_specifications:
                        scored_specifications[id] = {key: value}
                    else:
                        scored_specifications[id][key] = value

        # Saving
        key_count = len(scored_specifications)
        for id, values in scored_specifications.items():
            specification = BaseSpecification.objects.get(id=id)

            score = 0
            for key, value in values.items():
                score += value / key_count

            specification.score = score
            specification.is_ranked = True
            specification.save()

    @classmethod
    def create_dummy(cls):
        if cls.objects.count() == 0:
            specification_type_name = cls.__name__

            # Create/get category product type
            try:
                specification_type = SpecificationType.objects.get(name=specification_type_name)
            except SpecificationType.DoesNotExist:
                specification_type = SpecificationType.objects.create(name=specification_type_name)

            # Create dummy category product
            cls.create(specification_type=specification_type)

    @staticmethod
    def get_specification_instances(specifications, host=None):
        specification_instances = []

        # Iterate through all specifications
        for spec in specifications:

            # Proceed if specification is valid
            if len(spec) == 2:
                key = spec[0]
                value = spec[1]

                # Get alternative specification name
                if host is not None:
                    alternative_specification_name = AlternativeSpecificationName.objects.filter(name__iexact=key).first()
                else:
                    alternative_specification_name = AlternativeSpecificationName.objects.filter(name__iexact=key, host=host).first()

                if alternative_specification_name is not None:
                    # Create/get specification if it belongs to specification type
                    specification_type = alternative_specification_name.specification_type

                    if specification_type:
                        # Get specification model
                        specification_model = specification_type.get_specification_model()

                        # Process value for comparison
                        processed_spec = specification()
                        processed_spec.value = value

                        # Find existing specification instance
                        for spec in specification_model.objects.all():
                            if spec.value == processed_spec.value:
                                specification = spec
                                break
                        else:
                            # Create new specification
                            specification = specification_model.create(specification_type=specification_type)
                            specification.value = value
                            specification.save()

                        # Add specification instance to a list
                        specification_instances.append(specification)
                else:
                    # Create new alternative specification name
                    AlternativeSpecificationName.objects.create(name=key, host=host)

        return specification_instances

    def process_number(self, value):
        first_value = value.split(" ")[0]
        value = re.sub("[^0-9]", "", first_value).replace(" ", "")
        if value != "":
            return int(value)
        else:
            return None

    def process_text(self, value):
        value_lowercase = value.lower()
        value = re.sub('[^A-Za-z0-9 ]+', '', value_lowercase)
        return value

    def is_better(self, value):
        return self.value > value

    def is_equal(self, value):
        return self.value == value

    def __str__(self):
        return "<BaseSpecification {self.score}>".format(self=self)


class SpecificationType(ModelType):
    def get_specification_model(self):
        model_instance = BaseSpecification.objects.filter(specification_type_id=self.id).first()
        return model_instance.get_model()

    def __str__(self):
        return "<SpecificationType {self.name}>".format(self=self)
