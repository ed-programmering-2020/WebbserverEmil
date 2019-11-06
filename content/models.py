from django.db import models


class InfoPanel(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True)
    is_first = models.BooleanField(default=False)
    
    def __str__(self):
        return "<InfoPanel %s>" % self.name
