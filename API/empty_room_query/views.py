from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from course_query.models import Student
from .models import *


#campus 校区
#teaching_building 教学楼
#classroom 教室
#date 日期
#section 节数
'''
查询方法
http http://127.0.0.1:8000/query/classroom/ campus="学院路校区" date="2020-04-13" section="1,2,"
返回格式
{
    "一号楼": [
        {
            "classroom": "(一)103"
        },
        {
            "classroom": "(一)104"
        },
        {
            "classroom": "(一)105"
        }
    ],
    "二号楼": [
        {
            "classroom": "(一)105"
        }
    ]
}
'''
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



#objects
#course
#homework
#dll
#state
#student_id 
'''
返回格式
{
    "计网": [
        {
            "dll": "2010-10-11",
            "homework": "团队作业",
            "state": "已提交"
        }
    ],
    "软工": [
        {
            "dll": "2010-10-9",
            "homework": "团队作业",
            "state": "已提交"
        },
        {
            "dll": "2010-10-10",
            "homework": "个人作业",
            "state": "已提交"
        },
        {
            "dll": "2010-10-12",
            "homework": "最后一次作业",
            "state": "未提交"
        },
        {
            "dll": "2010-10-13",
            "homework": "团队作业",
            "state": "未提交"
        }
    ]
}
'''
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

        