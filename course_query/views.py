from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from request_queue.models import RequestRecord
from .serializers import StudentCourseSerializer, TeacherCourseSerializer, CourseEvaluationSerializer, \
    TeacherEvaluationSerializer
from .models import Student, Course, StudentCourse, Teacher, TeacherCourse, TeacherCourseSpecific, CourseEvaluation, \
    EvaluationUpRecord, EvaluationDownRecord, TeacherEvaluationRecord


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
            elif '单' in end:
                end = end.replace('单', '')
                for i in range(int(start), int(end) + 1):
                    if i % 2 == 1:
                        output += str(i) + ","
            else:
                for i in range(int(start), int(end) + 1):
                    output += str(i) + ","
        else:
            output += (value + ",")
    return output


def split_time(time):
    times = time.strip().split(' ')
    day = times[0][1]
    time_list = times[1].lstrip('第').rstrip('节').split('，')
    return day + '_' + time_list[0] + '_' + time_list[-1]


def add_course(student, semester, info):
    response = HttpResponse(status=201)
    if len(info) == 5:
        name = info[0].replace(' ', '')
        place = info[1].replace(' ', '')
        teacher = info[2].replace(' ', '')
        week = info[3].replace(' ', '')
        time = info[4]
        # 增加课程信息
        try:
            course = Course.objects.get(name=name)
        except Course.DoesNotExist:
            course = Course(name=name)
            course.save()
        # 保存信息
        new_student_course = StudentCourse(student_id=student, course_id=course
                                           , week=split_week(week), time=split_time(time), place=place,
                                           semester=semester)
        new_student_course.save()
        # 增加教师信息
        teachers = teacher.split('，')
        # 一门课程可能有多个教师
        for key in teachers:
            try:
                teacher = Teacher.objects.get(name=key)
            except Teacher.DoesNotExist:
                teacher = Teacher(name=key)
                teacher.save()
            # 增加总课的关联关系
            try:
                course = Course.objects.get(name=name, teachercourse__teacher_id__name=teacher.name)
            except Course.DoesNotExist:
                new_teacher_course = TeacherCourse(teacher_id=teacher, course_id=course)
                new_teacher_course.save()
            # 增加这节课的关联关系
            relation = TeacherCourseSpecific(student_course_id=new_student_course,
                                             teacher_id=teacher)
            relation.save()
            response = HttpResponse(status=201)
        # 不是5项表示数据有缺失
    else:
        message = 'info里的元素一定要为5项，请检查'
        response = HttpResponse(message, status=400)
    return response


class CourseList(APIView):

    @staticmethod
    def get(request):
        start_day = '2020-2-24'
        req = request.query_params.dict()
        result = StudentCourse.objects.all()
        # 记录查询次数
        try:
            count = RequestRecord.objects.get(name='timetable')
        except RequestRecord.DoesNotExist:
            count = RequestRecord(name='timetable', count=0)
        count.count += 1
        count.save()
        # 课表查询请求
        if len(req) == 2:
            for key, value in req.items():
                if key == 'student_id':
                    try:
                        Student.objects.get(id=req['student_id'])
                    except Student.DoesNotExist:
                        message = "没有这个学生的信息"
                        return HttpResponse(message, status=401)
                    result = result.filter(student_id__id=value)
                elif key == 'week':
                    if value != 'all':
                        value += ','
                        result = result.filter(week__icontains=value)
                else:
                    message = '您附加的参数名有错误，只允许\'student_id\', \'week\''
                    return HttpResponse(message, status=400)
            course_serializer = StudentCourseSerializer(result, many=True)
            return Response(course_serializer.data)
        # 当前周查询请求
        if len(req) == 1:
            if 'date' in req.keys():
                content = []
                date1 = datetime.strptime(req['date'], "%Y-%m-%d")
                date2 = datetime.strptime(start_day, "%Y-%m-%d")
                total_week = min(16, int((date1 - date2).days / 7 + 1))
                value = str(total_week)
                content.append({"week": value})
                return Response(content)
            message = '您附加参数有错误，请检查参数是否为date'
            return HttpResponse(message, status=400)
        # 其他非法请求
        message = '您附加参数数量有错误，请检查参数个数是否为1个或2个'
        return HttpResponse(message, status=400)

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
            message = '数据库中没有这个学生，数据库可能出现了问题'
            return HttpResponse(message, status=401)
        # 爬虫的数据库插入请求
        if len(req) == 2:
            response = HttpResponse(status=201)
            semester = '2020_Spring'
            # 更新则默认将原记录删除
            StudentCourse.objects.filter(student_id=student_id).delete()
            # 将爬虫爬取的数据写入数据库
            for lists in req['info']:
                for info in lists:
                    response = add_course(student, semester, info)
                    if response.status_code != 201:
                        return response
            return response
        # 其他非法请求
        message = '参数数量不正确'
        return HttpResponse(message, status=400)


class Search(APIView):

    @staticmethod
    def get(request):
        req = request.query_params.dict()
        result = TeacherCourse.objects.all()
        if 1 <= len(req) <= 3:
            for key in req.keys():
                if key == 'course':
                    name = req['course']
                    result = result.filter(course_id__name__icontains=name)
                elif key == 'teacher':
                    name = req['teacher']
                    result = result.filter(teacher_id__name__icontains=name)
                elif key == 'type':
                    types = req['type']
                    result = result.filter(course_id__type__icontains=types)
                else:
                    message = "参数名称错误"
                    return HttpResponse(message, status=400)
            return Response(TeacherCourseSerializer(result, many=True).data)
        message = "参数数量或名称不正确"
        return HttpResponse(message, status=400)


class CourseEvaluations(APIView):

    @staticmethod
    def get(request):
        req = request.query_params.dict()
        result = CourseEvaluation.objects.all()
        teachers = TeacherCourse.objects.all()
        if 'bid' in req.keys():
            bid = req['bid']
            try:
                course = Course.objects.get(bid=bid)
            except Course.DoesNotExist:
                message = "没有这门课程"
                return HttpResponse(message, status=404)
            result = result.filter(course__bid=bid)
            teachers = teachers.filter(course_id__bid=bid)
            teacher_info = TeacherEvaluationSerializer(teachers, many=True).data
            info = CourseEvaluationSerializer(result, many=True).data
            total_score = 0.0
            count = 0
            for i in result:
                total_score += i.score
                count += 1
            avg_score = total_score / count if count > 0 else 0
            info.insert(0, {"course_name": course.name})
            info.insert(1, {"avg_score": avg_score})
            info.insert(2, teacher_info)
            return Response(info)
        message = "参数数量不正确"
        return HttpResponse(message, status=400)

    # 点赞/加踩
    @staticmethod
    def post(request):
        req = request.data
        if len(req) == 4:
            student_id = req['student_id']
            actor = req['actor']
            bid = req['bid']
            action = req['action']
            try:
                student = Student.objects.get(id=student_id)
                actor = Student.objects.get(id=actor)
            except Student.DoesNotExist:
                message = "没有这个学生"
                return HttpResponse(message, status=401)
            try:
                course = Course.objects.get(bid=bid)
            except Course.DoesNotExist:
                message = "没有这门课程"
                return HttpResponse(message, status=404)
            try:
                evaluation = CourseEvaluation.objects.get(student=student, course=course)
            except CourseEvaluation.DoesNotExist:
                message = "没有这条评价"
                return HttpResponse(message, status=404)
            # 点赞
            if action == 'up':
                try:
                    # 已经赞过
                    EvaluationUpRecord.objects.get(evaluation=evaluation, student=actor)
                    return HttpResponse(status=202)
                except EvaluationUpRecord.DoesNotExist:
                    up_record = EvaluationUpRecord(evaluation=evaluation, student=actor)
                    up_record.save()
                    evaluation.up += 1
                    evaluation.save()
                    return HttpResponse(status=201)
            # 加踩
            if action == 'down':
                try:
                    # 已经踩过
                    EvaluationDownRecord.objects.get(evaluation=evaluation, student=actor)
                    return HttpResponse(status=202)
                except EvaluationDownRecord.DoesNotExist:
                    down = EvaluationDownRecord(evaluation=evaluation, student=actor)
                    down.save()
                    evaluation.down += 1
                    evaluation.save()
                    return HttpResponse(status=201)
            # 取消点赞
            if action == 'cancel_up':
                try:
                    up_record = EvaluationUpRecord.objects.get(evaluation=evaluation, student=actort)
                    up_record.delete()
                    evaluation.up -= 1
                    evaluation.save()
                    return HttpResponse(status=201)
                except EvaluationUpRecord.DoesNotExist:
                    message = "不存在这条点赞记录"
                    return HttpResponse(message, status=404)
            # 取消加踩
            if action == 'cancel_down':
                try:
                    down = EvaluationDownRecord.objects.get(evaluation=evaluation, student=actor)
                    down.delete()
                    evaluation.down -= 1
                    evaluation.save()
                    return HttpResponse(status=201)
                except EvaluationDownRecord.DoesNotExist:
                    message = "不存在这条被踩记录"
                    return HttpResponse(message, status=404)
        message = "参数数量不正确"
        return HttpResponse(message, status=400)

    # 创建新评价/修改评价
    @staticmethod
    def put(request):
        req = request.data
        if len(req) == 4:
            bid = req['bid']
            text = req['text']
            score = req['score']
            student_id = req['student_id']
            if not 1 <= score <= 5:
                message = "评分只能为1-5分"
                return HttpResponse(message, status=400)
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                message = "没有这个学生"
                return HttpResponse(message, status=401)
            try:
                course = Course.objects.get(bid=bid)
            except Course.DoesNotExist:
                message = "没有这门课程"
                return HttpResponse(message, status=404)
            try:
                evaluation = CourseEvaluation.objects.get(student=student, course=course)
                evaluation.evaluation = text
                evaluation.score = score
            except CourseEvaluation.DoesNotExist:
                evaluation = CourseEvaluation(student=student, course=course, score=score, evaluation=text)
            evaluation.save()
            return HttpResponse(status=201)
        message = "参数数量不正确"
        return HttpResponse(message, status=400)

    # 删除评价
    @staticmethod
    def delete(request):
        req = request.data
        if len(req) == 2:
            bid = req['bid']
            student_id = req['student_id']
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                message = "没有这个学生"
                return HttpResponse(message, status=401)
            try:
                course = Course.objects.get(bid=bid)
            except Course.DoesNotExist:
                message = "没有这门课程"
                return HttpResponse(message, status=404)
            try:
                evaluation = CourseEvaluation.objects.get(student=student, course=course)
                evaluation.delete()
                return HttpResponse(status=204)
            except CourseEvaluation.DoesNotExist:
                message = "没有这条评价"
                return HttpResponse(message, status=404)
        message = "参数数量不正确"
        return HttpResponse(message, status=400)


class TeacherEvaluations(APIView):

    # 点赞老师
    @staticmethod
    def post(request):
        req = request.data
        if len(req) == 4:
            teacher_name = req['teacher']
            bid = req['bid']
            actor = req['actor']
            action = req['action']
            try:
                teacher = Teacher.objects.get(name=teacher_name)
            except Teacher.DoesNotExist:
                message = "没有这个老师！"
                return HttpResponse(message, status=404)
            try:
                course = Course.objects.get(bid=bid)
            except Course.DoesNotExist:
                message = "没有这门课程"
                return HttpResponse(message, status=404)
            try:
                student = Student.objects.get(id=actor)
            except Student.DoesNotExist:
                message = "没有这个学生！"
                return HttpResponse(message, status=401)
            try:
                teacher_course = TeacherCourse.objects.get(teacher_id=teacher, course_id=course)
            except TeacherCourse.DoesNotExist:
                message = "没有这个课程评价"
                return HttpResponse(message, status=404)
            if action == 'up':
                try:
                    # 已经点过赞
                    TeacherEvaluationRecord.objects.get(teacher_course=teacher_course, student=student)
                    return HttpResponse(status=202)
                except TeacherEvaluationRecord.DoesNotExist:
                    # 没点过赞
                    up = TeacherEvaluationRecord(teacher_course=teacher_course, student=student)
                    up.save()
                    teacher_course.up += 1
                    teacher_course.save()
                return HttpResponse(status=201)
            elif action == 'cancel_up':
                try:
                    up = TeacherEvaluationRecord.objects.get(teacher_course=teacher_course, student=student)
                    up.delete()
                    teacher_course.up -= 1
                    teacher_course.save()
                except TeacherEvaluationRecord.DoesNotExist:
                    message = "不存在这个点赞记录"
                    return HttpResponse(status=404)
                return HttpResponse(status=201)
        message = "参数数量错误"
        return HttpResponse(message, status=400)
