from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from .serializers import *
from .models import *
from course_query.models import Student
from request_queue.models import RequestRecord


def get_gpa(origin_score, credit):
    if origin_score == "不及格":
        return 0.0 * credit
    elif origin_score == "及格":
        return 1.7 * credit
    elif origin_score == "中等":
        return 2.8 * credit
    elif origin_score == "良好":
        return 3.5 * credit
    elif origin_score == "优秀":
        return 4.0 * credit
    else:
        return max(0, credit * (4.0 - 3 * (100 - int(origin_score)) ** 2 / 1600.0))


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
                    # 检查学生是否存在
                    try:
                        Student.objects.get(id=req['student_id'])
                    except Student.DoesNotExist:
                        message = "没有这个学生的信息"
                        return HttpResponse(message, status=401)
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
            return HttpResponse(message, status=401)
        # 爬虫的数据库插入请求
        if len(req) == 3:
            semester = req['semester']
            for key in req['info']:
                if len(key) == 6:
                    bid = key[0].replace(' ', '')
                    course_name = key[1]
                    credit = key[2].replace(' ', '')
                    label = key[3].replace(' ', '')
                    origin_score = key[4].replace(' ', '')
                    score = key[5].replace(' ', '')
                    try:
                        old_score = Score.objects.get(student_id=student, bid=bid)
                        if label == '补考':
                            old_score.label = label
                            if origin_score in ['优秀', '良好', '中等', '及格']:
                                old_score.origin_score = '及格'
                                old_score.score = 60
                            elif origin_score == '不及格':
                                old_score.origin_score = '不及格'
                                old_score.score = score
                            else:
                                if int(origin_score) >= 60:
                                    old_score.origin_score = str(max(60, int(int(origin_score) * 0.8)))
                                    old_score.score = str(max(60, int(int(origin_score) * 0.8)))
                                else:
                                    old_score.origin_score = origin_score
                                    old_score.score = score
                            old_score.semester = semester
                            old_score.save()
                        elif label == '重修':
                            old_score.label = label
                            old_score.origin_score = origin_score
                            old_score.score = score
                            old_score.semester = semester
                            old_score.save()
                    except Score.DoesNotExist:
                        new_score = Score(student_id=student, semester=semester, course_name=course_name
                                          , bid=bid, credit=credit, label=label, origin_score=origin_score, score=score)
                        new_score.save()
                else:
                    message = 'info里的元素个数错误，只能为6个'
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
        student_id = req['student_id']
        gpa_sum = 0.0
        credit_sum = 0.0
        try:
            Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            message = '没有这个学生'
            return HttpResponse(message, status=404)
        if len(req) == 1 and 'student_id' in req.keys():
            scores = Score.objects.filter(student_id=student_id)
            for score in scores:
                gpa_sum += get_gpa(score.origin_score, score.credit)
                credit_sum += score.credit
            if credit_sum == 0:
                return Response({'gpa': 0.0000})
            return Response({'gpa': gpa_sum / credit_sum})
        else:
            message = '您附加的参数名称有错误，只允许\'student_id\''
            return HttpResponse(message, status=400)


class AvgScoreCalculate(APIView):
    @staticmethod
    def get(request):
        req = request.query_params.dict()
        student_id = req['student_id']
        score_sum = 0.0
        credit_sum = 0.0
        try:
            Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            message = '没有这个学生'
            return HttpResponse(message, status=404)
        if len(req) == 1 and 'student_id' in req.keys():
            scores = Score.objects.filter(student_id=student_id)
            for score in scores:
                score_sum += score.score * score.credit
                credit_sum += score.credit
            if credit_sum == 0:
                return Response({'score': 0.00000})
            return Response({'score': score_sum / credit_sum})
        else:
            message = '您附加的参数名称有错误，只允许\'student_id\''
            return HttpResponse(message, status=400)
