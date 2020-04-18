from rest_framework.response import Response
from rest_framework.views import APIView
from course_query.models import Student


class login(APIView):
    def get(self, request, format=None):
        """
        输入：用户名，用户密码，输出：登录状态（1代表成功，2代表无该账号，3代表密码错误）
        参数1:用户名 e.g. mushan，用户密码 e.g. h1010
        例:http --form GET http://127.0.0.1:8000/login/ usr_name="mushan" usr_password="h1010"
        返回:登录状态
        """
        usr_name = request.data["usr_name"]
        usr_password = request.data["usr_password"]
        #调用爬虫接口进行验证并取得下面的值
        major = "计算机科学与技术"
        grade = "2017"
        student_id = 17373349
        name = "bin"
        content = {"state":1}#1代表成功，2代表无该账号，3代表密码错误

        Student(id="1").save()
        print(Student.objects.filter(id="1").values("id"))
        return Response(content)

    def post(self, request, format=None):
        content = {"state":"未定义"}
        return Response(content)
