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
    # many to many
    teacher_course = models.ManyToManyField(Teacher, through='TeacherCourse')


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
    course_evaluation = models.ManyToManyField(Course, through='CourseEvaluation')


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
    # 老师被点赞数
    up = models.IntegerField(default=0)

    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)


# Beta阶段新功能
class CourseEvaluation(models.Model):
    # 课程评价分
    score = models.IntegerField(default=0)
    # 楼层数
    floor = models.IntegerField(default=1)
    # 点赞数
    up = models.IntegerField(default=0)
    # 被踩数
    down = models.IntegerField(default=0)
    # 评价内容
    evaluation = models.TextField()
    # 外键
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
