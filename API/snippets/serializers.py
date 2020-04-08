from rest_framework import serializers
from snippets.models import CourseTable


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTable
        fields = ('student_id', 'semester', 'course_name', 'course_time', 'teacher', 'class_week_start', 'class_week_end')
