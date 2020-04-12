from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import *


@api_view(['get'])
def course_list(request, pk):
    try:
        result = Student.objects.get(id=pk)
    except Student.DoesNotExist:
        # if cannot find, return 404
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # response to 'GET' method
        serializer = StudentSerializer(result)
        return Response(serializer.data)
