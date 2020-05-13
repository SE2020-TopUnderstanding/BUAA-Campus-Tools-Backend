from rest_framework import serializers
from .models import Course, Student, StudentCourse, TeacherCourse, Teacher


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
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
    course_name = serializers.CharField(source='course_id.name')
    teacher_name = serializers.CharField(source='teacher_id.name')

    class Meta:
        model = TeacherCourse
        fields = ('course_name', 'teacher_name')
