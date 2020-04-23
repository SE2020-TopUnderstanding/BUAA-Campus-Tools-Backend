from django.db import models


# Create your models here.
class TimeInfo(models.Model):
    time = models.DateTimeField(auto_now=True)


class RequestRecord(models.Model):
    name = models.CharField(max_length=50)
    count = models.IntegerField(default=0)
