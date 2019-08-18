from django.db import models

# Create your models here.
class Page(models.Model):
    name=models.CharField(max_length=50)
    code=models.TextField()
    username=models.IntegerField(default=0)
    password=models.IntegerField(default=1)
    index=models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Website(models.Model):
    name=models.URLField()
    pages=models.ManyToManyField(Page)
    def __str__(self):
        return self.name