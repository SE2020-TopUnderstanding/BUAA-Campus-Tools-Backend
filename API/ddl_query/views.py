from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *


class query_ddl(APIView):#输入学号：输出作业，dll，提交状态，课程
    def get(self, request, format=None):
        content = {"state":"未定义"}
        return Response(content)
    def post(self, request, format=None):#
        student_id = request.data["student_id"]
        content = {}
        re = DDL_t.objects.filter(student_id=student_id)

        course_re = re.values("course").distinct()

        for i in course_re:
            cr_re = re.filter(course=i["course"]).values("homework","dll", "state").distinct()
            content.update({i["course"]:cr_re})
        return Response(content)
