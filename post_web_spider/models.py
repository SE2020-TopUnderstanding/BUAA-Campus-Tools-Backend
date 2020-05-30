from django.db import models

from course_query.models import Student


class PostRecord(models.Model):
    objects = models.Manager()
    #具体功能
    name = models.CharField(max_length=50)
    #更新时间
    time = models.DateTimeField(auto_now_add=True)
    # 学生学号，可以为空
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)


class StudentError(models.Model):
    objects = models.Manager()
    number = models.IntegerField(default=0)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
