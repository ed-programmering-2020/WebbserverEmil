from django.db import models


class Feedback(models.Model):
    message = models.CharField('message', max_length=128, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "<Feedback %s>" % self.message
