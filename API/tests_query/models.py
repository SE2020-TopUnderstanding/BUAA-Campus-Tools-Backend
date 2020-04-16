from django.db import models
from course_query.models import Student


class TestTable(models.Model):
    # student's id
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    # semester
    semester = models.CharField(max_length=20)
    # week
    week = models.IntegerField(default=0)
    # place
    place = models.CharField(max_length=20)
    # time
    time = models.CharField(max_length=20)
    # seat
    seat = models.IntegerField(default=0)
