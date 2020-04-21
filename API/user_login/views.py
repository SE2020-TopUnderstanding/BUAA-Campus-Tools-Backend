from .LoginRequest.loginJudge import *
from rest_framework.response import Response
from rest_framework.views import APIView
from course_query.models import Student

class login(APIView):
    def get(self, request, format=None):
        content = Student.objects.all().values("usr_name","usr_password")
        
        return Response(content)


    def post(self, request, format=None):
        """
        输入：用户名，用户密码，输出：登录状态（1代表成功，2代表无该账号，3代表密码错误）
        参数1:用户名 e.g. mushan，用户密码 e.g. h1010
        例:http --form POST http://127.0.0.1:8000/login/ usr_name="mushan" usr_password="h1010"
        返回:登录状态
        0 -> failed, username or password is wrong
        -1 -> failed, request timeout
        -2 -> failed, unknown exception
        """
        
        usr_name = request.data["usr_name"]
        usr_password = request.data["usr_password"]
        ans = getStudentInfo(usr_name,usr_password)
        
        state = 1
        content = {}
        student_id = ""
        if ans == 0:
            state = 0
        elif ans == -1:
            state = -1
        elif ans == -2:
            state = -2
        else:
            student_id = str(ans[0])
            name = ans[2]
            grade = ans[3]
            Student(usr_name=usr_name,usr_password=usr_password,id=student_id, name=name,grade=grade).save()
        
        print(Student.objects.filter(usr_name=usr_name).values("name","grade"))
        content = {"state":state, "student_id":student_id}#1代表成功，2代表无该账号，3代表密码错误
        return Response(content)
