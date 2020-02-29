from django.contrib.contenttypes.models import ContentType
from django.db import models


class PolymorphicManager(models.Manager):
    def get_queryset(self):
        model_instances = super().get_queryset()

        first_model_instance = model_instances.first()
        if first_model_instance:
            inherited_model = first_model_instance.get_model()

            inherited_model_instances = inherited_model.objects.none()
            for model_instance in model_instances:
                inherited_model_instance = inherited_model.objects.get(id=model_instance.id)
                inherited_model_instances |= inherited_model_instance

            return inherited_model_instances
        else:
            return model_instances


class PolymorphicModel(models.Model):
    content_type = models.ForeignKey(ContentType, editable=False, on_delete=models.SET_NULL, null=True)
    inherited_objects = PolymorphicManager()

    def get_model(self):
        content_type = self.content_type
        model = content_type.model_class()
        return model


class ModelType(models.Model):
    name = models.CharField("name", max_length=32)

    class Meta:
        abstract = True


class AlternativeModelName(models.Model):
    name = models.CharField("name", max_length=64)
    host = models.ForeignKey("products.Website", null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True
