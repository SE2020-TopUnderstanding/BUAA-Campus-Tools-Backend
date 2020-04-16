from django.db import models


class Classroom_t(models.Model):  # 空教室表
    objects = models.Manager()
    campus = models.CharField(max_length=30)  # 校区
    teaching_building = models.CharField(max_length=30)  # 教学楼
    classroom = models.CharField(max_length=30)  # 教室
    date = models.CharField(max_length=30)  # 日期
    section = models.CharField(max_length=30)  # 节数

