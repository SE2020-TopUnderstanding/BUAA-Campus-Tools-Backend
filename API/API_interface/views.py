from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .serializers import *
from .models import *


class CourseList(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Student.objects.get(id=pk)
        except Student.DoesNotExist:
            # if cannot find, return 404
            raise Http404

    def get(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
