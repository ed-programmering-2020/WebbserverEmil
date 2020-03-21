from .base import BaseSpecification
from django.db import models
from decimal import Decimal
from bs4 import BeautifulSoup
import requests


class BenchmarkSpecification(BaseSpecification):
    _value = models.CharField("value", null=True, max_length=128)

    class Meta:
        abstract = True

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
        # Check if inherited
        if cls is BenchmarkSpecification:
            return

        benchmarks = cls.collect_benchmarks()
        amount_of_benchmarks = sum(1 for _ in benchmarks)
        for i, benchmark in enumerate(benchmarks):
            name, __ = benchmark
            score = Decimal(1 - (i / amount_of_benchmarks))  # Adjusts based on the amount of benchmarks

            # Get/Create specification instance with the benchmark
            try:
                specification = cls.objects.get(_value=name)
                specification.score = score
                specification.save()
            except cls.DoesNotExist:
                cls.create(_value=name, score=score)

    @staticmethod
    def collect_benchmarks():
        raise NotImplementedError
