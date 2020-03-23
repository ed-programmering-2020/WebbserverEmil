"""This module contains all models necessary to maintain polymorphic models, inside this project, such as categories"""

from django.contrib.contenttypes.models import ContentType
from django.db import models


class NoContentTypeError(Exception):
    pass


class AlternativeName(models.Model):
    name = models.CharField("name", max_length=64)
    host = models.ForeignKey("products.Website", null=True, on_delete=models.CASCADE)
    model_type = models.ForeignKey(ContentType, editable=False, on_delete=models.SET_NULL, null=True)


class PolymorphicManager(models.Manager):
    def create(self, *args, **kwargs):
        """Overridden create method to prevent creation without a content type"""

        if "content_type" not in kwargs:
            raise self.NoContentTypeError

        return super().create(*args, **kwargs)


class PolymorphicModel(models.Model):
    content_type = models.ForeignKey(ContentType, editable=False, on_delete=models.SET_NULL, null=True)
    objects = PolymorphicManager()

    class Meta:
        abstract = True

    @classmethod
    def create(cls, *args, **kwargs):
        """Creates a new instance with a corresponding content type"""

        model_name = cls.__name__
        content_type = ContentType.objects.get(app_label="products", model=model_name)
        return cls.objects.create(*args, content_type=content_type, **kwargs)

    @classmethod
    def get_model_with_name(cls, alternative_name, host=None):
        """Finds matching model with a alternative name"""

        # Get/create alternative name
        try:
            model_instances = AlternativeName.objects.filter(name__iexact=alternative_name)
        except AlternativeName.DoesNotExist:
            AlternativeName.objects.create(name=alternative_name, host=host)
            return None

        # Find a matching alternative name
        for instance in model_instances:
            model_type = instance.model_type
            if model_type is None:
                continue

            model_class = model_type.model_class()
            if isinstance(model_class, cls):
                return model_class

        return None
