from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from course_query.models import Student
from request_queue.models import RequestRecord
from api_exception.exceptions import ArgumentError, UnAuthorizedError
from score_query.serializers import ScoreSerializer
from score_query.models import Score


def get_gpa(origin_score, credit):
    if origin_score == "不及格":
        return 0.0 * credit
    if origin_score == "及格":
        return 1.7 * credit
    if origin_score == "中等":
        return 2.8 * credit
    if origin_score == "良好":
        return 3.5 * credit
    if origin_score == "优秀":
        return 4.0 * credit
    return max(0, credit * (4.0 - 3 * (100 - int(origin_score)) ** 2 / 1600.0))


def insert_failed_course(old_score, semester, label, origin_score, score):
    old_score.label = label
    if origin_score in ['优秀', '良好', '中等', '及格']:
        old_score.origin_score = '及格'
        old_score.score = 60
    elif origin_score == '不及格':
        old_score.origin_score = '不及格'
        old_score.score = score
    elif origin_score == '通过':
        old_score.origin_score = '通过'
        old_score.score = 60
    elif origin_score == '不通过':
        old_score.origin_score = '不通过'
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


def insert_score(student, semester, key):
    if len(key) == 6:
        bid = key[0].replace(' ', '')
        course_name = key[1]
        credit = key[2].replace(' ', '')
        label = key[3].replace(' ', '')
        origin_score = key[4].replace(' ', '')
        score = key[5].replace(' ', '')
        if origin_score == '缓考':
            return HttpResponse(status=201)
        try:
            old_score = Score.objects.get(student_id=student, bid=bid)
            if label == '补考':
                insert_failed_course(old_score=old_score, semester=semester, label=label, origin_score=origin_score,
                                     score=score)
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
        return HttpResponse(status=201)
    raise ArgumentError()


class ScoreList(APIView):
    @staticmethod
    def get(request):
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
                        raise UnAuthorizedError()
                    result = result.filter(student_id=value)
                else:
                    raise ArgumentError()
        else:
            raise ArgumentError()
        score_serializer = ScoreSerializer(result, many=True)
        return Response(score_serializer.data)

    @staticmethod
    def post(request):
        req = request.data
        # 确保数据库中有此学生的记录
        try:
            student = Student.objects.get(id=req['student_id'])
        except Student.DoesNotExist:
            raise UnAuthorizedError()
        # 爬虫的数据库插入请求
        if len(req) == 3:
            semester = req['semester']
            for key in req['info']:
                insert_score(student=student, semester=semester, key=key)
            return HttpResponse(status=201)
        # 其他非法请求
        raise ArgumentError()


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
            raise UnAuthorizedError()
        if len(req) == 1 and 'student_id' in req.keys():
            scores = Score.objects.filter(student_id=student_id)
            for score in scores:
                if score.origin_score != '通过' and score.origin_score != '不通过':
                    gpa_sum += get_gpa(score.origin_score, score.credit)
                    credit_sum += score.credit
            if credit_sum == 0:
                return Response({'gpa': 0.0000})
            return Response({'gpa': gpa_sum / credit_sum})
        raise ArgumentError()


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
            raise UnAuthorizedError()
        if len(req) == 1 and 'student_id' in req.keys():
            scores = Score.objects.filter(student_id=student_id)
            for score in scores:
                score_sum += score.score * score.credit
                credit_sum += score.credit
            if credit_sum == 0:
                return Response({'score': 0.00000})
            return Response({'score': score_sum / credit_sum})
        raise ArgumentError()
