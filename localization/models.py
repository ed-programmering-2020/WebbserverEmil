from django.db import models


class Country(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=64, blank=True)
    currency = models.CharField('currency', max_length=64, blank=True)
    currency_short = models.CharField('currency_short', max_length=16, blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Countries'
