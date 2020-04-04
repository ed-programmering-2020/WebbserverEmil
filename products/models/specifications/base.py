from django.db import models
from bs4 import BeautifulSoup
from decimal import Decimal
import requests
import re


class BaseSpecification(models.Model):
    score = models.DecimalField("score", max_digits=10, decimal_places=9, null=True)

    class Meta:
        abstract = True

    @property
    def value(self):
        return self.raw_value

    @value.setter
    def value(self, value):
        first_value = value.split(" ")[0].split(",")[0]
        value = re.sub("[^0-9]", "", first_value).replace(" ", "")
        if value is not "":
            self.raw_value = int(value)

    def is_better(self, raw_value):
        return self.raw_value > raw_value

    def is_equal(self, raw_value):
        return self.raw_value == raw_value

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

    @classmethod
    def rank(cls, *args):
        # Gather and sort all specifications
        sorted_specifications = []
        for specification in cls.objects.all().iterator():
            # Prepare sorting values
            value = specification.raw_value
            package = (specification.id, value)

            # Skip if value property returns None
            if value is None:
                continue

            # Sort specification into its belonging list
            for i, stored_specifications in enumerate(sorted_specifications):
                # Get first specification from list
                specification_id, saved_value = stored_specifications[0]

                # If the specification is better than the stored specification
                if specification.is_better(saved_value):
                    sorted_specifications.insert(i, [package])
                    break

                # If the specifications are equal
                if specification.is_equal(saved_value):
                    sorted_specifications[i].append(package)
                    break

            # If the specification has the lowest value or list is empty
            else:
                sorted_specifications.append([package])

        # Save specification instances
        for i, values in enumerate(sorted_specifications):
            for specification_id, value in values:
                specification = cls.objects.get(id=specification_id)
                specification.score = 1 - ((i + 1) / len(sorted_specifications))
                specification.save()


    @classmethod
    def to_attribute_name(cls):
        attribute_like_name = ""
        class_name = cls.__class__.__name__
        for i, letter in enumerate(class_name):
            if not letter.islower() and i != 0:
                attribute_like_name += "_"

            attribute_like_name += letter

        return attribute_like_name.lower()

    @staticmethod
    def get_specification_instances(specifications):
        specification_instances = []

        for spec in specifications:
            key, value = spec

            # Check if the spec is a key value pair
            if len(spec) != 2:
                continue

            # Check for correlating model
            mod = __import__("products")
            for component in ["models", key]:
                mod = getattr(mod, component)

            # Process value for comparison
            temporary_specification = mod()
            temporary_specification.value = value

            # Find existing specification instance, else create a new specification
            specification = mod.find_existing(temporary_specification.raw_value)
            if specification is None:
                specification = temporary_specification
                specification.save()

            specification_instances.append(specification)

        return specification_instances

    def __str__(self):
        return "<BaseSpecification>"


class BenchmarkSpecification(BaseSpecification):
    raw_value = models.CharField("value", null=True, max_length=128)
    full_score = models.PositiveSmallIntegerField(null=True)

    class Meta:
        abstract = True

    @property
    def value(self):
        if self.raw_value is not None:
            return self.raw_value.capitalize()
        return None

    @value.setter
    def value(self, value):
        # Remove special characters
        for character in [",", "(", ")"]:
            value = value.replace(character, "")

        self.raw_value = value.lower()

    @staticmethod
    def get_soup(url):
        fp = requests.get(url)
        html_doc = fp.text
        return BeautifulSoup(html_doc, "html.parser")

    @staticmethod
    def collect_benchmarks():
        raise NotImplementedError

    @classmethod
    def find_existing(cls, value):
        for spec_instance in cls.objects.all():
            if spec_instance.raw_value in value or value in spec_instance.raw_value:
                return spec_instance

        return None

    @classmethod
    def rank(cls):
        # Collect and save benchmarks
        benchmarks = cls.collect_benchmarks()
        for i, benchmark in enumerate(benchmarks):
            name, full_score = benchmark
            score = 1 - i / len(benchmarks)  # Adjusts based on the amount of benchmarks

            # Get/Create specification instance with the benchmark
            try:
                specification = cls.objects.get(raw_value=name)
                specification.score = score
                specification.full_score = full_score
                specification.save()
            except cls.DoesNotExist:
                cls.objects.create(raw_value=name, score=score, full_score=full_score)


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
