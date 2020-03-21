from .base import BaseSpecification
from collections import defaultdict
import time, re


class StandardSpecification(BaseSpecification):
    class Meta:
        abstract = True

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
        # Check if inherited
        if cls is StandardSpecification:
            return

        last = time.time()

        # Gather and sort all specifications
        sorted_specifications = []
        for specification in cls.objects.all().iterator():
            print(time.time() - last)

            # Get inherited model instance
            model = specification.content_type.model_class()
            inherited_specification = model.objects.get(id=specification.id)

            # Prepare sorting values
            value = inherited_specification.value
            package = (inherited_specification.id, value)

            # Skip if value property returns None
            if value is None:
                continue

            # Sort specification into its belonging list
            for i, stored_specifications in enumerate(sorted_specifications):
                # Get first specification from list
                specification_id, saved_value = stored_specifications[0]

                # If the specification is better than the stored specification
                if inherited_specification.is_better(saved_value, id=specification_id):
                    sorted_specifications.insert(i, [package])
                    break

                # If the specifications are equal
                if inherited_specification.is_equal(saved_value, id=specification_id):
                    sorted_specifications[i].append(package)
                    break

            # If the specification has the lowest value or list is empty
            else:
                sorted_specifications.append([package])

        print(sorted_specifications)

        # Save specification instances
        for i, values in enumerate(sorted_specifications):
            for specification_id, value in values:
                specification = cls.objects.get(id=specification_id)
                specification.score = i / len(sorted_specifications)
