from django.db import models
from bs4 import BeautifulSoup
import requests


class IntegerSpecification(models.Model):
    _value = models.IntegerField("value", null=True)

    class Meta:
        abstract = True


class DecimalSpecification(models.Model):
    _value = models.DecimalField("value", null=True, max_digits=5, decimal_places=5)

    class Meta:
        abstract = True


class CharSpecification(models.Model):
    _value = models.CharField("value", null=True, max_length=128)

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
    benchmark_score = models.IntegerField("benchmark", null=True)

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
