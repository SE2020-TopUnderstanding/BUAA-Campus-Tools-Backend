from django.db import models


class CourseTable(models.Model):
    # user's id
    student_id = models.CharField(max_length=10)
    # the course's semester
    semester = models.CharField(max_length=30)
    # the course's name
    course_name = models.CharField(max_length=60)
    # the course's time
    course_time = models.CharField(max_length=20)
    # the course's teacher
    teacher = models.CharField(max_length=20)
    # the course's start week
    class_week_start = models.IntegerField(default=1)
    # the course's end week
    class_week_end = models.IntegerField(default=20)
