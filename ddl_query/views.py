import logging
from itertools import chain
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from api_exception.exceptions import ArgumentError, UnAuthorizedError, DatabaseNotExitError
from course_query.models import Student
from request_queue.models import RequestRecord
from .models import DDL, SchoolCalendar, SchoolYear


def add_0(time):
    if (int(time) < 10) & (time != "00") & (len(time) < 2):
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
        参数错误，返回400错误;
        查询用户不存在返回401
        """
        try:  # 保存前端请求数据
            record = RequestRecord.objects.get(name="ddl")
            record.count = record.count + 1
            record.save()
        except RequestRecord.DoesNotExist:
            RequestRecord(name="ddl", count=1).save()

        req = request.query_params.dict()

        if (len(req) != 1) or ("student_id" not in req):
            raise ArgumentError()

        student_id = req["student_id"]
        content = []

        try:
            Student.objects.get(id=req['student_id'])
            req = DDL.objects.filter(student_id=student_id)
        except Student.DoesNotExist:
            raise UnAuthorizedError()

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
        错误：400
        """
        req = request.data
        try:
            student = Student.objects.get(id=req['student_id'])
            DDL.objects.filter(student_id=req['student_id']).delete()
        except Student.DoesNotExist:
            raise UnAuthorizedError()

        if "ddl" not in req:
            raise ArgumentError()
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
                            raise ArgumentError()
                    DDL(student_id=student, ddl=time, homework=i["homework"],
                        state=i["state"], course=name).save()
            else:
                raise ArgumentError()

        content = {"state": 1}
        return Response(content)


class QuerySchoolCalendar(APIView):
    @staticmethod
    def get(request):
        """
        功能：前端获取校历和该学生未完成的ddl
        调用方法：http://127.0.0.1:8000/ddl/Calendar/?student_id=17373349&school_year=2019-2020
        返回参数：具体学期，日期，节假日，ddl事件
        具体json格式见接口文档，两个列表，一个ddl，一个节假日
        :param request:
        :return:
        """
        try:  # 保存前端请求数据
            record = RequestRecord.objects.get(name="SchoolCalendar")
            record.count = record.count + 1
            record.save()
        except RequestRecord.DoesNotExist:
            RequestRecord(name="SchoolCalendar", count=1).save()

        req = request.query_params.dict()

        if (len(req) != 2) or ("student_id" not in req) or ("school_year" not in req):
            raise ArgumentError()

        try:
            Student.objects.get(id=req['student_id'])
            ddl_req = DDL.objects.filter(student_id=req['student_id'])
        except Student.DoesNotExist:
            raise UnAuthorizedError()

        #该学生未完成的ddl
        ddl = ddl_req.filter((Q(state="尚未提交") | Q(state="草稿 - 进行中"))).values("course", "homework", "ddl")

        # 第一学期开始日期+寒假开始日期+第二学期开始日期+第三学期开始日期
        try:
            semester = SchoolYear.objects.get(school_year=req["school_year"])
        except SchoolYear.DoesNotExist:
            raise DatabaseNotExitError

        #节假日信息
        holiday = SchoolCalendar.objects.filter(Q(semester__contains=req["school_year"])
                                                & ~Q(holiday__contains=req["school_year"]))

        content = {"school_year": req["school_year"], "first_semester": semester.first_semester,
                   "winter_semester": semester.winter_semester, "second_semester": semester.second_semester,
                   "third_semester": semester.third_semester, "end_semester": semester.end_semester}

        content.update({"holiday": holiday.values("year", "semester", "date", "holiday"),
                        "ddl": ddl})

        return Response(content)

    @staticmethod
    def post(request):
        """
        插入某一学年的所有数据，若该学年已被录入，则之前的被删除
        http://127.0.0.1:8000/ddl/Calendar/
        :param request:
        :return:
        """
        req = request.data
        if ("school_year" not in req) | ("first_semester" not in req)\
                | ("winter_semester" not in req) | ("second_semester" not in req) \
                | ("third_semester" not in req) | ("end_semester" not in req) \
                | ("content" not in req):
            raise ArgumentError()

        SchoolYear.objects.filter(school_year=req["school_year"]).delete()

        SchoolYear(school_year=req["school_year"], first_semester=req["first_semester"],
                   winter_semester=req["winter_semester"], second_semester=req["second_semester"],
                   third_semester=req["third_semester"], end_semester=req["end_semester"]).save()
        s_y = SchoolYear.objects.get(school_year=req["school_year"])
        for i in req["content"]:
            SchoolCalendar(year=s_y, semester=i["semester"], date=i["date"], holiday=i["holiday"]).save()

        return Response({"state": "成功"})
