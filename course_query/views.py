from datetime import datetime

from django.db.models import Avg
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from request_queue.models import RequestRecord
from course_query.serializers import StudentCourseSerializer, TeacherCourseSerializer, CourseEvaluationSerializer, \
    TeacherEvaluationSerializer
from course_query.models import Student, Course, StudentCourse, Teacher, TeacherCourse, TeacherCourseSpecific, \
    CourseEvaluation, PublicCourse, \
    EvaluationUpRecord, EvaluationDownRecord, TeacherEvaluationRecord
from api_exception.exceptions import ArgumentError, UnAuthorizedError, NotFoundError


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


def check_public(course_name, bid):
    # 体育课
    if course_name.find('体育') != -1:
        try:
            public_course = PublicCourse.objects.get(name=course_name)
        except PublicCourse.DoesNotExist:
            public_course = PublicCourse(name=course_name)
            public_course.save()
        return bid + str(public_course.id)
    return bid


def add_course(info):
    # 增加课程信息
    name = info[0].replace(' ', '')
    bid = info[1].replace(' ', '')
    bid = check_public(name, bid)
    credit = float(info[2].replace(' ', ''))
    hours = info[3].replace(' ', '')
    hours = None if hours == "" else int(float(hours))
    department = info[4].replace(' ', '')
    types = info[5].replace(' ', '')
    try:
        course = Course.objects.get(bid=bid)
    except Course.DoesNotExist:
        course = Course(bid=bid, name=name, credit=credit, hours=hours, department=department, type=types)
        course.save()
    return course


def add_teacher(key):
    try:
        teacher = Teacher.objects.get(name=key)
    except Teacher.DoesNotExist:
        teacher = Teacher(name=key)
        teacher.save()
    return teacher


def add_teacher_relation(teacher, course):
    try:
        Course.objects.get(teachercourse__teacher_id__name=teacher.name)
    except Course.DoesNotExist:
        new_teacher_course = TeacherCourse(teacher_id=teacher, course_id=course)
        new_teacher_course.save()


def add_student_course(student, semester, info):
    if len(info) == 10:
        place = info[6].replace(' ', '')
        teacher = info[7].replace(' ', '')
        week = info[8].replace(' ', '')
        time = info[9]
        # 增加课程信息
        course = add_course(info[0:5])
        # 保存信息
        new_student_course = StudentCourse(student_id=student, course_id=course
                                           , week=split_week(week), time=split_time(time), place=place,
                                           semester=semester)
        new_student_course.save()
        # 增加教师信息
        teachers = teacher.split('，')
        # 一门课程可能有多个教师
        for key in teachers:
            teacher = add_teacher(key)
            # 增加总课的关联关系
            add_teacher_relation(teacher, course)
            # 增加这节课的关联关系
            relation = TeacherCourseSpecific(student_course_id=new_student_course,
                                             teacher_id=teacher)
            relation.save()
    # 不是10项表示数据有缺失
    raise ArgumentError()


def evaluator_count(course):
    return CourseEvaluation.objects.filter(course=course).count()


def up_count(evaluation):
    return EvaluationUpRecord.objects.filter(evaluation=evaluation).count()


def down_count(evaluation):
    return EvaluationDownRecord.objects.filter(evaluation=evaluation).count()


def up_count_teacher(teacher_course):
    return TeacherEvaluationRecord.objects.filter(teacher_course=teacher_course).count()


def up_check(student, evaluation):
    return EvaluationUpRecord.objects.filter(student=student, evaluation=evaluation).count() == 1


def down_check(student, evaluation):
    return EvaluationDownRecord.objects.filter(student=student, evaluation=evaluation).count() == 1


def format_serializer(result, student):
    for dicts in result:
        evaluation_id = dicts['id']
        evaluation = CourseEvaluation.objects.get(id=evaluation_id)
        dicts['has_up'] = up_check(student, evaluation)
        dicts['has_down'] = down_check(student, evaluation)
    return result


def up_check_teacher(student, evaluation):
    return TeacherEvaluationRecord.objects.filter(student=student, teacher_course=evaluation).count() == 1


def format_serializer_teacher(result, student):
    for dicts in result:
        evaluation_id = dicts['id']
        evaluation = TeacherCourse.objects.get(id=evaluation_id)
        dicts['has_up'] = up_check_teacher(student, evaluation)
    return result


def format_search(result):
    exist_bid = []
    result_list = []
    for dicts in result:
        if dicts['bid'] in exist_bid:
            continue
        course = Course.objects.get(bid=dicts['bid'])
        exist_bid.append(dicts['bid'])
        evaluations = CourseEvaluation.objects.filter(course=course)
        avg_score = evaluations.aggregate(Avg('score'))['score__avg']
        dicts['avg_score'] = avg_score
        result_list.append(dicts)
    return result_list


def get_evaluation(req):
    try:
        student_id = req['student_id']
        actor = req['actor']
        bid = req['bid']
    except KeyError:
        raise ArgumentError()
    try:
        student = Student.objects.get(id=student_id)
        actor = Student.objects.get(id=actor)
    except Student.DoesNotExist:
        raise UnAuthorizedError()
    try:
        course = Course.objects.get(bid=bid)
    except Course.DoesNotExist:
        raise NotFoundError(detail="没有这门课程")
    try:
        evaluation = CourseEvaluation.objects.get(student=student, course=course)
    except CourseEvaluation.DoesNotExist:
        raise NotFoundError(detail="没有这条评价")
    return actor, evaluation


def up_action(evaluation, actor):
    try:
        # 已经赞过
        EvaluationUpRecord.objects.get(evaluation=evaluation, student=actor)
        up_cnt = evaluation.up
        down_cnt = evaluation.down
        return Response({"up": up_cnt, "down": down_cnt}, status=202)
    except EvaluationUpRecord.DoesNotExist:
        try:
            down = EvaluationDownRecord.objects.get(evaluation=evaluation, student=actor)
            down.delete()
        except EvaluationDownRecord.DoesNotExist:
            pass
        up_record = EvaluationUpRecord(evaluation=evaluation, student=actor)
        up_record.save()
        evaluation.up = up_count(evaluation)
        evaluation.down = down_count(evaluation)
        evaluation.save()
        up_cnt = evaluation.up
        down_cnt = evaluation.down
        return Response({"up": up_cnt, "down": down_cnt}, status=201)


def down_action(evaluation, actor):
    try:
        # 已经踩过
        EvaluationDownRecord.objects.get(evaluation=evaluation, student=actor)
        up_cnt = evaluation.up
        down_cnt = evaluation.down
        return Response({"up": up_cnt, "down": down_cnt}, status=202)
    except EvaluationDownRecord.DoesNotExist:
        try:
            up_record = EvaluationUpRecord.objects.get(evaluation=evaluation, student=actor)
            up_record.delete()
        except EvaluationUpRecord.DoesNotExist:
            pass
        down = EvaluationDownRecord(evaluation=evaluation, student=actor)
        down.save()
        evaluation.up = up_count(evaluation)
        evaluation.down = down_count(evaluation)
        evaluation.save()
        up_cnt = evaluation.up
        down_cnt = evaluation.down
        return Response({"up": up_cnt, "down": down_cnt}, status=201)


class CourseList(viewsets.ViewSet):

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
                        raise UnAuthorizedError()
                    result = result.filter(student_id__id=value)
                elif key == 'week':
                    if value != 'all':
                        value += ','
                        result = result.filter(week__icontains=value)
                else:
                    raise ArgumentError()
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
            raise ArgumentError()
        # 其他非法请求
        raise ArgumentError()

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
            raise UnAuthorizedError()
        # 爬虫的数据库插入请求
        if len(req) == 2:
            semester = '2020_Spring'
            # 更新则默认将原记录删除
            StudentCourse.objects.filter(student_id=student_id).delete()
            # 将爬虫爬取的数据写入数据库
            for lists in req['info']:
                for info in lists:
                    add_student_course(student, semester, info)
            return HttpResponse(status=201)
        # 其他非法请求
        raise ArgumentError()

    @staticmethod
    def add_course(request):
        req = request.data
        if 'info' in req.keys():
            for info in req['info']:
                course = add_course(info)
                teacher_list = info[6]
                teachers = teacher_list.split('，')
                for teacher_name in teachers:
                    if teacher_name == "":
                        continue
                    teacher = add_teacher(teacher_name)
                    add_teacher_relation(teacher, course)
            return HttpResponse(status=201)
        raise ArgumentError()


class Search(viewsets.ViewSet):

    @staticmethod
    def get(request):
        req = request.query_params.dict()
        result = TeacherCourse.objects.all()
        if 1 <= len(req) <= 4:
            results = []
            for key, value in req.items():
                if key == 'course' and value != "":
                    name = req['course']
                    result = result.filter(course_id__name__icontains=name)
                elif key == 'teacher' and value != "":
                    name = req['teacher']
                    result = result.filter(teacher_id__name__icontains=name)
                elif key == 'type' and value != "":
                    types = req['type']
                    result = result.filter(course_id__type=types)
                elif key == 'department' and value != "":
                    department = req['department']
                    result = result.filter(course_id__department=department)
                else:
                    raise ArgumentError()
                results = TeacherCourseSerializer(result, many=True).data
            return Response(format_search(results))
        raise ArgumentError()

    @staticmethod
    def default(request):
        req = request.query_params.dict()
        teacher_courses = []
        if 'student_id' in req.keys():
            student_id = req['student_id']
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                raise UnAuthorizedError()
            courses = StudentCourse.objects.filter(student_id=student)
            for course in courses:
                select_course = course.course_id
                teacher_course = TeacherCourse.objects.filter(course_id=select_course)[0]
                teacher_courses.append(teacher_course)
            result = TeacherCourseSerializer(teacher_courses, many=True).data
            return Response(format_search(result))
        raise ArgumentError()


class CourseEvaluations(APIView):

    @staticmethod
    def get(request):
        req = request.query_params.dict()
        result = CourseEvaluation.objects.all()
        teachers = TeacherCourse.objects.all()
        info_dict = {}
        if len(req) == 2:
            try:
                bid = req['bid']
                student_id = req['student_id']
            except KeyError:
                raise ArgumentError()
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                raise UnAuthorizedError()
            try:
                course = Course.objects.get(bid=bid)
            except Course.DoesNotExist:
                raise NotFoundError(detail="没有这门课程")
            result = result.filter(course__bid=bid)
            teachers = teachers.filter(course_id__bid=bid)
            teacher_info = TeacherEvaluationSerializer(teachers, many=True).data
            teacher_info = format_serializer_teacher(teacher_info, student)
            info = CourseEvaluationSerializer(result, many=True).data
            info = format_serializer(info, student)
            avg_score = result.aggregate(Avg('score'))['score__avg']
            evaluation_num = evaluator_count(course)
            info_dict["course_name"] = course.name
            info_dict["evaluation_num"] = evaluation_num
            info_dict["avg_score"] = avg_score
            info_dict["teacher_info"] = teacher_info
            info_dict["info"] = info
            return Response(info_dict)
        raise ArgumentError()

    # 创建新评价/修改评价
    @staticmethod
    def put(request):
        req = request.data
        if len(req) == 4:
            try:
                bid = req['bid']
                text = req['text']
                score = req['score']
                student_id = req['student_id']
            except KeyError:
                raise ArgumentError()
            if not 1 <= score <= 5:
                raise ArgumentError(detail="评分只能为1-5分")
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                raise UnAuthorizedError()
            try:
                course = Course.objects.get(bid=bid)
            except Course.DoesNotExist:
                raise NotFoundError(detail="没有这门课程")
            try:
                evaluation = CourseEvaluation.objects.get(student=student, course=course)
                evaluation.evaluation = text
                evaluation.score = score
            except CourseEvaluation.DoesNotExist:
                evaluation = CourseEvaluation(student=student, course=course, score=score, evaluation=text)
            evaluation.save()
            return HttpResponse(status=201)
        raise ArgumentError()

    # 删除评价
    @staticmethod
    def delete(request):
        req = request.data
        if len(req) == 2:
            try:
                bid = req['bid']
                student_id = req['student_id']
            except KeyError:
                raise ArgumentError()
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                raise UnAuthorizedError()
            try:
                course = Course.objects.get(bid=bid)
            except Course.DoesNotExist:
                raise NotFoundError(detail="没有这门课程")
            try:
                evaluation = CourseEvaluation.objects.get(student=student, course=course)
                evaluation.delete()
                return HttpResponse(status=204)
            except CourseEvaluation.DoesNotExist:
                raise NotFoundError(detail="没有这条评价")
        raise ArgumentError()


class CourseEvaluationAction(viewsets.ViewSet):
    @staticmethod
    def up_action(request):
        req = request.data
        if len(req) == 3:
            actor, evaluation = get_evaluation(req)
            return up_action(evaluation, actor)
        raise ArgumentError()

    @staticmethod
    def cancel_up_action(request):
        req = request.data
        if len(req) == 3:
            actor, evaluation = get_evaluation(req)
            try:
                up_record = EvaluationUpRecord.objects.get(evaluation=evaluation, student=actor)
                up_record.delete()
                evaluation.up = up_count(evaluation)
                evaluation.save()
                up_cnt = evaluation.up
                down_cnt = evaluation.down
                return Response({"up": up_cnt, "down": down_cnt}, status=201)
            except EvaluationUpRecord.DoesNotExist:
                raise NotFoundError(detail="不存在这条点赞记录")
        raise ArgumentError()

    @staticmethod
    def down_action(request):
        req = request.data
        if len(req) == 3:
            actor, evaluation = get_evaluation(req)
            return down_action(evaluation, actor)
        raise ArgumentError()

    @staticmethod
    def cancel_down_action(request):
        req = request.data
        if len(req) == 3:
            actor, evaluation = get_evaluation(req)
            try:
                down = EvaluationDownRecord.objects.get(evaluation=evaluation, student=actor)
                down.delete()
                evaluation.down = down_count(evaluation)
                evaluation.save()
                up_cnt = evaluation.up
                down_cnt = evaluation.down
                return Response({"up": up_cnt, "down": down_cnt}, status=201)
            except EvaluationDownRecord.DoesNotExist:
                raise NotFoundError(detail="不存在这条被踩记录")
        raise ArgumentError()


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
                raise NotFoundError(detail="没有这个老师")
            try:
                course = Course.objects.get(bid=bid)
            except Course.DoesNotExist:
                raise NotFoundError(detail="没有这门课程")
            try:
                student = Student.objects.get(id=actor)
            except Student.DoesNotExist:
                raise UnAuthorizedError()
            try:
                teacher_course = TeacherCourse.objects.get(teacher_id=teacher, course_id=course)
            except TeacherCourse.DoesNotExist:
                raise NotFoundError(detail="没有这个课程评价")
            if action == 'up':
                try:
                    # 已经点过赞
                    TeacherEvaluationRecord.objects.get(teacher_course=teacher_course, student=student)
                    return Response({"up": teacher_course.up}, status=202)
                except TeacherEvaluationRecord.DoesNotExist:
                    # 没点过赞
                    up_record = TeacherEvaluationRecord(teacher_course=teacher_course, student=student)
                    up_record.save()
                    teacher_course.up = up_count_teacher(teacher_course)
                    teacher_course.save()
                return Response({"up": teacher_course.up}, status=201)
            if action == 'cancel_up':
                try:
                    up_record = TeacherEvaluationRecord.objects.get(teacher_course=teacher_course, student=student)
                    up_record.delete()
                    teacher_course.up = up_count_teacher(teacher_course)
                    teacher_course.save()
                except TeacherEvaluationRecord.DoesNotExist:
                    raise NotFoundError(detail="不存在这个点赞记录")
                return Response({"up": teacher_course.up}, status=201)
        raise ArgumentError()
