from django.db import models

# Create your models here.
class Version_t(models.Model):
    objects = models.Manager()#版本号 更新日期 更新公告 下载地址
    version_number = models.CharField(max_length=100, primary_key=True)
    update_date = models.CharField(max_length=100)
    announcement = models.TextField()
    download_address = models.CharField(max_length=100)

    
