from django.db import models
from course_query.models import Student


class DDL(models.Model):
    objects = models.Manager()
    course = models.CharField(max_length=100)
    homework = models.CharField(max_length=100)
    ddl = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)


class SchoolYear(models.Model):
    objects = models.Manager()
    #学年
    school_year = models.CharField(max_length=50, primary_key=True)
    #第一学期开始日期
    first_semester = models.CharField(max_length=50)
    #寒假开始日期
    winter_semester = models.CharField(max_length=50)
    # 第二学期开始日期
    second_semester = models.CharField(max_length=50)
    # 第三学期开始日期
    third_semester = models.CharField(max_length=50)
    # 第三学期结束日期
    end_semester = models.CharField(max_length=50)


class SchoolCalendar(models.Model):
    objects = models.Manager()
    # 学期
    semester = models.CharField(max_length=50)
    # 日期
    date = models.CharField(max_length=50)
    # 节假日
    holiday = models.CharField(max_length=50)
    # 学年
    year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)