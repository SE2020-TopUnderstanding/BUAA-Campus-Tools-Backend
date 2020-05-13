from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse

from course_query.models import Student
from course_query.models import StudentCourse
from score_query.models import Score
from ddl_query.models import DDL
from request_queue.models import RequestRecord
from request_queue.views import add_request

from API.settings import PASSWORD_SPIDER
from .login_request.password_utils import Aescrypt, KEY, MODEL, IV, ENCODE_
from .login_request.login_judge import get_student_info

N_SERVER = 4  # 爬虫服务器数量


class Login(APIView):
    @staticmethod
    def get(request):
        """
        输入：密码
        http://127.0.0.1:8000/login/?password=123
        返回：所有用户姓名和密码
        http://127.0.0.1:8000/login/?password=123&number=1
        返回：第几台服务器所拥有的用户
        错误：462
        """
        req = request.query_params.dict()
        if req["password"] == PASSWORD_SPIDER:
            content = Student.objects.all().values("usr_name", "usr_password")
            if "number" in req:
                number = int(req["number"])
                length = content.count()  # 例 11个学生
                remainder = length % N_SERVER  # 余数 3
                quotient = int(int(length) / int(N_SERVER))  # 商  2      1-3 4-6 7-9 10-11
                start = quotient * (number - 1) + min(remainder, number - 1)
                end = quotient * number + min(remainder, number)
                return Response(content[start:end])
            return Response(content)
        return HttpResponse(status=462)

    @staticmethod
    def post(request):
        """
        输入：用户名，用户密码，输出：登录状态（1代表成功，2代表无该账号，3代表密码错误）
        参数1:用户名 e.g. mushan，用户密码 e.g. h1010
        例:http --form POST http://127.0.0.1:8000/login/ usr_name="mushan" usr_password="h1010"
        获取学生基本信息
        返回: [state, student_id, name]
        没有提供参数，参数数量错误，返回400错误;
        参数错误，返回400错误;
        密码账号错误401
        账号被锁返回460
        服务器ip返回461
        """

        try:  # 保存前端请求数据
            record = RequestRecord.objects.get(name="login")
            record.count = record.count + 1
            record.save()
        except RequestRecord.DoesNotExist:
            RequestRecord(name="login", count=1).save()

        req = request.data

        if len(req) != 2:
            return Response(status=400, data={"state": "-3", "student_id": "", "name": ""})
        if ("usr_name" not in req) | ("usr_password" not in req):
            return Response(status=400, data={"state": "-3", "student_id": "", "name": ""})

        usr_name = request.data["usr_name"]
        usr_password = request.data["usr_password"]
        ans = get_student_info(usr_name, usr_password)

        state = ans
        if (ans == 0) | (ans == -1) | (ans == -2)  | (ans == -3) | (ans == -4) | (ans == -5):
            return Response(status=500, data={"state": state, "student_id": "", "name": ""})

        if ans == -6:  # IP is banned from the buaa
            return Response(status=461, data={"state": state, "student_id": "", "name": ""})

        if (ans == -7) | (ans == -8):
            return Response(status=401, data={"state": state, "student_id": "", "name": ""})

        if ans == -9:
            return Response(status=400, data={"state": state, "student_id": "", "name": ""})

        if ans == -10:
            return Response(status=460, data={"state": state, "student_id": "", "name": ""})

        state = 1
        student_id = str(ans[0])
        password_d = Aescrypt(KEY, MODEL, IV, ENCODE_)
        student_id = password_d.aesencrypt(student_id)
        name = ans[2]
        grade = ans[3]

        Student(usr_name=usr_name, usr_password=usr_password, id=student_id, name=name, grade=grade).save()
        if len(StudentCourse.objects.filter(student_id_id=student_id)) == 0:
            add_request('s', student_id)
        if len(Score.objects.filter(student_id_id=student_id)) == 0:
            add_request('g', student_id)
        if len(DDL.objects.filter(student_id_id=student_id)) == 0:
            add_request('d', student_id)

        content = {"state": state, "student_id": ans[0], "name": name}
        return Response(content)
