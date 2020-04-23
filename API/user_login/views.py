from .LoginRequest.loginJudge import *
from rest_framework.response import Response
from rest_framework.views import APIView
from course_query.models import Student
from request_queue.models import RequestRecord
from django.http import Http404, HttpResponseBadRequest, HttpResponse
from request_queue.views import add_request

class login(APIView):
    def get(self, request, format=None):
        '''
        输入：密码
        http://127.0.0.1:8000/login/?password="123"
        返回：所有用户姓名和密码
        错误：500
        '''

        req = request.query_params.dict()
        content = {}
        if req["password"] == "123":
            content = Student.objects.all().values("usr_name","usr_password")
        else:
            return HttpResponse(status=500)
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
        没有提供参数，参数数量错误，返回400错误;
        参数错误，返回400错误;
        """
        
        try:#保存前端请求数据
            record = RequestRecord.objects.get(name="login")
            record.count = record.count+1
            record.save()
        except RequestRecord.DoesNotExist:
            RequestRecord(name="login", count=1).save()


        req = request.data

        
        if len(req) != 2:
            return Response(status=500,data={"state":"-2", "student_id":"", "name":""})
        if ("usr_name" not in req) | ("usr_password" not in req):
            return Response(status=500,data={"state":"-2", "student_id":"", "name":""})

        usr_name = request.data["usr_name"]
        usr_password = request.data["usr_password"]
        ans = getStudentInfo(usr_name,usr_password)
        
        state = 1
        content = {}
        name = ""
        student_id = ""
        if ans == 0:
            state = 0
            return Response(status=400,data={"state":state, "student_id":"", "name":""})
        elif ans == -1:
            state = -1
            return Response(status=500,data={"state":state, "student_id":"", "name":""})
        elif ans == -2:
            state = -2
            return Response(status=500,data={"state":state, "student_id":"", "name":""})
        else:
            student_id = str(ans[0])
            name = ans[2]
            grade = ans[3]
            Student(usr_name=usr_name,usr_password=usr_password,id=student_id, name=name,grade=grade).save()
            add_request('s', student_id)
            add_request('g', student_id)
            add_request('d', student_id)
        
        #print(Student.objects.filter(usr_name=usr_name).values("name","grade"))

        content = {"state":state, "student_id":student_id, "name":name}
        return Response(content)
