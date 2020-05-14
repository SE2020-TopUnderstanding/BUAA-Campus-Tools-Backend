from rest_framework.response import Response
from rest_framework.views import APIView

from api_exception.exceptions import ArgumentError, UnAuthorizedError
from course_query.models import Student
from .models import Feedback


class UserFeedback(APIView):
    @staticmethod
    def get(request):
        """
        管理员调用获得用户反馈信息
        http://127.0.0.1:8000/feedback/
        http://127.0.0.1:8000/feedback/?date=2020-05-14
        http://127.0.0.1:8000/feedback/?kind=bug
        无参数或参数插入日期或反馈类别
        返回结果:学生id，插入日期，反馈类别，具体内容
        :param request:
        :return:
        """
        req = request.query_params.dict()

        if (len(req) != 1) & (len(req) != 0):
            raise ArgumentError()

        result = []
        if "date" in req:
            result = Feedback.objects.filter(date__contains=req["date"])
        elif "kind" in req:
            result = Feedback.objects.filter(kind=req["kind"])
        elif len(req) == 0:
            result = Feedback.objects.all()
        else:
            raise ArgumentError()
        content = []
        for i in result:
            try:
                name = i.student_id.name
            except Student.DoesNotExist:
                raise UnAuthorizedError()
            content.append({"name": name, "date": i.date, "kind": i.kind, "content": i.content})
        return Response(content)

    @staticmethod
    def post(request):
        """
        前端调用插入用户反馈信息
        http://127.0.0.1:8000/feedback/
        参数:学生id，反馈类别，具体内容
        :param request:
        :return:
        """
        req = request.data
        if (len(req) != 3) | (("student_id" not in req) |
                              ("kind" not in req) | ("content" not in req)):
            raise ArgumentError()

        try:
            student = Student.objects.get(id=req['student_id'])
        except Student.DoesNotExist:
            raise UnAuthorizedError()

        Feedback(student_id=student, kind=req["kind"], content=req["content"]).save()

        return Response({"state": "成功"})
