from django.db import models

# Create your models here.
class Usr_t(models.Model):#用户表
    objects = models.Manager()
    usr_name = models.CharField(max_length=30, primary_key=True, unique=True)
    usr_password = models.CharField(max_length=30)
    major = models.CharField(max_length=30)#专业
    grade = models.CharField(max_length=30)#年级
    student_id = models.IntegerField()
    name = models.CharField(max_length=30)

class Classroom_t(models.Model):#空教室表
    objects = models.Manager()
    campus = models.CharField(max_length=30)#校区
    teaching_building = models.CharField(max_length=30)#教学楼
    classroom = models.CharField(max_length=30)#教室
    date = models.CharField(max_length=30)#日期
    section = models.CharField(max_length=30)#节数

