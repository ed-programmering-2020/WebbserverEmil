from django.db import models


class Feedback(models.Model):
    message = models.CharField('message', max_length=128, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "<Feedback %s>" % self.message


class CategorySurveyAnswer(models.Model):
    answer = models.CharField('message', max_length=128)
    category = models.CharField('category', max_length=64)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<{self.category}SurveyAnswer {self.answer}>".format(self=self)


class Paragraph(models.Model):
    text = models.CharField("text", max_length=2048)
    newsletter = models.ForeignKey("content.Newsletter", related_name="paragraphs", on_delete=models.CASCADE)


class Newsletter(models.Model):
    title = models.CharField("title", max_length=256)
    author = models.CharField("author", max_length=128)
    creation_date = models.DateField(auto_now=True)
