from django.db import models


class Website(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True)
    url = models.CharField('url', max_length=256, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "<Website {self.name}>".format(self=self)
