from rest_framework.response import Response
from rest_framework.views import APIView

from api_exception.exceptions import ArgumentError
from request_queue.models import RequestRecord
from post_web_spider.models import PostRecord
from .models import Classroom


class QueryClassroom(APIView):
    @staticmethod
    def get(request):
        """
        输入：校区，日期，第几节到第几节，返回：教学楼，教室
        参数1:校区 e.g. 新主楼
        参数2：日期 e.g. 2020-4-18
        参数3：第几节到第几节 e.g. 1,2,3,
        例:http://114.115.208.32:8000/classroom/?campus=学院路校区&date=2020-04-20&section=1, 2, 3,
        返回:查询结果
        没有提供参数，参数数量错误，返回400错误;
        参数错误，返回400错误;
        """

        try:  # 保存前端请求数据
            record = RequestRecord.objects.get(name="classroom")
            record.count = record.count + 1
            record.save()
        except RequestRecord.DoesNotExist:
            RequestRecord(name="classroom", count=1).save()
        req = request.query_params.dict()

        if (len(req) != 3) | ("campus" not in req) | ("date" not in req) | ("section" not in req):
            raise ArgumentError()

        campus = req["campus"]
        date = req["date"]
        section = req["section"]
        content = {}
        req = Classroom.objects.filter(campus=campus, date=date, section__contains=section)
        tb_re = req.values("teaching_building").distinct()

        for i in tb_re:
            cr_re = req.filter(teaching_building=i["teaching_building"]).values("classroom").distinct()
            content.update({i["teaching_building"]: cr_re})

        return Response(content)

    @staticmethod
    def post(request):  #
        """
        访问方法 POST http://127.0.0.1:8000/classroom/
        数据格式
        {
            "date":"2020-04-20",
            "classroom":[
                {
                    "campus":"学院路校区",
                    "teaching_building":"一号楼",
                    "classroom":"(一)203",
                    "section":"1,2,3,4,5,7,"
                }
                    ]
        }
        输出：HTTP状态码，错误为500
            正确，{"state":1}
        """
        req = request.data
        Classroom.objects.filter(date=req['date']).delete()

        try:  # 学生更新数据最新时间
            PostRecord.objects.get(name="empty_room").delete()
            PostRecord.objects.get(name="empty_room").save()
        except PostRecord.DoesNotExist:
            PostRecord(name="empty_room").save()

        if "classroom" not in req:
            raise ArgumentError()
        for key in req["classroom"]:
            Classroom(campus=key["campus"], teaching_building=key["teaching_building"],
                      classroom=key["classroom"], date=req["date"], section=key["section"]).save()

        content = {"state": 1}
        return Response(content)
