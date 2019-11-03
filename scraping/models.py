from django.db import models
from localization.models import Country


class Website(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True)
    url = models.CharField('url', max_length=256, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)


class DataType(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True)


class SearchGroup(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    group_type = models.ForeignKey(DataType, on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)


class SearchList(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    search_group = models.ForeignKey(SearchGroup, on_delete=models.CASCADE)


class FetchInfo(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    search_list = models.ForeignKey(SearchList, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Fetch info'
        ordering = ['time']
