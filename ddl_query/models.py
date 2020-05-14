from django.db import models
from course_query.models import Student


class DDL(models.Model):
    objects = models.Manager()
    course = models.CharField(max_length=100)
    homework = models.CharField(max_length=100)
    ddl = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)


class SchoolCalendar(models.Model):
    objects = models.Manager()
    #学期
    semester = models.CharField(max_length=50)
    #日期
    date = models.CharField(max_length=50)
    #节假日
    holiday = models.CharField(max_length=50)
