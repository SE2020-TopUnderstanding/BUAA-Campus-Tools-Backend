from django.db import models


class VERSION(models.Model):
    objects = models.Manager()
    version_number = models.CharField(max_length=100, primary_key=True)
    update_date = models.CharField(max_length=100)
    announcement = models.TextField()
    download_address = models.CharField(max_length=100)
