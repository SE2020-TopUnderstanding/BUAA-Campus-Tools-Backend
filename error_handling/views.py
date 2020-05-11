from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from course_query.models import Student
from request_queue.views import delete_request


class DeleteStudent(APIView):
    @staticmethod
    def post(request):
        """
        根据学号删除某个学生的信息，且在消息队列中删除该学生的请求
        访问方法 POST http://127.0.0.1:8000/delete/
        参数usr_name, password
        如果数据库中无该学生，返回0
        如果数据库中密码不相同，返回-1
        如果成功删除返回1
        """
        req = request.data

        if len(req) != 2:
            print(len(req))
            return HttpResponse(status=500)
        if ("usr_name" not in req) | ("password" not in req):
            return HttpResponse(status=500)

        state = 0
        try:
            student = Student.objects.get(usr_name=req["usr_name"])
            if student.usr_password != req["password"]:
                state = -1
            else:
                student.delete()
                delete_request(student.usr_name, student.usr_password)
                print(student.usr_name)
                state = 1
        except Student.DoesNotExist:
            state = 0
        content = {"state": state}
        return Response(content)
