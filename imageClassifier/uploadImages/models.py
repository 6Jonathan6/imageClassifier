from django.db import models
from django.contrib.postgres.fields import JSONField 
# Create your models here.

class Image(models.Model):

    user = models.CharField(max_length=30)
    key = models.CharField(max_length=50)
    labels = JSONField()
    confidence = models.CharField(max_length=250)
    slug = models.SlugField(max_length=50)
    