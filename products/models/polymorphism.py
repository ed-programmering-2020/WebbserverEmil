from django.contrib.contenttypes.models import ContentType
from django.db import models


class PolymorphicManager(models.Manager):
    def as_inherited_model(self, model):
        content_type = model.content_type
        model = content_type.model_class()
        return model.objects.first()

    def get_queryset(self):
        model = super().get_queryset()
        inherited_model = self.as_inherited_model(model)
        return inherited_model


class PolymorphicModel(models.Model):
    content_type = models.ForeignKey(ContentType, editable=False, on_delete=models.SET_NULL, null=True)
    objects = PolymorphicManager()
