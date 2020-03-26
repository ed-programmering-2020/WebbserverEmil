"""This module contains all models necessary to maintain polymorphic models, inside this project, such as categories"""

from django.contrib.contenttypes.models import ContentType
from django.db import models


class AlternativeName(models.Model):
    name = models.CharField("name", max_length=64)
    model_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)


class PolymorphicModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_model_with_name(cls, alternative_name):
        """Finds matching model with a alternative name"""

        try:
            alternative_name_instance = AlternativeName.objects.get(name__iexact=alternative_name)
        except AlternativeName.DoesNotExist:
            AlternativeName.objects.create(name=alternative_name)
            return None

        model_type = alternative_name_instance.model_type
        if model_type is not None:
            return model_type.model_class()
        else:
            return None
