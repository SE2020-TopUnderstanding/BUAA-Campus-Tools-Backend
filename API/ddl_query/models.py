from django.db import models
from course_query.models import Student


class DDL_t(models.Model):
    objects = models.Manager()
    course = models.CharField(max_length=30)
    homework = models.CharField(max_length=30)
    dll = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
