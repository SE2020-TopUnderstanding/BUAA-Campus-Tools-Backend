from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from .serializers import *
from .models import *
from course_query.models import Student
from request_queue.models import RequestRecord


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
        # 记录次数
        try:
            count = RequestRecord.objects.get(name='score')
        except RequestRecord.DoesNotExist:
            count = RequestRecord(name='score', count=0)
        count.count += 1
        count.save()
        # 查询
        req = request.query_params.dict()
        result = Score.objects.all()
        if len(req) == 2:
            for key, value in req.items():
                if key == 'semester':
                    result = result.filter(semester=value)
                elif key == 'student_id':
                    result = result.filter(student_id=value)
                else:
                    message = '您附加的参数名称有错误，只允许\'semester\',\'student_id\''
                    return HttpResponse(message, status=400)
        else:
            message = '您附加的参数个数有错误，只允许2个'
            return HttpResponse(message, status=400)
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
            message = '数据库中没有这个学生，服务器数据库可能有错误'
            return HttpResponse(message, status=500)
        # 爬虫的数据库插入请求
        if len(req) == 3:
            semester = req['semester']
            for key in req['info']:
                if len(key) == 4:
                    bid = key[0].replace(' ', '')
                    course_name = key[1]
                    credit = key[2].replace(' ', '')
                    score = key[3].replace(' ', '')
                    try:
                        Score.objects.get(student_id=student, bid=bid)
                    except Score.DoesNotExist:
                        new_score = Score(student_id=student, semester=semester, course_name=course_name
                                          , bid=bid, credit=credit, score=score)
                        new_score.save()
                else:
                    message = 'info里的元素个数错误，只能为4个'
                    return HttpResponse(message, status=400)
            return HttpResponse(status=201)

        # 其他非法请求
        else:
            message = '参数个数有错误，只能为3个'
            return HttpResponse(message, status=400)


class GPACalculate(APIView):
    @staticmethod
    def get(request):
        req = request.query_params.dict()
        gpa_sum = 0.0
        credit_sum = 0.0
        if len(req) == 1 and 'student_id' in req.keys():
            scores = Score.objects.filter(student_id=req['student_id'])
            for score in scores:
                gpa_sum += max(0, score.credit * (4.0 - 3 * (100 - score.score) ** 2 / 1600.0))
                credit_sum += score.credit
            return Response({'gpa': gpa_sum / credit_sum})
        else:
            message = '您附加的参数名称有错误，只允许\'student_id\''
            return HttpResponse(message, status=400)


class AvgScoreCalculate(APIView):
    @staticmethod
    def get(request):
        req = request.query_params.dict()
        score_sum = 0.0
        credit_sum = 0.0
        if len(req) == 1 and 'student_id' in req.keys():
            scores = Score.objects.filter(student_id=req['student_id'])
            for score in scores:
                score_sum += score.score * score.credit
                credit_sum += score.credit
            return Response({'score': score_sum / credit_sum})
        else:
            message = '您附加的参数名称有错误，只允许\'student_id\''
            return HttpResponse(message, status=400)
