from django.db import models


class Benchmark(models.Model):
    name = models.CharField("name", max_length=32)
    score = models.PositiveSmallIntegerField("score")
    spec_group = models.ForeignKey("products.SpecGroup", on_delete=models.SET_NULL)
