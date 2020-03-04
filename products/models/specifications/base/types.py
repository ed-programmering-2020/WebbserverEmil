from django.db import models
from bs4 import BeautifulSoup
import requests


class IntegerSpecification(models.Model):
    _value = models.IntegerField("value", null=True)

    class Meta:
        abstract = True


class DecimalSpecification(models.Model):
    _value = models.DecimalField("value", null=True, max_digits=4, decimal_places=2)

    def process_value(self, value):
        value = value.split(" ")[0]
        value = ''.join(i for i in value if not i.isalpha())

        # Change commas to dots for later float parsing
        if "," in value:
            value = value.replace(",", ".")

        # return value as float if it is valid
        if value is not "":
            return float(value)
        else:
            return None

    class Meta:
        abstract = True


class CharSpecification(models.Model):
    _value = models.CharField("value", null=True, max_length=128)

    class Meta:
        abstract = True


class TypeSpecification(CharSpecification):
    def get_rank(self, value):
        for i, panel_types in enumerate(self.types):
            if type(panel_types) is not list:
                panel_types = [panel_types]

            for panel_type in panel_types:
                if panel_type in value:
                    return i
        return 0

    def is_better(self, value):
        return self.get_rank(self.value) > self.get_rank(value)

    def is_equal(self, value):
        return self.get_rank(self.value) == self.get_rank(value)

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

            print(name)

            try:
                specification = model.objects.get(name=name)
                specification.benchmark_score = score
                specification.save()
            except model.DoesNotExist:
                model.objects.polymorphic_create(name=name, score=score)

    class Meta:
        abstract = True
