from django.db import models
from ..specifications.


class SpecificationType(models.Model):
    name = models.CharField("name", max_length=32)

    def get_specification_model(self):


    def __str__(self):
        return "<SpecificationAlternativeName {self.name}>".format(self=self)


class AlternativeSpecificationName(models.Model):
    name = models.CharField("name", max_length=32)
    specification_type = models.ForeignKey(
        "products.SpecificationType",
        related_name="alternative_names",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return "<SpecificationAlternativeName {self.name}>".format(self=self)
