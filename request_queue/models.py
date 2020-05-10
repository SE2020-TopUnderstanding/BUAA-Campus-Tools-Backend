from django.db import models


# Create your models here.
class TimeInfo(models.Model):
    time = models.DateTimeField(auto_now=True)


class RequestRecord(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50, primary_key=True)
    count = models.IntegerField(default=0)
