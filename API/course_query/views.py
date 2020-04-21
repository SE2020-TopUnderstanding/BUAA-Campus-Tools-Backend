from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404, HttpResponse
from .serializers import *
from .models import *
from django.http import HttpResponseBadRequest
from datetime import datetime
import request_queue.views as req_module


def split_week(week):
    """分割 week
    input: 1,2,3-5,4-6双
    output: 1,2,3,4,5,4,6,
    """
    parts = week.split("，")
    output = ""
    for value in parts:
        if '-' in value:
            start = value.split('-')[0]
            end = value.split('-')[1]
            if '双' in end:
                end = end.replace('双', '')
                for i in range(int(start), int(end) + 1):
                    if i % 2 == 0:
                        output += str(i) + ","
            else:
                for i in range(int(start), int(end) + 1):
                    output += str(i) + ","
        else:
            output += (value + ",")
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
        week: 附带周数，查询指定周的课表;
        date: 返回这周是第几周
        例：127.0.0.1/timetable?student_id=17333333&week=3
        查询学号为17373333 2020春季学期第三周课表;
        没有提供参数，参数数量错误，返回400错误;
        参数错误，返回404错误;
        """
        start_day = '2020-2-24'
        req = request.query_params.dict()
        result = StudentCourse.objects.all()
        # 课表查询请求
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
        # 当前周查询请求
        elif len(req) == 1:
            if 'date' in req.keys():
                content = []
                date1 = datetime.strptime(req['date'], "%Y-%m-%d")
                date2 = datetime.strptime(start_day, "%Y-%m-%d")
                total_week = min(16, int((date1 - date2).days / 7 + 1))
                value = str(total_week)
                content.append({"week": value})
                return Response(content)
            else:
                return HttpResponseBadRequest()
        # 其他非法请求
        else:
            return HttpResponseBadRequest()

    @staticmethod
    def post(request):
        """
        根据post的json文件来将相关数据插入数据库；
        格式：{student_id:(id), semester:(sm), info:[[课程名称1，地点1...],[课程名称2，地点2...]}
        """
        req = request.data
        # 确保数据库中有这个同学的信息
        student_id = req['student_id']
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise Http404
        # 爬虫的数据库插入请求
        if len(req) == 2:
            semester = '2020_Spring'
            # 更新则默认将原记录删除
            StudentCourse.objects.filter(student_id=student_id).delete()
            # 将爬虫爬取的数据写入数据库
            for lists in req['info']:
                for info in lists:
                    # info必须有5项
                    if len(info) == 5:
                        name = info[0].replace(' ', '')
                        place = info[1]
                        teacher = info[2].replace(' ', '')
                        week = info[3]
                        time = info[4]
                        # 增加课程信息
                        try:
                            course = Course.objects.get(name=name)
                        except Course.DoesNotExist:
                            course = Course(name=name)
                            course.save()
                        # 增加教师信息
                        teachers = teacher.split('，')
                        # 一门课程可能有多个教师
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
                                                           , week=split_week(week), time=time, place=place,
                                                           semester=semester)
                        new_student_course.save()
                    # 不是5项表示数据有缺失
                    else:
                        return HttpResponseBadRequest()
            return HttpResponse(status=201)
        # 前端的更新请求
        elif len(req) == 1:
            req_module.req_id += 1
            req_id = req_module.req_id
            req_queue = req_module.req_queue
            pending_work = req_module.pending_work
            req_queue.put(
                {'req_id': req_id, 'usr_name': student.usr_name, 'password': student.usr_password, 'req_type': 's'})
            pending_work.append(req_module.req_id)
            return Response([{"id": req_id}])
        # 其他非法请求
        else:
            return HttpResponseBadRequest()
