from django.db import models

# Create your models here.
class Notice(models.Model):
    _id = models.IntegerField(primary_key=True)
    name = models.TextField()
    link = models.TextField()
    belt = models.CharField(max_length=20)
    date = models.CharField(max_length=15)