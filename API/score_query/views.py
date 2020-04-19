from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404, HttpResponseBadRequest, HttpResponse
from .serializers import *
from .models import *
from course_query.models import Student


class ScoreList(APIView):
    @staticmethod
    def get(request):
        """
        参数1:学生学号 e.g. 17373333
        参数2：学期 e.g.2020_Spring
        参数数量错误、不给参数均返回400错误
        参数错误，返回404错误
        例:127.0.0.1/score?student_id=11111111&semester=2020_Spring
        获得学号为11111111，2020春季学期的成绩
        """
        req = request.query_params.dict()
        result = Score.objects.all()
        if (len(req) > 0) and (len(req) < 3):
            for key, value in req.items():
                if key == 'semester':
                    result = result.filter(semester=value)
                elif key == 'student_id':
                    result = result.filter(student_id=value)
                else:
                    raise Http404
        else:
            return HttpResponseBadRequest()
        score_serializer = ScoreSerializer(result, many=True)
        return Response(score_serializer.data)

    @staticmethod
    def post(request):
        """
        根据post的json数据将数据插入数据库；
        格式：{student_id:(id), semester:(sm), info:[[课程名称1，学分1...],[课程名称2，学分2...]}
        """
        req = request.data
        semester = req['semester']
        # 找不到这个学生肯定有问题
        try:
            student = Student.objects.get(id=req['student_id'])
        except Student.DoesNotExist:
            raise Http404
        for key in req['info']:
            if len(key) == 4:
                bid = key[0]
                course_name = key[1]
                credit = key[2]
                score = key[3]
                try:
                    Score.objects.get(bid=bid)
                except Score.DoesNotExist:
                    new_score = Score(student_id=student, semester=semester, course_name=course_name
                                      , bid=bid, credit=credit, score=score)
                    new_score.save()
            else:
                return HttpResponseBadRequest()
        return HttpResponse(status=201)
