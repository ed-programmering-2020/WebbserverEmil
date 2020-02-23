from ..polymorphism import PolymorphicModel
from django.db import models
from bs4 import BeautifulSoup
import requests
import re


class BaseSpecification(PolymorphicModel):
    name = models.CharField("name", max_length=32)
    verbose_name = models.CharField("verbose name", max_length=32, null=True)
    score = models.DecimalField("score", max_digits=9, decimal_places=9, null=True)
    specification_type = models.ForeignKey(
        "products.SpecificationType",
        related_name="specifications",
        on_delete=models.SET_NULL
    )

    @property
    def value(self):
        raise NotImplementedError

    @value.setter
    def value(self, value):
        raise NotImplementedError

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


class IntegerSpecification(models.Model):
    _value = models.IntegerField("value")

    class Meta:
        abstract = True


class DecimalSpecification(models.Model):
    _value = models.DecimalField("value")

    class Meta:
        abstract = True


class CharSpecification(models.Model):
    _value = models.CharField("value", max_length=128)

    class Meta:
        abstract = True


class TypeSpecification(CharSpecification):
    def get_rank(self, value):
        for i, panel_type in enumerate(self.types):
            if panel_type in value:
                return i
        return 0

    def __gt__(self, other):
        return self.get_rank(self.value) > self.get_rank(other.value)

    def __eq__(self, other):
        return self.get_rank(self.value) == self.get_rank(other.value)

    class Meta:
        abstract = True


class BenchmarkSpecification(CharSpecification):
    benchmark_score = models.IntegerField("benchmark")

    @staticmethod
    def get_soup(url):
        fp = requests.get(url)
        html_doc = fp.text
        return BeautifulSoup(html_doc, "html.parser")

    @staticmethod
    def collect_benchmarks():
        raise NotImplementedError

    @staticmethod
    def save_benchmarks(benchmarks, model):
        for i, benchmark in enumerate(benchmarks):
            name, __ = benchmark
            score = len(benchmarks) - i

            try:
                specification = model.objects.get(name=name)
                specification.benchmark_score = score
                specification.save()
            except model.DoesNotExist:
                model.objects.create(name=name, score=score)

    class Meta:
        abstract = True
