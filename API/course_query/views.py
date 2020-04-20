from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404, HttpResponse
from .serializers import *
from .models import *
from django.http import HttpResponseBadRequest
from datetime import datetime
from request_queue.views import req_queue


def split_week(week):
    weeks = []
    parts = week.split("，")
    for value in parts:
        if '-' in value:
            start = value.split('-')[0]
            end = value.split('-')[1]
            for i in range(int(start), int(end) + 1):
                weeks.append(i)
        else:
            weeks.append(value)
    output = ""
    for value in weeks:
        output += str(value)
        output += ','
    return output


class CourseList(APIView):
    """
    本类接收get, post请求
    get方法给前端使用
    post方法给爬虫使用
    """

    @staticmethod
    def get(request):
        """可使用的参数有：
        student_id: 附带学生学号，查询指定学生课表;
        semester: 附带学年学期，查询指定学期课表;
        week: 附带周数，查询指定周的课表，若参数值为all,则查询该学期全部周的课表;
        例：127.0.0.1/timetable?student_id=17333333&semester=2020_Spring&week=3
        查询学号为17373333 2020春季学期第三周课表;
        没有提供参数，参数数量错误，返回400错误;
        参数错误，返回404错误;
        """
        start_day = '2020-2-24'
        req = request.query_params.dict()
        result = StudentCourse.objects.all()
        if len(req) == 2:
            for key, value in req.items():
                if key == 'student_id':
                    result = result.filter(student_id__id=value)
                elif key == 'week':
                    value += ','
                    result = result.filter(week__icontains=value)
                else:
                    raise Http404
            course_serializer = StudentCourseSerializer(result, many=True)
            return Response(course_serializer.data)
        elif len(req) == 1:
            if 'date' in req.keys():
                content = []
                date1 = datetime.strptime(req['date'], "%Y-%m-%d")
                date2 = datetime.strptime(start_day, "%Y-%m-%d")
                total_week = min(16, int((date1 - date2).days / 7))
                value = str(total_week)
                content.append({"week": value})
                return Response(content)
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()

    @staticmethod
    def post(request):
        """
        根据post的json文件来将相关数据插入数据库；
        格式：{student_id:(id), semester:(sm), info:[[课程名称1，地点1...],[课程名称2，地点2...]}
        """
        req = request.data
        # 找不到这个同学肯定有问题
        student_id = req['student_id']
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            print("not exists:" + student_id)
            raise Http404

        if len(req) == 3:
            semester = req['semester']
            # 更新则默认将原记录删除
            StudentCourse.objects.filter(student_id=student_id).delete()
        elif len(req) == 1:
            print(req_queue)
            req_queue.put({'usr_name': student.usr_name, 'password': student.usr_password, 'req_type': 's'})
            return HttpResponse(status=202)
        else:
            return HttpResponseBadRequest()

        for info in req['info']:
            if len(info) == 5:
                name = info[0]
                place = info[1]
                teacher = info[2]
                week = info[3]
                time = info[4]
                # 增加课程信息
                try:
                    course = Course.objects.get(name=name)
                except Course.DoesNotExist:
                    course = Course(name=name)
                    course.save()
                # 增加教师信息
                teacher = teacher.replace(' ', '')
                teachers = teacher.split('，')
                for key in teachers:
                    try:
                        teacher = Teacher.objects.get(name=key)
                    except Teacher.DoesNotExist:
                        teacher = Teacher(name=key)
                        teacher.save()
                    # 增加关联关系
                    try:
                        course = Course.objects.get(name=name, teachercourse__teacher_id__name=teacher.name)
                    except Course.DoesNotExist:
                        new_teacher_course = TeacherCourse(teacher_id=teacher, course_id=course)
                        new_teacher_course.save()
                # 保存信息
                new_student_course = StudentCourse(student_id=student, course_id=course
                                                   , week=split_week(week), time=time, place=place, semester=semester)
                new_student_course.save()
            else:
                return HttpResponseBadRequest()
        return HttpResponse(status=201)
