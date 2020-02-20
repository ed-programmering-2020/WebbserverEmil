from django.contrib.contenttypes.models import ContentType
from difflib import SequenceMatcher
from django.db import models
import re


class SpecGroup(models.Model):
    name = models.CharField("name", max_length=32)
    verbose_name = models.CharField("verbose name", max_length=32, null=True)
    rank_group = models.BooleanField("rank group", default=False)
    content_type = models.ForeignKey(ContentType, editable=False, on_delete=models.SET_NULL, null=True)

    def process_number(self, value):
        value = value.split(" ")[0]
        value = re.sub("\D", "", value)
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

    def get_rank(self, value):
        for i, panel_type in enumerate(self.types):
            if panel_type in value:
                return i
        return 0

    def is_greater(self, first, second):
        return first > second

    def is_equal(self, first, second):
        return first == second

    def as_inherited_model(self):
        content_type = self.content_type
        model = content_type.model_class()
        return model.objects.first()

    def __str__(self):
        return "<SpecGroup %s>" % self.name


class Benchmark(models.Model):
    name = models.CharField("name", max_length=64)
    score = models.PositiveSmallIntegerField("score")
    spec_group = models.ForeignKey(SpecGroup, on_delete=models.SET_NULL, null=True)


class RefreshRate(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="RefreshRate", verbose_name="refresh rate", rank_group=True).save()

    def process_value(self, value):
        return self.process_number(value)


class PanelType(SpecGroup):
    types = ["ips", "va", "tn"]

    @classmethod
    def create(cls):
        return cls(name="PanelType", verbose="panel type", rank_group=True).save()

    def process_value(self, value):
        return self.process_text(value)

    def is_greater(self, first, second):
        first, second = self.get_rank(first), self.get_rank(second)
        return first > second

    def is_equal(self, first, second):
        first, second = self.get_rank(first), self.get_rank(second)
        return first == second


class Resolution(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="Resolution", verbose_name="resolution", rank_group=True).save()

    def process_value(self, value):
        numbers = re.findall(r'\d+', value)
        if len(numbers) >= 2:
            return int(numbers[1])
        elif len(numbers) == 1:
            return int(numbers[0])
        else:
            return 0


class StorageSize(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="StorageSize", verbose_name="storage size", rank_group=True).save()

    def process_value(self, value):
        value.lower()
        number = int(value.split(" ")[0])

        if "tb" in value:
            number *= 1024

        return number


class DiskType(SpecGroup):
    types = ["ssd", "hdd", "emmc"]

    @classmethod
    def create(cls):
        return cls(name="DiskType", verbose_name="disk type", rank_group=True).save()

    def process_value(self, value):
        return self.process_text(value)

    def is_greater(self, first, second):
        first, second = self.get_rank(first), self.get_rank(second)
        return first > second

    def is_equal(self, first, second):
        first, second = self.get_rank(first), self.get_rank(second)
        return first == second


class Memory(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="Memory", verbose_name="memory", rank_group=True).save()

    def process_value(self, value):
        return self.process_number(value)


class GraphicsCard(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="GraphicsCard", verbose_name="graphics card", rank_group=True).save()

    def process_value(self, value):
        return self.process_benchmark(value)


class Processor(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="Processor", verbose_name="processor", rank_group=True).save()

    def process_value(self, value):
        return self.process_benchmark(value)


class BatteryTime(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="BatteryTime", verbose_name="battery time", rank_group=True).save()

    def process_value(self, value):
        return self.process_number(value)


class Weight(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="Weight", verbose_name="weight", rank_group=True).save()

    def process_value(self, value):
        number = self.process_number(value)
        if " g" in value:
            number = number / 1000
        return number

    def is_greater(self, first, second):
        return first < second


class ScreenSize(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="ScreenSize", rank_group=False).save()

    def process_value(self, value):
        return self.process_number(value)

