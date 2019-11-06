from django.db import models
from localization.models import Country


class Website(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True)
    url = models.CharField('url', max_length=256, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    has_run = models.BooleanField(default=False)
    
    def __str__(self):
        return "<Website %s>" % self.name


class DataType(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField('name', max_length=128, blank=True)
    
    def __str__(self):
        return "<DataType %s>" % self.name


class SearchGroup(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    group_type = models.ForeignKey(DataType, related_name="search_groups", on_delete=models.CASCADE)
    website = models.ForeignKey(Website, related_name="search_groups", on_delete=models.CASCADE)
    
    def __str__(self):
        return "<SearchGroup %s>" % self.id


class SearchList(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    search_group = models.ForeignKey(SearchGroup, related_name="search_lists", on_delete=models.CASCADE)
    
    def __str__(self):
        return "<SearchList %s>" % self.id


class FetchInfo(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    search_list = models.ForeignKey(SearchList, related_name="fetch_infos", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    tag_name = models.CharField('tag_name', max_length=32, blank=True)
    class_name = models.CharField('class_name', max_length=32, blank=True)
    id_name = models.CharField('id_name', max_length=32, blank=True)

    class Meta:
        verbose_name_plural = 'Fetch info'
        ordering = ['time']
        
    def __str__(self):
        return "<FetchInfo %s>" % self.id
