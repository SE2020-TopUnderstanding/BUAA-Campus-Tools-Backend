from rest_framework import serializers
from .models import *


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = '__all__'
        exclude = ('name',)


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherSerializerLimited(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('name',)


class StudentCourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='course_id.name')

    class Meta:
        model = StudentCourse
        exclude = ('student_id', 'course_id', 'id',)
        depth = 1


class TeacherCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherCourse
        fields = '__all__'
