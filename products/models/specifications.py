# from .polymorphism import PolymorphicModel
from django.db import models
import re

"""
class BaseSpecification(PolymorphicModel):
    name = models.CharField("name", max_length=32)
    verbose_name = models.CharField("verbose name", max_length=32, null=True)
    score = models.DecimalField("score", max_digits=9, decimal_places=9, null=True)

    def process_number(self, value):
        value = value.split(" ")[0]
        value = re.sub("[^0-9]", "", value)
        value = value.replace(" ", "")
        return int(value)

    def process_text(self, value):
        value = value.lower()
        value = re.sub('[^A-Za-z0-9 ]+', '', value)
        return value

    def process_benchmark(self, value):
        text = value.lower()
        benchmarks = Benchmark.objects.filter(name__contains=text)
        if benchmarks.count() != 0:
            benchmark = benchmarks.first()
        else:
            top_likeness = 0
            benchmark = None
            for b in Benchmark.objects.all():
                likeness = SequenceMatcher(None, text, b.name).ratio()
                if likeness > top_likeness:
                    top_likeness = likeness
                    benchmark = b

        if benchmark:
            return benchmark.score
        else:
            return 0

    def is_greater(self, first, second):
        return first > second

    def is_equal(self, first, second):
        return first == second

    def as_inherited_model(self):
        content_type = self.content_type
        model = content_type.model_class()
        return model.objects.first()


class SpecificationAlternativeName(models.Model):
    name = models.CharField("name", max_length=32)
    specification = models.ForeignKey("products.BaseSpecification",
                                      related_name="alternative_names",
                                      on_delete=models.CASCADE)


class RefreshRate(BaseSpecification):
    def process_value(self, value):
        return self.process_number(value)

    def display_value(self, value):
        return "%s Hz" % value


class PanelType(BaseSpecification):
    types = ["ips", "va", "tn"]

    def process_value(self, value):
        return self.process_text(value)

    def get_rank(self, value):
        for i, panel_type in enumerate(self.types):
            if panel_type in value:
                return i
        return 0

    def is_greater(self, first, second):
        first, second = self.get_rank(first), self.get_rank(second)
        return first > second

    def is_equal(self, first, second):
        first, second = self.get_rank(first), self.get_rank(second)
        return first == second

    def display_value(self, value):
        return value.capitalize()


class Resolution(BaseSpecification):
    def process_value(self, value):
        numbers = re.findall(r'\d+', value)
        if len(numbers) >= 2:
            return int(numbers[1])
        elif len(numbers) == 1:
            return int(numbers[0])
        else:
            return 0

    def display_value(self, value):
        return "%sp" % value


class StorageSize(BaseSpecification):
    def process_value(self, value):
        value.lower()
        number = int(value.split(" ")[0])

        if "tb" in value:
            number *= 1024

        return number

    def display_value(self, value):
        if value >= 1024:
            to_display = "%s Tb" % round(value / 1024, 1)
        else:
            to_display = "%s Gb" % value

        return to_display


class DiskType(BaseSpecification):
    types = ["ssd", "hdd", "emmc"]

    def process_value(self, value):
        return self.process_text(value)

    def is_greater(self, first, second):
        first, second = self.get_rank(first), self.get_rank(second)
        return first > second

    def is_equal(self, first, second):
        first, second = self.get_rank(first), self.get_rank(second)
        return first == second

    def display_value(self, value):
        return value.capitalize()


class Memory(BaseSpecification):
    def process_value(self, value):
        return self.process_number(value)

    def display_value(self, value):
        return "%s Gb" % value


class GraphicsCard(BaseSpecification):
    def process_value(self, value):
        return self.process_benchmark(value)

    def display_value(self, value):
        return value


class Processor(BaseSpecification):
    def process_value(self, value):
        return self.process_benchmark(value)

    def display_value(self, value):
        return value


class BatteryTime(BaseSpecification):
    def process_value(self, value):
        return self.process_number(value)

    def display_value(self, value):
        return value


class Weight(BaseSpecification):
    def process_value(self, value):
        number = self.process_number(value)
        if " g" in value:
            number = number / 1000
        return number

    def is_greater(self, first, second):
        return first < second

    def display_value(self, value):
        return "%s kg" % value


class ScreenSize(BaseSpecification):
    def process_value(self, value):
        value = value.split(" ")[0]
        value = ''.join(i for i in value if not i.isalpha())
        value = value.split('"')[0]

        return float(value)

    def display_value(self, value):
        return '%s"' % value
"""


