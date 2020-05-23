from rest_framework.views import APIView
from rest_framework.response import Response

from api_exception.exceptions import ArgumentError, UnAuthorizedError
from course_query.models import Student
from request_queue.views import delete_request
from .models import PostRecord


class DeleteStudent(APIView):
    @staticmethod
    def post(request):
        """
        根据学号删除某个学生的信息，且在消息队列中删除该学生的请求
        访问方法 POST http://127.0.0.1:8000/spider/delete/
        参数usr_name, password
        如果数据库中无该学生，返回0
        如果数据库中密码不相同，返回-1
        如果成功删除返回1
        """
        req = request.data

        if (len(req) != 2) | ("usr_name" not in req) | ("password" not in req):
            raise ArgumentError()

        state = 0
        try:
            student = Student.objects.get(usr_name=req["usr_name"])
            if student.usr_password != req["password"]:
                state = -1
            else:
                student.delete()
                delete_request(student.usr_name, student.usr_password)
                state = 1
        except Student.DoesNotExist:
            state = 0
        content = {"state": state}
        return Response(content)


class UpdateTime(APIView):
    @staticmethod
    def get(request):
        """
        根据学号返回该学生的所有功能更新时间
        访问方法
        GET
        http://127.0.0.1:8000/spider/update/?student_id=17373349 某个学生的所有功能更新时间
        http://127.0.0.1:8000/spider/update/?calendar=1       校历
        http://127.0.0.1:8000/spider/update/?empty_room=1    空教室
        :param request:
        :return:
        """
        req = request.query_params.dict()

        if len(req) != 1:
            raise ArgumentError()

        content = {}
        if "student_id" in req:
            try:
                student = Student.objects.get(id=req["student_id"])
                content = PostRecord.objects.filter(student_id=student).values("name", "time")
            except Student.DoesNotExist:
                raise UnAuthorizedError
        elif ("calendar" in req) and(req["calendar"] == "1"):
            content = PostRecord.objects.filter(name="calendar").values("name", "time")
        elif ("empty_room" in req) and (req["empty_room"] == "1"):
            content = PostRecord.objects.filter(name="empty_room").values("name", "time")
        else:
            raise ArgumentError

        return Response(content)
