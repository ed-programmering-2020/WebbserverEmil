from .base import BaseSpecification
from collections import defaultdict
import time, re


class StandardSpecification(BaseSpecification):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        first_value = value.split(" ")[0]
        value = re.sub("[^0-9]", "", first_value).replace(" ", "")
        if value != "":
            self._value = int(value)

    def is_better(self, value):
        """This is needed because Django already uses the comparison operators"""
        return self.value > value

    def is_equal(self, value):
        """This is needed because Django already uses the comparison operators"""
        return self.value == value

    @classmethod
    def rank(cls, *args):
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

            # Sort specification into its belonging list
            for i, stored_specifications in enumerate(sorted_specifications[key]):
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

            # If the specification has the lowest value or list is empty
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
