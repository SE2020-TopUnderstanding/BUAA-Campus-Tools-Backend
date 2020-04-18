from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *


class query_ddl(APIView):#输入学号：输出作业，dll，提交状态，课程
    def get(self, request, format=None):
        """
        输入：学号，输出：作业，dll，提交状态，课程
        参数1:学生学号 e.g. 17373349
        例:http --form GET http://127.0.0.1:8000/ddl/ student_id="17373349"
        返回作业，dll，提交状态，课程
        """
        student_id = request.data["student_id"]
        print(student_id)
        content = {}


        re = DDL_t.objects.filter(student_id=student_id)

        course_re = re.values("course").distinct()

        for i in course_re:
            cr_re = re.filter(course=i["course"]).values("homework", "ddl", "state").distinct().order_by("state")
            content.update({i["course"]:cr_re})
        return Response(content)
      
    def post(self, request, format=None):#
        content = {"state":"未定义"}
        return Response(content)
