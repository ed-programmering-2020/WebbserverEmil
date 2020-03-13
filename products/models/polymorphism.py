from django.contrib.contenttypes.models import ContentType
from django.db import models


class PolymorphicManager(models.Manager):
    def get_queryset(self):
        model_instances = super().get_queryset()

        first_model_instance = model_instances.first()
        if not first_model_instance:
            return model_instances

        inherited_model = first_model_instance.get_model()

        inherited_model_instances = inherited_model.objects.none()
        for model_instance in model_instances:
            inherited_model_instance = inherited_model.objects.get(id=model_instance.id)
            inherited_model_instances |= inherited_model_instance

        return inherited_model_instances


class PolymorphicModel(models.Model):
    content_type = models.ForeignKey(ContentType, editable=False, on_delete=models.SET_NULL, null=True)
    inherited_objects = PolymorphicManager()

    @classmethod
    def polymorphic_create(cls, **kwargs):
        model_name = cls.__name__

        print(model_name)

        # Create/get content type
        try:
            content_type = ContentType.objects.get(app_label="products", model=model_name)
        except ContentType.DoesNotExist:
            content_type = ContentType.objects.create(app_label="products", model=model_name)

        return cls.objects.create(content_type=content_type, **kwargs)

    def get_model(self):
        content_type = self.content_type

        if content_type:
            return content_type.model_class()

        return None

    def __hash__(self):
        return hash(self.id)


class ModelType(models.Model):
    name = models.CharField("name", max_length=32)

    class Meta:
        abstract = True


class AlternativeModelName(models.Model):
    name = models.CharField("name", max_length=64)
    host = models.ForeignKey("products.Website", null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True
