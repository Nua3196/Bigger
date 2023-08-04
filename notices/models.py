from django.db import models
from django.utils import timezone

# Create your models here.
class Notice(models.Model):
    _id = models.IntegerField(primary_key=True)
    name = models.TextField()
    link = models.TextField()
    belt = models.CharField(max_length=20)
    date = models.CharField(max_length=15)

class Update(models.Model):
    when = models.DateTimeField(default=timezone.now)
    how = models.CharField(max_length=20)