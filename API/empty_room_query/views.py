from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from course_query.models import Student
from django.http import Http404, HttpResponseBadRequest, HttpResponse
from .models import *




class query_classroom(APIView):
    def get(self, request, format=None):
        """
        输入：校区，日期，第几节到第几节，返回：教学楼，教室
        参数1:校区 e.g. 新主楼
        参数2：日期 e.g. 2020-4-18
        参数3：第几节到第几节 e.g. 1,2,3,
        例:http://127.0.0.1:8000/classroom/?campus=学院路校区&date=2020-04-20&section=1,2,3,
        返回:查询结果
        没有提供参数，参数数量错误，返回400错误;
        参数错误，返回404错误;
        """
        req = request.query_params.dict()

        if len(req) != 3:
            return HttpResponseBadRequest()
        if ("campus" not in req) | ("date" not in req) | ("section" not in req):
            return HttpResponse(status=404)

        campus = req["campus"]
        date = req["date"]
        section = req["section"]
        content = {}
        re = Classroom_t.objects.filter(campus=campus, date=date,
                                        section__contains=section)
        tb_re = re.values("teaching_building").distinct()

        for i in tb_re:
            cr_re = re.filter(teaching_building=i["teaching_building"]).values("classroom").distinct()
            content.update({i["teaching_building"]:cr_re})

        return Response(content)

    def post(self, request, format=None):#
        '''
        {
            "date":"2020-04-20",
            "classroom":[
                {
                    "campus":"学院路校区",
                    "teaching_building":"一号楼",
                    "classroom":"(一)203",
                    "section":"1,2,3,4,5,7,"
                },
                {
                    "campus":"学院路校区",
                    "teaching_building":"一号楼",
                    "classroom":"(一)204",
                    "section":"1,2,3,4,7,"
                },
                {
                    "campus":"学院路校区",
                    "teaching_building":"三号楼",
                    "classroom":"(三)202",
                    "section":"3,4,5,7,8,"
                },
                {
                    "campus":"学院路校区",
                    "teaching_building":"三号楼",
                    "classroom":"(三)202",
                    "section":"3,4,5,7,8,"
                }
            ]    
        }
        '''
        req = request.data
        try:
            Classroom_t.objects.filter(date=req['date']).delete()
        except Student.DoesNotExist:
            raise Http404

        for key in req["classroom"]:
                    Classroom_t(campus=key["campus"],teaching_building=key["teaching_building"],
                        classroom=key["classroom"],date=req["date"],section=key["section"]).save()

        content = {"state":1}
        return Response(content)