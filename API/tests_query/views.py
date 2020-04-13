from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .serializers import *
from .models import *


class TestList(APIView):
    # 参数1：student_id e.g.17373333
    # 参数2：semester e.g. 2020_Spring
    # 参数3: week e.g. 19
    # 不给参数，参数数量不正确均返回404错误
    # 例：127.0.0.1/tests?student_id=17373333&semester=2020_Spring&week=19
    # 查询学号为17373333 2020春季学期第19周课表
    @staticmethod
    def get(request):
        req = request.query_params.dict()
        result = TestTable.objects.all()
        if len(req) > 0:
            for key, value in req.items():
                if key == 'student_id':
                    result = result.filter(student_id=value)
                elif key == 'semester':
                    result = result.filter(semester=value)
                elif key == 'week':
                    result = result.filter(week=value)
                elif key == 'format':
                    pass
                else:
                    raise Http404
        else:
            raise Http404
        test_serializer = TestSerializer(result, many=True)
        return Response(test_serializer.data)
