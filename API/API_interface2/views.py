from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from API_interface.models import Student
from .models import *

class login(APIView):
    def get(self, request, format=None):
        content = {"state":"未定义"}
        return Response(content)
    def post(self, request, format=None):
        usr_name = request.data["usr_name"]
        usr_password = request.data["usr_password"]
        #调用爬虫接口进行验证并取得下面的值
        major = "计算机科学与技术"
        grade = "2017"
        student_id = 17373349
        name = "bin"
        content = {"state":1}#1代表成功，2代表无该账号，3代表密码错误

        Student(id="1").save()
        print(Student.objects.filter(id="1").values("id"))
        return Response(content)


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
    "课程1": [
        {
            "作业": ""
            "dll":""
            "状态":""
        },
        {
             "作业": ""
            "dll":""
            "状态":""
        }
    ],
    "课程2": [
        {
            "作业": ""
            "dll":""
            "状态":""
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

        re = Dll_t.objects.filter(student_id=student_id)

        course_re = re.values("course").distinct()

        for i in course_re:
            cr_re = re.filter(teaching_building=i["course"]).values("homework","dll", "state").distinct()
            content.update({i["course"]:cr_re})
        return Response(content)

        