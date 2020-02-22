from django.contrib.contenttypes.models import ContentType
from django.db import models


class PolymorphicModel(models.Model):
    content_type = models.ForeignKey(ContentType, editable=False, on_delete=models.SET_NULL, null=True)

    def as_inherited_model(self):
        content_type = self.content_type
        model = content_type.model_class()
        return model.objects.first()

