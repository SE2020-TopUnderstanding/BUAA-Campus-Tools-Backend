from django.db import models


class Teacher(models.Model):
    # teacher's id
    id = models.AutoField(primary_key=True)
    # teacher's name
    name = models.CharField(max_length=20)


class Course(models.Model):
    # course's bid, e.g.B2F020550
    bid = models.CharField(max_length=20)
    # the course's name, e.g. Software Engineering
    name = models.CharField(max_length=120)
    # 开课院系
    department = models.CharField(max_length=120)
    # 学分
    credit = models.FloatField(default=0.0)
    # 总学时
    hours = models.IntegerField(null=True)
    # 课程类别
    type = models.CharField(max_length=60)
    # many to many
    teacher_course = models.ManyToManyField(Teacher, through='TeacherCourse')


class PublicCourse(models.Model):
    name = models.CharField(max_length=90)


class Student(models.Model):
    objects = models.Manager()
    # student's id, e.g. 17373000
    id = models.CharField(max_length=50, primary_key=True)
    # 统一身份认证账号
    usr_name = models.CharField(max_length=30, unique=True)
    # 统一身份认证密码（密文）
    usr_password = models.CharField(max_length=50)
    # student's name, e.g kkk
    name = models.CharField(max_length=90)
    # student's grade e.g 4
    grade = models.IntegerField(default=-1)
    # manytomany
    student_course = models.ManyToManyField(Course, through='StudentCourse')
    course_evaluation = models.ManyToManyField(Course, through='CourseEvaluation', related_name='evaluated_course')


class StudentCourse(models.Model):
    # the course's time, e.g Tuesday 8, 9
    time = models.CharField(max_length=40)
    # the course's place, e.g. New Teaching Building F201
    place = models.CharField(max_length=100)
    # the course's start week ,e.g. 1-7,9-16
    week = models.CharField(max_length=80)
    # the course's semester, e.g 2019 Spring
    semester = models.CharField(max_length=30)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_teacher = models.ManyToManyField(Teacher, through='TeacherCourseSpecific')


class TeacherCourseSpecific(models.Model):
    student_course_id = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class TeacherCourse(models.Model):
    # 点赞数
    up = models.IntegerField(default=0)
    # 外键
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    # 点赞记录
    up_record = models.ManyToManyField(Student, through="TeacherEvaluationRecord")


# Beta阶段新功能
class CourseEvaluation(models.Model):
    # 课程评价分
    score = models.IntegerField(default=0)
    # 创建时间
    created_time = models.DateTimeField(auto_now_add=True)
    # 最后修改时间
    updated_time = models.DateTimeField(auto_now=True)
    # 点赞数
    up = models.IntegerField(default=0)
    # 被踩数
    down = models.IntegerField(default=0)
    # 评价内容
    evaluation = models.TextField()
    # 外键
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # 多对多关系
    up_record = models.ManyToManyField(Student, through='EvaluationUpRecord', related_name='up_evaluator')
    down_record = models.ManyToManyField(Student, through='EvaluationDownRecord', related_name='down_evaluator')


# 每条评价的点赞人
class EvaluationUpRecord(models.Model):
    # 外键
    evaluation = models.ForeignKey(CourseEvaluation, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


# 每条评价的加踩人
class EvaluationDownRecord(models.Model):
    # 外键
    evaluation = models.ForeignKey(CourseEvaluation, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


# 每位老师的点赞人
class TeacherEvaluationRecord(models.Model):
    # 外键
    teacher_course = models.ForeignKey(TeacherCourse, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
