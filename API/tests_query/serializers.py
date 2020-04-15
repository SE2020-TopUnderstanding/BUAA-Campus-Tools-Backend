from rest_framework import serializers
from .models import *


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTable
        exclude = ('student_id', 'id')
