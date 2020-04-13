from django.db import models
from API_interface.models import Student


class Classroom_t(models.Model):#空教室表
    objects = models.Manager()
    campus = models.CharField(max_length=30)#校区
    teaching_building = models.CharField(max_length=30)#教学楼
    classroom = models.CharField(max_length=30)#教室
    date = models.CharField(max_length=30)#日期
    section = models.CharField(max_length=30)#节数

class Dll_t(models.Model):
    objects = models.Manager()
    course =  models.CharField(max_length=30)
    homework = models.CharField(max_length=30)
    dll = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)

