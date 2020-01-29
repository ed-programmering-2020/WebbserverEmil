from django.db import models


class SpecGroup(models.Model):
    name = models.CharField('name', max_length=128, blank=True, null=True)

    def __str__(self):
        return "<SpecGroup %s>" % self.name


class SpecKey(models.Model):
    spec_group = models.ForeignKey(SpecGroup, related_name="spec_keys", on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey("products.Category", related_name="spec_keys", on_delete=models.CASCADE, blank=True, null=True)
    key = models.CharField('key', max_length=128, blank=True)

    def __str__(self):
        return "<SpecKey %s %s>" % (self.key, self.category)


class SpecValue(models.Model):
    products = models.ManyToManyField("products.Product", related_name="spec_values")
    spec_key = models.ForeignKey(SpecKey, related_name="spec_values", on_delete=models.CASCADE, blank=True, null=True)
    value = models.CharField('value', max_length=128, blank=True)

    def __str__(self):
        return "<SpecValue %s>" % self.value
