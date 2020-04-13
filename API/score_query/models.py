from django.db import models
from API_interface.models import Student


class Score(models.Model):
    # student_id
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    # course's name
    course_name = models.CharField(max_length=20)
    # semester
    semester = models.CharField(max_length=20)
    # credit
    credit = models.FloatField(default=0)
    # score
    score = models.IntegerField(default=-1)
