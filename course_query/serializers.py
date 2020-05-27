from rest_framework import serializers
from .models import Course, Student, StudentCourse, TeacherCourse, Teacher, CourseEvaluation


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
    bid = serializers.CharField(source='course_id.bid')

    class Meta:
        model = StudentCourse
        exclude = ('student_id', 'course_id', 'id', 'course_teacher',)


class CourseEvaluationSerializerHome(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name')
    credit = serializers.CharField(source='course.credit')
    department = serializers.CharField(source='course.department')

    class Meta:
        model = CourseEvaluation
        fields = ('course_name', 'credit', 'score', 'department')


class TeacherCourseSerializer(serializers.ModelSerializer):
    bid = serializers.CharField(source='course_id.bid')
    course_name = serializers.CharField(source='course_id.name')
    credit = serializers.CharField(source='course_id.credit')
    department = serializers.CharField(source='course_id.department')
    teacher = serializers.CharField(source='teacher_id.name')

    class Meta:
        model = TeacherCourse
        fields = ('bid', 'course_name', 'teacher', 'credit', 'department')


class CourseEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEvaluation
        fields = ('id', 'student', 'score', 'updated_time', 'evaluation', 'up', 'down')


class TeacherEvaluationSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher_id.name')

    class Meta:
        model = TeacherCourse
        fields = ('id', 'teacher_name', 'up')
