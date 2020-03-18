from ...polymorphism import PolymorphicModel
from collections import defaultdict
from django.db import models
import re, time


class BaseSpecification(PolymorphicModel):
    score = models.DecimalField("score", max_digits=9, decimal_places=9, null=True)

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
        sorted_specifications = defaultdict(list)

        # Gather and sort all specifications
        last = time.time()
        for specification in BaseSpecification.objects.all().iterator():
            print(time.time() - last)

            # Get inherited model instance
            model = specification.content_type.model_class()
            inherited_specification = model.objects.get(id=specification.id)

            # Prepare sorting values
            key = model.__name__
            value = inherited_specification.value
            package = (inherited_specification.id, value)

            # Skip if value property returns None
            if value is None:
                continue

            # append to list if it is empty
            if len(sorted_specifications[key]) == 0:
                sorted_specifications[key].append([package])
                continue

            # Sort specification into its belonging list
            for i, stored_specifications in enumerate(sorted_specifications[key]):
                print(i)
                # Get first specification from list
                specification_id, saved_value = stored_specifications[0]

                # If the specification is better than the stored specification
                if inherited_specification.is_better(saved_value, id=specification_id):
                    sorted_specifications[key].insert(i, [package])
                    break

                # If the specifications are equal
                if inherited_specification.is_equal(saved_value, id=specification_id):
                    sorted_specifications[key][i].append(package)
                    break

            # If the specification has the lowest value
            else:
                sorted_specifications[key].append([package])

        print(sorted_specifications)

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
    def get_specification_instances(specifications, host=None):
        specification_instances = []

        for spec in specifications:
            # Check if the spec is a key value pair
            if len(spec) != 2:
                continue

            # Split spec into key value pair
            key, value = spec

            # Check for correlating model
            model_class = BaseSpecification.get_model_with_name(key, host)
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
                specification = model_class.create()
                specification.value = value
                specification.save()

            specification_instances.append(specification)

        return specification_instances

    def process_number(self, value):
        first_value = value.split(" ")[0]
        value = re.sub("[^0-9]", "", first_value).replace(" ", "")
        if value != "":
            return int(value)

        return None

    def process_text(self, value):
        value_lowercase = value.lower()
        value = re.sub('[^A-Za-z0-9 ]+', '', value_lowercase)
        return value

    def is_better(self, value, **kwargs):
        return self.value > value

    def is_equal(self, value, **kwargs):
        return self.value == value

    def __str__(self):
        return "<BaseSpecification {self.score}>".format(self=self)
