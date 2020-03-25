from .base import BaseSpecification
from django.db import models
from bs4 import BeautifulSoup
import requests


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
        # Check if inherited
        if cls is BenchmarkSpecification:
            return

        # Collect and save benchmarks
        benchmarks = cls.collect_benchmarks()
        for i, benchmark in enumerate(benchmarks):
            name, full_score = benchmark
            score = 1 - i / len(benchmarks)  # Adjusts based on the amount of benchmarks

            # Get/Create specification instance with the benchmark
            try:
                specification = cls.objects.get(_value=name)
                specification.score = score
                specification.full_score = full_score
                specification.save()
            except cls.DoesNotExist:
                cls.objects.create(_value=name, score=score, full_score=full_score)
