from rest_framework import serializers
from .models import Score


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('course_name', 'credit', 'origin_score')
