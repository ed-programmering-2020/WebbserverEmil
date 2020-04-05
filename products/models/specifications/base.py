from django.db import models
from bs4 import BeautifulSoup
import requests
import re


class BaseSpecification(models.Model):
    name = None

    score = models.DecimalField("score", max_digits=5, decimal_places=3, null=True)

    class Meta:
        abstract = True

    @classmethod
    def to_attribute_name(cls):
        attribute_like_name = ""
        for i, letter in enumerate(cls.__class__.__name__):
            if not letter.islower() and i != 0:
                attribute_like_name += "_"
            attribute_like_name += letter
        return attribute_like_name.lower()

    def __str__(self):
        return "<BaseSpecification>"


class BenchmarkSpecification(BaseSpecification):
    value = models.CharField("value", null=True, max_length=128)

    class Meta:
        abstract = True

    @property
    def formatted_value(self):
        return self.value.capitalize()

    @staticmethod
    def process_value(self, value):
        for character in [",", "(", ")"]:
            value = value.replace(character, "")
        return value.lower()

    @staticmethod
    def get_soup(url):
        fp = requests.get(url)
        html_doc = fp.text
        return BeautifulSoup(html_doc, "html.parser")

    @staticmethod
    def collect_benchmarks():
        raise NotImplementedError

    @classmethod
    def rank(cls):
        benchmarks = sorted(cls.collect_benchmarks(), key=lambda tup: tup[1])
        min_score, max_score = benchmarks[0][1], benchmarks[-1][1]
        for name, score in benchmarks:
            specification = cls.objects.get_or_create(value=name)
            specification.score = (score - min_score) / max_score * 5
            specification.save()


class SpecifiedSpecification(BaseSpecification):
    specified_values = None

    value = models.CharField("value", null=True, max_length=128)

    class Meta:
        abstract = True

    @property
    def formatted_value(self):
        return self.value.upper()

    def update_score(self):
        for i, values in enumerate(self.specified_values):
            for value in values:
                if self.value is value:
                    self.score = i
                    self.save()
                    return

    @staticmethod
    def process_value(value):
        for character in [",", "("]:
            if character in value:
                value = value.split(character)[0]
        return value.lower()


class DynamicSpecification(BaseSpecification):
    no_score = False
    reverse = False
    baseline_value = None

    class Meta:
        abstract = True

    def update_score(self):
        if self.no_score is True:
            return

        self.score = self.value / self.baseline_value
        if self.reverse is True:
            self.score = (self.score - 1) * -1 + 1

    @staticmethod
    def process_value(value):
        first_value = value.split(" ")[0].split(",")[0]
        value = re.sub("[^0-9]", "", first_value).replace(" ", "")
        return int(value)
