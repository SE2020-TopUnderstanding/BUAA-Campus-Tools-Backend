from django.db import models

# Create your models here.
class TimeInfo(models.Model):
    time = models.DateTimeField(auto_now=True)