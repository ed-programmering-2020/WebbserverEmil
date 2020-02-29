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
        on_delete=models.SET_NULL
    )

    objects = models.Manager()

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
                letter = letter.lower()
                attribute_like_name += "_"

            attribute_like_name += letter

        return attribute_like_name

    @staticmethod
    def rank():
        sorted_specifications = defaultdict()

        # Sorting
        for specification in BaseSpecification.objects.all().iterator():
            if not specification.is_ranked:
                value = specification.value
                key = specification.__class__.__name__
                package = (specification.id, value)

                if key not in sorted_specifications:
                    sorted_specifications[key] = [[package]]
                else:
                    for i, stored_specification in enumerate(sorted_specifications[key]):
                        __, saved_value = stored_specification[0]

                        # Rank with value
                        if value > saved_value:
                            sorted_specifications[key].insert(i, [package])
                            break

                        elif value == saved_value:
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

    @staticmethod
    def get_specification_instances(specs_list):
        specifications = []
        for specs in specs_list:
            for spec in specs:
                key, value = spec

                print(key, value)

                # Create/get spec key
                try:
                    alternative_specification_name = AlternativeSpecificationName.objects.get(name__iexact=key)
                    print("bapp")

                    # Create/get if it belongs to spec group
                    specification_type = alternative_specification_name.specification_type
                    if specification_type:

                        # Get model and process value
                        specification_model = specification_type.get_specification_model()
                        temporary_model_instance = specification_model()
                        temporary_model_instance.value = value
                        processed_value = temporary_model_instance.value

                        try:
                            specification = specification_model.inherited_objects.get(_value=processed_value)
                        except specification_model.DoesNotExist:
                            specification = specification_model.objects.create(_value=processed_value, specification_type=specification_type)
                            specification.save()

                        specifications.append(specification)

                except AlternativeSpecificationName.DoesNotExist:
                    AlternativeSpecificationName.objects.create(name=key)
                    print("bopp")

        return specifications

    def process_number(self, value):
        first_value = value.split(" ")[0]
        value = re.sub("[^0-9]", "", first_value).replace(" ", "")
        return int(value)

    def process_text(self, value):
        value_lowercase = value.lower()
        value = re.sub('[^A-Za-z0-9 ]+', '', value_lowercase)
        return value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        raise NotImplementedError


class SpecificationType(ModelType):
    def get_model(self):
        model_instance = BaseSpecification.objects.filter(specification_type_id=self.id).first()
        return model_instance.get_model()

    def __str__(self):
        return "<SpecificationType {self.name}>".format(self=self)
