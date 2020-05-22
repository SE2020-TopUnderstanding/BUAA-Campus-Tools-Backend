from django.test import TestCase, Client
from .views import Student, split_week, split_time, check_public, add_course, add_teacher, add_teacher_relation, \
    add_student_course, down_action, up_check, down_check, up_check_teacher, up_count, down_count, up_action, \
    up_count_teacher, format_search, format_serializer_teacher, format_serializer, evaluator_count, get_evaluation
from .models import Teacher, Course, CourseEvaluation, EvaluationUpRecord, EvaluationDownRecord, \
    TeacherEvaluationRecord, TeacherCourse


# Create your tests here.
class CourseGetTest(TestCase):

    def test_get_success(self):
        client = Client()
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        response = client.get("/timetable/?student_id=17373010&week=all")
        self.assertEqual(response.status_code, 200)

    def test_not_found(self):
        client = Client()
        response = client.get("/timetable/?student_id=17373011&week=all")
        self.assertEqual(response.status_code, 401)

    def test_bad_request1(self):
        client = Client()
        response = client.get("/timetable/")
        self.assertEqual(response.status_code, 400)

    def test_bad_request2(self):
        client = Client()
        response = client.get("/timetable/?student=17373011&week=all")
        self.assertEqual(response.status_code, 400)

    def test_this_week(self):
        client = Client()
        response = client.get("/timetable/?date=2020-4-19")
        self.assertEqual(response.status_code, 200)

    def test_this_week_bad(self):
        client = Client()
        response = client.get("/timetable/?dae=2020-4-19")
        self.assertEqual(response.status_code, 400)

    def test_post2(self):
        client = Client()
        response = client.post("/timetable/", content_type='application/json',
                               data={"student_id": "17373010",
                                     "info": [["111", "(一)305", "荣文戈", "1-16", "周1 第3，4节"]]})
        self.assertEqual(response.status_code, 401)

    def test_post3(self):
        client = Client()
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        response = client.post("/timetable/", content_type='application/json',
                               data={"student_id": "17373010",
                                     "info": [["111", "(一)305", "荣文戈", "1-16", "周1 第3，4节"]]})
        self.assertEqual(response.status_code, 400)

    def test_split_week(self):
        week = "1，2-4单，5-9双，10-11，12"
        self.assertEqual(split_week(week), '1,3,6,8,10,11,12,')

    def test_split_time(self):
        time = "周2 第6，7节"
        self.assertEqual(split_time(time), '2_6_7')

    def test_check_public(self):
        self.assertEqual(check_public("体育(6)", '0001'), '00011')

    def test_add_course(self):
        info = ['计算机网络', '001', '2.0', '32', '计算机学院', '核心专业类']
        self.assertEqual(add_course(info).bid, '001')

    def test_add_teacher(self):
        key = '张辉'
        self.assertEqual(add_teacher(key).name, '张辉')

    def test_add_teacher_relation(self):
        course = Course(bid='111', name='计算机网络', credit='2.0', hours='32', department='计算机学院', type='核心专业类')
        course.save()
        teacher = Teacher(name='张辉')
        teacher.save()
        add_teacher_relation(teacher, course)
        self.assertEqual(True, True)

    def test_add_student_course_relation(self):
        student = Student(id='17373456')
        student.save()
        course = Course(bid='111', name='计算机网络', credit='2.0', hours='32', department='计算机学院', type='核心专业类')
        course.save()
        infos = ['111', '(一)305', '荣文戈， 张辉', '1-16', '周1 第3，4节']
        add_student_course(student=student, semester='2020_Spring', info=infos)
        self.assertEqual(True, True)

    def test_get_evaluation_count(self):
        course = Course(bid='111')
        course.save()
        self.assertEqual(evaluator_count(course), 0)

    def test_up_count(self):
        student = Student(id='17373456')
        student.save()
        course = Course(bid='111')
        course.save()
        evaluation = CourseEvaluation(course=course, student=student)
        evaluation.save()
        self.assertEqual(up_count(evaluation), 0)

    def test_down_count(self):
        student = Student(id='17373456')
        student.save()
        course = Course(bid='111')
        course.save()
        evaluation = CourseEvaluation(course=course, student=student)
        evaluation.save()
        self.assertEqual(down_count(evaluation), 0)

    def test_up_count_teacher(self):
        course = Course(bid='111')
        course.save()
        teacher = Teacher(name='张辉')
        teacher.save()
        teacher_course = TeacherCourse(teacher_id=teacher, course_id=course)
        self.assertEqual(up_count_teacher(teacher_course=teacher_course), False)

    def test_up_check(self):
        student = Student(id='17373456')
        student.save()
        course = Course(bid='111')
        course.save()
        evaluation = CourseEvaluation(course=course, student=student)
        evaluation.save()
        self.assertEqual(up_check(student, evaluation), False)

    def test_down_check(self):
        student = Student(id='17373456')
        student.save()
        course = Course(bid='111')
        course.save()
        evaluation = CourseEvaluation(course=course, student=student)
        evaluation.save()
        self.assertEqual(down_check(student, evaluation), False)

    def test_format_serializer(self):
        student = Student(id='17373456')
        student.save()
        course = Course(bid='111')
        course.save()
        evaluation = CourseEvaluation(course=course, student=student)
        evaluation.save()
        result = [{"id": 1}]
        format_serializer(result, student)
        self.assertEqual(True, True)

    def test_up_check_teacher(self):
        student = Student(id='17373456')
        student.save()
        course = Course(bid='111')
        course.save()
        teacher = Teacher(name='张辉')
        teacher.save()
        teacher_course = TeacherCourse(teacher_id=teacher, course_id=course)
        self.assertEqual(up_check_teacher(student, teacher_course), 0)

    def test_format_serializer_teacher(self):
        student = Student(id='17373456')
        student.save()
        course = Course(bid='111')
        course.save()
        teacher = Teacher(name='张辉')
        teacher.save()
        teacher_course = TeacherCourse(teacher_id=teacher, course_id=course)
        teacher_course.save()
        format_serializer_teacher([{"id": 1}], student)
        self.assertEqual(True, True)

    def test_format_search(self):
        course = Course(bid='111')
        course.save()
        result = [{"bid": "111"}, {"bid": "111"}]
        format_search(result)
        self.assertEqual(True, True)

    def test_get_evaluation(self):
        student = Student(id='17373010', usr_name='111')
        student.save()
        student = Student(id='17373456')
        student.save()
        course = Course(bid='111')
        course.save()
        evaluation = CourseEvaluation(course=course, student=student)
        evaluation.save()
        actor, return_evaluation = get_evaluation({'student_id': '17373456', 'bid': '111', 'actor': '17373010'})
        self.assertEqual(return_evaluation, evaluation)
