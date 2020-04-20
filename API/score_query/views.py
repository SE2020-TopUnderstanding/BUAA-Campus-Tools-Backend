from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404, HttpResponseBadRequest, HttpResponse
from .serializers import *
from .models import *
from course_query.models import Student
import request_queue.views as req_module


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
        if len(req) == 2:
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
        # 确保数据库中有此学生的记录
        try:
            student = Student.objects.get(id=req['student_id'])
        except Student.DoesNotExist:
            raise Http404

        # 前端的更新请求
        if len(req) == 1:
            req_module.req_id += 1
            req_queue = req_module.req_queue
            pending_work = req_module.pending_work
            req_queue.put(
                {'req_id': req_module.req_id, 'usr_name': student.usr_name, 'password': student.usr_password,
                 'req_type': "g"})
            pending_work.append(req_module.req_id)
            return Response([{'id': req_module.req_id}])

        # 爬虫的数据库插入请求
        elif len(req) == 3:
            semester = req['semester']
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

        # 其他非法请求
        else:
            return HttpResponse(status=400)
