from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .models import *

class login(APIView):
    def get(self, request, format=None):
        content = {"state":"未定义"}
        return Response(content)
    def post(self, request, format=None):
        usr_name = request.data["usr_name"]
        usr_password = request.data["usr_password"]
        #调用爬虫接口进行验证并取得下面的值
        major = "计算机科学与技术"
        grade = "2017"
        student_id = 17373349
        name = "bin"

        content = {"state":1}#1代表成功，2代表无该账号，3代表密码错误

        return Response(content)


#campus 校区
#teaching_building 教学楼
#classroom 教室
#date 日期
#section 节数
class query_classroom(APIView):#输入：校区，日期，第几节到第几节 返回：教学楼，教室
    def get(self, request, format=None):
        content = {"state":"未定义"}
        return Response(content)

    def post(self, request, format=None):#
        campus = request.data["campus"]
        date = request.data["date"]
        section = request.data["section"]
        #调用爬虫取得
        content = {}

        
        re = Classroom_t.objects.filter(campus=campus, date=date,
                                        section__contains=section)
        tb_re = re.values("teaching_building").distinct()

        for i in tb_re:
            cr_re = re.filter(teaching_building=i["teaching_building"]).values("classroom").distinct()
            content.update({i["teaching_building"]:cr_re})


        return Response(content)