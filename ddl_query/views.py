from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404, HttpResponseBadRequest, HttpResponse
from .models import *
from request_queue.models import RequestRecord
import logging
from django.db.models import Q
from django.forms.models import model_to_dict
from itertools import chain

def add_0(s):
    if (int(s)<10) & (s != "00"):
        s = "0" + s
    return s

def standard_time(t):
    '''
    将爬虫爬的ddl时间修改为标准时间
    数据库中2020-3-19 下午11:55
    标准时间2020-03-19 23:55:00
    '''
    temp = t.split("-")
    year = temp[0]
    month = add_0(temp[1])
    
    temp2 = temp[2].split(" ")
    day = add_0(temp2[0])
    
    time = ""
    type = 0
    if "上午" in temp2[1]:
        time = temp2[1].replace('上午','')
    elif "下午" in temp2[1]:
        type = 1#代表下午
        time = temp2[1].replace("下午",'')
    temp3 = time.split(":")

    if type == 0:
        if temp3[0] == "12":
            hour = "00"
        else:
            hour = add_0(temp3[0])
    else:
        if temp3[0] == "12":
            hour = "12"
        else:
            hour = str(int(temp3[0])+12)
    minute = add_0(temp3[1])

    return year + "-" + month + "-" + day + " " + hour + ":" + minute + ":00"



class query_ddl(APIView):#输入学号：输出作业，dll，提交状态，课程
    def get(self, request, format=None):
        """
        输入：学号，输出：作业，dll，提交状态，课程
        参数1:学生学号 e.g. 17373349
        例:http://127.0.0.1:8000/ddl/?student_id=17373349
        返回作业，dll，提交状态，课程
        没有提供参数，参数数量错误，返回500错误;
        参数错误，返回500错误;
        查询用户不存在返回401
        """
        try:#保存前端请求数据
            record = RequestRecord.objects.get(name="ddl")
            record.count = record.count+1
            record.save()
        except RequestRecord.DoesNotExist:
            RequestRecord(name="ddl", count=1).save()

        req = request.query_params.dict()

        if len(req) != 1:
            return HttpResponse(status=500)
        if ("student_id" not in req):
            return HttpResponse(status=500)

        student_id = req["student_id"]
        content = []

        try:
            Student.objects.get(id=req['student_id'])
            re = DDL_t.objects.filter(student_id=student_id)
        except Student.DoesNotExist:
            return HttpResponse(status=401)

        course_re = re.values("course").distinct()

        
        for i in course_re:
            cr_re_1 = re.filter(Q(course=i["course"])
                    &(Q(state="尚未提交")|Q(state="草稿 - 进行中"))).values("homework", "ddl", "state").distinct()
            cr_re_2 = re.filter(Q(course=i["course"])
                    &(~Q(state="尚未提交")&~Q(state="草稿 - 进行中"))).values("homework", "ddl", "state").distinct()
            cr_re = chain(cr_re_1,cr_re_2)
            content.append({"name":i["course"],"content":cr_re})
        return Response(content)
      
    def post(self, request, format=None):#
        '''
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
        '''
        req = request.data
        try:
            student = Student.objects.get(id=req['student_id'])
            DDL_t.objects.filter(student_id=req['student_id']).delete()
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
                        t = ""
                    else:
                        try:
                            t = standard_time(i["ddl"])
                        except:
                            logging.warning("ddl时间格式错误 "+i["ddl"])
                            return HttpResponse(status=500)
                    DDL_t(student_id=student, ddl=t, homework=i["homework"],
                     state=i["state"], course=name).save()
            else:
                return HttpResponse(status=400)
        
        content = {"state":1}
        return Response(content)
