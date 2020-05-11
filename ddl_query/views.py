import logging
from itertools import chain
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Q


from course_query.models import Student
from request_queue.models import RequestRecord
from .models import DDL


def add_0(time):
    if (int(time) < 10) & (time != "00"):
        time = "0" + time
    return time


def standard_time(initial_time):
    """
    将爬虫爬的ddl时间修改为标准时间
    数据库中2020-3-19 下午11:55
    标准时间2020-03-19 23:55:00
    """
    temp = initial_time.split("-")
    year = temp[0]
    month = add_0(temp[1])

    temp2 = temp[2].split(" ")
    day = add_0(temp2[0])

    time = ""
    kind = 0
    if "上午" in temp2[1]:
        kind = 0
        time = temp2[1].replace('上午', '')
    elif "下午" in temp2[1]:
        kind = 1  # 代表下午
        time = temp2[1].replace("下午", '')
    temp3 = time.split(":")

    if kind == 0:
        if temp3[0] == "12":
            hour = "00"
        else:
            hour = add_0(temp3[0])
    else:
        if temp3[0] == "12":
            hour = "12"
        else:
            hour = str(int(temp3[0]) + 12)
    minute = add_0(temp3[1])

    return year + "-" + month + "-" + day + " " + hour + ":" + minute + ":00"


class QueryDdl(APIView):  # 输入学号：输出作业，dll，提交状态，课程
    @staticmethod
    def get(request):
        """
        输入：学号，输出：作业，dll，提交状态，课程
        参数1:学生学号 e.g. 17373349
        例:http://127.0.0.1:8000/ddl/?student_id=17373349
        返回作业，dll，提交状态，课程
        没有提供参数，参数数量错误，返回500错误;
        参数错误，返回500错误;
        查询用户不存在返回401
        """
        try:  # 保存前端请求数据
            record = RequestRecord.objects.get(name="ddl")
            record.count = record.count + 1
            record.save()
        except RequestRecord.DoesNotExist:
            RequestRecord(name="ddl", count=1).save()

        req = request.query_params.dict()

        if len(req) != 1:
            return HttpResponse(status=500)
        if "student_id" not in req:
            return HttpResponse(status=500)

        student_id = req["student_id"]
        content = []

        try:
            Student.objects.get(id=req['student_id'])
            req = DDL.objects.filter(student_id=student_id)
        except Student.DoesNotExist:
            return HttpResponse(status=401)

        course_re = req.values("course").distinct()

        for i in course_re:
            cr_re_1 = req.filter(Q(course=i["course"]) &
                                 (Q(state="尚未提交") | Q(state="草稿 - 进行中"))).values("homework", "ddl", "state").distinct()
            cr_re_2 = req.filter(Q(course=i["course"]) &
                                 (~Q(state="尚未提交") &
                                  ~Q(state="草稿 - 进行中"))).values("homework", "ddl", "state").distinct()
            cr_re = chain(cr_re_1, cr_re_2)
            content.append({"name": i["course"], "content": cr_re})
        return Response(content)

    @staticmethod
    def post(request):
        """
        访问方法 POST http://127.0.0.1:8000/ddl/
        {
            "student_id":"17373349",
            "ddl":[
                    {
                        "content":[
                            {
                                "ddl":"2020-3-19 下午11:55",
                                "homework":"第一次作业",
                                "state":"提交"
                            },
                            {
                                "ddl":"2020-3-19 下午11:55",
                                "homework":"第二次作业",
                                "state":"未提交"
                            }
                        ],
                        "name":"计算机科学方法论"
                    },
                    {
                        "content":[
                            {
                                "ddl":"2020-3-19 下午11:55",
                                "homework":"第一次作业",
                                "state":"提交"
                            }
                        ],
                        "name":"计算机图形学"
                    }
                ]
        }
        错误：500
        """
        req = request.data
        try:
            student = Student.objects.get(id=req['student_id'])
            DDL.objects.filter(student_id=req['student_id']).delete()
        except Student.DoesNotExist:
            return HttpResponse(status=401)

        if "ddl" not in req:
            return HttpResponse(status=500)
        for key in req['ddl']:
            if len(key) == 2:
                content = key["content"]
                name = key["name"]
                for i in content:
                    if i["ddl"] == "":
                        time = ""
                    else:
                        try:
                            time = standard_time(i["ddl"])
                        except ValueError:
                            text = "ddl时间格式错误 " + i["ddl"]
                            logging.warning(text)
                            return HttpResponse(status=500)
                    DDL(student_id=student, ddl=time, homework=i["homework"],
                        state=i["state"], course=name).save()
            else:
                return HttpResponse(status=400)

        content = {"state": 1}
        return Response(content)
