from django.db import models
from course_query.models import Student


class Score(models.Model):
    # student_id
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    # course's name
    course_name = models.CharField(max_length=120)
    # semester
    semester = models.CharField(max_length=30)
    # bid
    bid = models.CharField(max_length=15)
    # credit
    credit = models.FloatField(default=0)
    # origin_score
    origin_score = models.CharField(max_length=20)
    # score
    score = models.IntegerField(default=-1)
