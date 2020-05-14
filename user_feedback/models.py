from django.db import models
from course_query.models import Student


class Feedback(models.Model):
    objects = models.Manager()
    #插入日期
    date = models.DateTimeField(auto_now_add=True)
    #反馈类别
    kind = models.CharField(max_length=100)
    #具体内容
    content = models.TextField()
    #学生id
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
