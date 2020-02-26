from django.contrib.contenttypes.models import ContentType
from django.db import models


class PolymorphicManager(models.Manager):
    def get_queryset(self):
        model_instance = super().get_queryset()

        inherited_model = model_instance.first().get_model()
        inherited_model_instance = inherited_model.objects.get(id=model_instance.id)
        return inherited_model_instance


class PolymorphicModel(models.Model):
    content_type = models.ForeignKey(ContentType, editable=False, on_delete=models.SET_NULL, null=True)
    objects = PolymorphicManager()

    def get_model(self):
        content_type = self.content_type
        model = content_type.model_class()
        return model


class ModelType(models.Model):
    name = models.CharField("name", max_length=32)

    def get_model(self):
        model_instance = self.model.objects.filter(specification_type=self).first()
        return model_instance.get_model()

    def __str__(self):
        return "<{self.model.__class__.__name__}Type {self.name}>".format(self=self)

    class Meta:
        abstract = True


class AlternativeModelName(models.Model):
    name = models.CharField("name", max_length=32)

    def __str__(self):
        return "<{self.model.__class__.__name__}AlternativeName {self.name}>".format(self=self)

    class Meta:
        abstract = True
