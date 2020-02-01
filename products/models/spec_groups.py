from django.contrib.contenttypes.models import ContentType
from difflib import SequenceMatcher
from django.db import models
import re


class SpecGroup(models.Model):
    name = models.CharField("name", max_length=32)
    rank_group = models.BooleanField("rank group", default=False)
    content_type = models.ForeignKey(ContentType, editable=False, on_delete=models.SET_NULL, null=True)

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

    def get_rank(self, value):
        for i, panel_type in enumerate(self.types):
            if panel_type in value:
                return i
        return 0

    def is_greater(self, first, second):
        return first > second

    def is_equal(self, first, second):
        return first == second

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
            super(SpecGroup, self).save(*args, **kwargs)

    def as_inherited_model(self):
        content_type = self.content_type
        model = content_type.model_class()
        return model.objects.first()

    def __str__(self):
        return "<SpecGroup %s>" % self.name


class Benchmark(models.Model):
    name = models.CharField("name", max_length=32)
    score = models.PositiveSmallIntegerField("score")
    spec_group = models.ForeignKey(SpecGroup, on_delete=models.SET_NULL, null=True)


class RefreshRate(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="RefreshRate", rank_group=True).save()

    def process_value(self, value):
        return self.process_number(value)


class PanelType(SpecGroup):
    types = ["ips", "va", "tn"]

    @classmethod
    def create(cls):
        return cls(name="PanelType", rank_group=True).save()

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
        return cls(name="Resolution", rank_group=True).save()

    def process_value(self, value):
        numbers = []
        for val in value.split("x"):
            val = val.replace(" ", "")
            if val.isdigit():
                numbers.append(int(val))

        print(value, numbers)
        if len(numbers) >= 2:
            return numbers[1]
        else:
            print(numbers)
            return numbers[0]


class StorageSize(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="StorageSize", rank_group=True).save()

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
        return cls(name="DiskType", rank_group=True).save()

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
        return cls(name="Memory", rank_group=True).save()

    def process_value(self, value):
        return self.process_number(value)


class GraphicsCard(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="GraphicsCard", rank_group=True).save()

    def process_value(self, value):
        return self.process_benchmark(value)


class Processor(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="Processor", rank_group=True).save()

    def process_value(self, value):
        return self.process_benchmark(value)


class BatteryTime(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="BatteryTime", rank_group=True).save()

    def process_value(self, value):
        return self.process_number(value)


class Weight(SpecGroup):
    @classmethod
    def create(cls):
        return cls(name="Weight", rank_group=True).save()

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
