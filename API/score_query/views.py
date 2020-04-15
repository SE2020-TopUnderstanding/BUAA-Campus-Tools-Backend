from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .serializers import *
from .models import *


class ScoreList(APIView):
    # 参数1:学生学号 e.g. 17373333
    # 参数2：学期 e.g.2020_Spring
    # 参数类型错误、不给参数均返回404错误
    # 例:127.0.0.1/score?student_id=11111111&semester=2020_Spring
    # 获得学号为11111111，2020春季学期的成绩
    @staticmethod
    def get(request):
        req = request.query_params.dict()
        result = Score.objects.all()
        if len(req) > 0:
            for key, value in req.items():
                if key == 'semester':
                    result = result.filter(semester=value)
                elif key == 'student_id':
                    result = result.filter(student_id=value)
                elif key == 'format':
                    pass
                else:
                    raise Http404
        else:
            raise Http404
        score_serializer = ScoreSerializer(result, many=True)
        return Response(score_serializer.data)