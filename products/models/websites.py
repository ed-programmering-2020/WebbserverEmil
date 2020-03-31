from django.db import models


class Website(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('name', max_length=128)
    short_url = models.CharField("short url", max_length=64)
    url = models.CharField('url', max_length=256)
    description = models.CharField("description", max_length=4096, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "<Website {self.name}>".format(self=self)
