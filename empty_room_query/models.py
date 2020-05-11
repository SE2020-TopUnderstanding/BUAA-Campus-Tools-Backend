from django.db import models


class Classroom(models.Model):  # 空教室表
    objects = models.Manager()
    campus = models.CharField(max_length=100)  # 校区
    teaching_building = models.CharField(max_length=100)  # 教学楼
    classroom = models.CharField(max_length=100)  # 教室
    date = models.CharField(max_length=100)  # 日期
    section = models.CharField(max_length=100)  # 节数
