from rest_framework import serializers
from .models import Course, Student, StudentCourse, TeacherCourse, Teacher


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
    teacher_course = TeacherSerializerLimited(source='course_teacher', many=True)

    class Meta:
        model = StudentCourse
        exclude = ('student_id', 'course_id', 'id', 'course_teacher',)


class TeacherCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherCourse
        fields = '__all__'
