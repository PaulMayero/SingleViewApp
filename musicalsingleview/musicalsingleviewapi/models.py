from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Musicalwork(models.Model):
    title = models.CharField(max_length=60)
    contributors = ArrayField(models.CharField(max_length=200))
    iswc = models.CharField(max_length=15)

    def __str__(self):
        return self.title
