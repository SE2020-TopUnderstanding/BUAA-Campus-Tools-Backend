from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from course_query.models import Student
from .models import *




class query_classroom(APIView):
    def get(self, request, format=None):
        """
        输入：校区，日期，第几节到第几节，返回：教学楼，教室
        参数1:校区 e.g. 新主楼
        参数2：日期 e.g. 2020-4-18
        参数3：第几节到第几节 e.g. 1,2,3,
        例:http://127.0.0.1:8000/classroom/?campus=新主楼&date=2020-4-18&section=1,2,3,
        返回:登录状态
        """
        req = request.query_params.dict()
        campus = req["campus"]
        date = req["date"]
        section = req["section"]
        #调用爬虫取得
        content = {}
        re = Classroom_t.objects.filter(campus=campus, date=date,
                                        section__contains=section)
        tb_re = re.values("teaching_building").distinct()

        for i in tb_re:
            cr_re = re.filter(teaching_building=i["teaching_building"]).values("classroom").distinct()
            content.update({i["teaching_building"]:cr_re})

        return Response(content)

    def post(self, request, format=None):#
        content = {"state":"未定义"}
        return Response(content)