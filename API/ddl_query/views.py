from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404, HttpResponseBadRequest, HttpResponse
from .models import *


class query_ddl(APIView):#输入学号：输出作业，dll，提交状态，课程
    def get(self, request, format=None):
        """
        输入：学号，输出：作业，dll，提交状态，课程
        参数1:学生学号 e.g. 17373349
        例:http://127.0.0.1:8000/ddl/?student_id=17373349
        返回作业，dll，提交状态，课程
        """
        req = request.query_params.dict()
        student_id = req["student_id"]
        print(student_id)
        content = []


        re = DDL_t.objects.filter(student_id=student_id)

        course_re = re.values("course").distinct()

        
        for i in course_re:
            cr_re = re.filter(course=i["course"]).values("homework", "ddl", "state").distinct().order_by("-state")
            content.append({"name":i["course"],"content":cr_re})
        return Response(content)
      
    def post(self, request, format=None):#
        '''
        {
            "student_id":"17373349",
            "ddl":[
                    {
                        "content":[
                            {
                                "ddl":"2020-04-28 04:03:00",
                                "homework":"第一次作业",
                                "state":"提交"
                            },
                            {
                                "ddl":"2020-04-23 02:03:00",
                                "homework":"第二次作业",
                                "state":"未提交"
                            }
                        ],
                        "name":"计算机科学方法论"
                    },
                    {
                        "content":[
                            {
                                "ddl":"2020-04-23 04:03:00",
                                "homework":"第一次作业",
                                "state":"提交"
                            }
                        ],
                        "name":"计算机图形学"
                    }
                ]
        }
        '''
        req = request.data
        try:
            student = Student.objects.get(id=req['student_id'])
            DDL_t.objects.filter(student_id=req['student_id']).delete()
        except Student.DoesNotExist:
            raise Http404
        
        for key in req['ddl']:
            if len(key) == 2:
                content = key["content"]
                name = key["name"]
                for i in content:
                    DDL_t(student_id=student, ddl=i["ddl"], homework=i["homework"],
                     state=i["state"], course=name).save()
            else:
                return HttpResponseBadRequest()
        
        content = {"state":1}
        return Response(content)
