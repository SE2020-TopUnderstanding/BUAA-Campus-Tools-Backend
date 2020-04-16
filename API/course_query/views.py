from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .serializers import *
from .models import *
from django.http import HttpResponseBadRequest


class CourseList(APIView):
    # 可使用的参数有：
    # student_id: 附带学生学号，查询指定学生课表
    # semester: 附带学年学期，查询指定学期课表
    # week: 附带周数，查询指定周的课表，若参数值为all,则查询该学期全部周的课表
    # 例：127.0.0.1/timetable?student_id=17333333&semester=2020_Spring&week=3
    # 查询学号为17373333 2020春季学期第三周课表
    # 没有提供参数，参数数量错误，返回400错误
    # 参数错误，返回404错误
    @staticmethod
    def get(request):
        req = request.query_params.dict()
        result = StudentCourse.objects.all()
        if (len(req) > 0) and (len(req) < 4):
            for key, value in req.items():
                if key == 'student_id':
                    result = result.filter(student_id__id=value)
                elif key == 'semester':
                    result = result.filter(course_id__semester=value)
                elif key == 'week':
                    if value != 'all':
                        value += ','
                        result = result.filter(course_id__week__icontains=value)
                else:
                    raise Http404
            course_serializer = StudentCourseSerializer(result, many=True)
            return Response(course_serializer.data)
        else:
            return HttpResponseBadRequest()
