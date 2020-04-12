from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .serializers import *
from .models import *


class CourseList(APIView):
    @staticmethod
    def get(request):
        req = request.query_params.dict()
        result = StudentCourse.objects.all()
        if len(req) > 0:
            for key, value in req.items():
                if key == 'student_id':
                    result = result.filter(student_id__id=value)
                elif key == 'semester':
                    result = result.filter(course_id__semester=value)
                elif key == 'week':
                    if value != 'all':
                        value += ','
                        result = result.filter(course_id__week__icontains=value)
                elif key == 'format':
                    pass
                else:
                    raise Http404
            course_serializer = StudentCourseSerializer(result, many=True)
            return Response(course_serializer.data)
        else:
            raise Http404
