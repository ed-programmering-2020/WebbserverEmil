from .base import BaseSpecification
from django.db import models
from bs4 import BeautifulSoup
import requests


class BenchmarkSpecification(BaseSpecification):
    _value = models.CharField("value", null=True, max_length=128)

    @property
    def value(self):
        if self._value is not None:
            return self._value.capitalize()
        return None

    @value.setter
    def value(self, value):
        # Remove special characters
        for character in [",", "(", ")"]:
            value.replace(character, "")

        self._value = value.lower()

    @staticmethod
    def get_soup(url):
        fp = requests.get(url)
        html_doc = fp.text
        return BeautifulSoup(html_doc, "html.parser")

    @classmethod
    def rank(cls):
        for model in BenchmarkSpecification.objects.inherited_models():
            benchmarks = model.collect_benchmarks()

            for i, benchmark in enumerate(benchmarks):
                name, __ = benchmark
                score = 1 - i / len(benchmarks)  # Adjusts based on the amount of benchmarks

                # Get/Create specification instance with the benchmark
                try:
                    specification = model.objects.get(_value=name)
                    specification.score = score
                    specification.save()
                except model.DoesNotExist:
                    model.create(_value=name, score=score)

    @staticmethod
    def collect_benchmarks():
        raise NotImplementedError
