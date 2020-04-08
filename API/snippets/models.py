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
    # the course's place
    place = models.CharField(max_length=20)
    # the course's start week
    class_week_start = models.IntegerField(default=1)
    # the course's end week
    class_week_end = models.IntegerField(default=20)


class ScoreTable(models.Model):
    # user's id
    student_id = models.CharField(max_length=10)
    # semester
    semester = models.CharField(max_length=30)
    # course_name
    course_name = models.CharField(max_length=60)
    # credit
    credit = models.FloatField(default=-1.0)
    # score
    score = models.IntegerField(default=-1)
    # if pass?
    passed = models.BooleanField(default=True)


class TestTimeTable(models.Model):
    # user's id
    student_id = models.CharField(max_length=10)
    # course_name
    course_name = models.CharField(max_length=30)
    # test_date
    test_date = models.CharField(max_length=15)
    # test_time
    test_time = models.CharField(max_length=10)
    # test_place
    test_place = models.CharField(max_length=20)
    # seat_id
    seat_id = models.IntegerField(default=-1)
