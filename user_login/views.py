from .login_request.login_judge import *
from rest_framework.response import Response
from rest_framework.views import APIView
from course_query.models import Student
from course_query.models import StudentCourse
from score_query.models import Score
from ddl_query.models import DDL_t
from request_queue.models import RequestRecord
from django.http import Http404, HttpResponseBadRequest, HttpResponse
from request_queue.views import add_request
from .login_request.password_utils import *

n_server = 4  # 爬虫服务器数量


class login(APIView):
    def get(self, request, format=None):
        '''
        输入：密码
        http://127.0.0.1:8000/login/?password=123
        返回：所有用户姓名和密码
        http://127.0.0.1:8000/login/?password=123&number=1
        返回：第几台服务器所拥有的用户
        错误：500
        '''
        req = request.query_params.dict()
        content = {}
        if req["password"] == "123":
            content = Student.objects.all().values("usr_name", "usr_password")
            if "number" in req:
                number = int(req["number"])
                length = content.count()  # 例 11个学生
                remainder = length % n_server  # 余数 3
                quotient = int(int(length) / int(n_server))  # 商  2      1-3 4-6 7-9 10-11
                start = quotient * (number - 1) + min(remainder, number - 1)
                end = quotient * number + min(remainder, number)
                return Response(content[start:end])
            return Response(content)
        else:
            return HttpResponse(status=500)

    def post(self, request, format=None):
        """
        输入：用户名，用户密码，输出：登录状态（1代表成功，2代表无该账号，3代表密码错误）
        参数1:用户名 e.g. mushan，用户密码 e.g. h1010
        例:http --form POST http://127.0.0.1:8000/login/ usr_name="mushan" usr_password="h1010"
        返回:登录状态
        0 -> request error when login the jiaowu web
        -1 -> login error, unknown, please refer to the log
        -2 -> login request status code is 2XX, but not 200
        -3 -> jump to unknown page
        -4 -> request exception, timeout or network error
        -5 -> login request status code is 4XX or 5XX
        -6 -> IP is banned from the buaa
        -7 -> usr_name is wrong or there is a CAPTCHA
        -8 -> password is wrong
        -9 -> usr_name or password is empty
        -10 -> account is locked
        没有提供参数，参数数量错误，返回500错误;
        参数错误，返回500错误;
        账号被锁返回402
        密码账号错误401
        服务器ip返回403
        """

        try:  # 保存前端请求数据
            record = RequestRecord.objects.get(name="login")
            record.count = record.count + 1
            record.save()
        except RequestRecord.DoesNotExist:
            RequestRecord(name="login", count=1).save()

        req = request.data

        if len(req) != 2:
            return Response(status=500, data={"state": "-3", "student_id": "", "name": ""})
        if ("usr_name" not in req) | ("usr_password" not in req):
            return Response(status=500, data={"state": "-3", "student_id": "", "name": ""})

        usr_name = request.data["usr_name"]
        usr_password = request.data["usr_password"]
        ans = get_student_info(usr_name, usr_password)

        state = 1
        content = {}
        name = ""
        student_id = ""
        if ans == 0:  # request error when login the jiaowu web
            state = 0
            return Response(status=500, data={"state": state, "student_id": "", "name": ""})
        elif ans == -1:  # login error, unknown, please refer to the log
            state = -1
            return Response(status=500, data={"state": state, "student_id": "", "name": ""})
        elif ans == -2:  # login request status code is 2XX, but not 200
            state = -2
            return Response(status=500, data={"state": state, "student_id": "", "name": ""})
        elif ans == -3:  # jump to unknown page
            state = -3
            return Response(status=500, data={"state": state, "student_id": "", "name": ""})
        elif ans == -4:  # request exception, timeout or network error
            state = -4
            return Response(status=500, data={"state": state, "student_id": "", "name": ""})
        elif ans == -5:  # login request status code is 4XX or 5XX
            state = -5
            return Response(status=500, data={"state": state, "student_id": "", "name": ""})
        elif ans == -6:  # IP is banned from the buaa
            state = -6
            return Response(status=403, data={"state": state, "student_id": "", "name": ""})
        elif ans == -7:  # usr_name is wrong or there is a CAPTCHA
            state = -7
            return Response(status=401, data={"state": state, "student_id": "", "name": ""})
        elif ans == -8:  # password is wrong
            state = -8
            return Response(status=401, data={"state": state, "student_id": "", "name": ""})
        elif ans == -9:  # usr_name or password is empty
            state = -9
            return Response(status=400, data={"state": state, "student_id": "", "name": ""})
        elif ans == -10:  # account is locked
            state = -10
            return Response(status=402, data={"state": state, "student_id": "", "name": ""})
        else:
            student_id = str(ans[0])
            pr = aescrypt(key, model, iv, encode_)
            student_id = pr.aesencrypt(student_id)
            name = ans[2]
            grade = ans[3]

            Student(usr_name=usr_name, usr_password=usr_password, id=student_id, name=name, grade=grade).save()
            if len(StudentCourse.objects.filter(student_id_id=student_id)) == 0:
                add_request('s', student_id)
            if len(Score.objects.filter(student_id_id=student_id)) == 0:
                add_request('g', student_id)
            if len(DDL_t.objects.filter(student_id_id=student_id)) == 0:
                add_request('d', student_id)

        # print(Student.objects.filter(usr_name=usr_name).values("name","grade"))

        content = {"state": state, "student_id": ans[0], "name": name}
        return Response(content)
