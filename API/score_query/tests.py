from django.test import TestCase, Client
import json
from .models import *
from course_query.models import Student
from .views import *


# Create your tests here.
class ScoreGetTest(TestCase):
    def test_get_score(self):
        client = Client()
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        response = client.get("/score/?student_id=17373010&semester=''")
        self.assertEqual(response.status_code, 200)

    def test_get_gpa(self):
        client = Client()
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        score = Score(student_id=student, course_name="123", semester="22", score=22, origin_score="33", label="")
        score.save()

        score = Score(student_id=student, course_name="123", semester="22", score=22, origin_score="优秀", label="")
        score.save()

        score = Score(student_id=student, course_name="123", semester="22", score=22, origin_score="良好", label="")
        score.save()
        score = Score(student_id=student, course_name="123", semester="22", score=22, origin_score="及格", label="")
        score.save()
        score = Score(student_id=student, course_name="123", semester="22", score=22, origin_score="不及格", label="")
        score.save()
        response = client.get("/score/gpa/?student_id=17373010")
        self.assertEqual(response.status_code, 200)

    def test_get_avg_score(self):
        client = Client()
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        score = Score(student_id=student, course_name="123", semester="22", score=22, origin_score="33", label="")
        score.save()
        response = client.get("/score/avg_score/?student_id=17373010")
        self.assertEqual(response.status_code, 200)

    def test_get_score_bad(self):
        client = Client()
        response = client.get("/score/?student_id=17373010&semester=''")
        self.assertEqual(response.status_code, 401)

    def test_get_score_bad2(self):
        client = Client()
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        response = client.get("/score/?student_id=17373010")
        self.assertEqual(response.status_code, 400)

    def test_get_score_bad3(self):
        client = Client()
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        response = client.get("/score/?student_id=17373010&s=""")
        self.assertEqual(response.status_code, 400)

    def test_post_score(self):
        client = Client()
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        data = {"student_id": "17373010", "semester": "2018秋季",
                "info": [["B1A09104A", "工科数学分析(1)", "6.0", "", "99", "99"],
                         ["B1A09104A", "工科数学分析(1)", "6.0", "补考", "99", "99"],
                         ["B1A09104A", "工科数学分析(1)", "6.0", "重修", "99", "99"]]}
        response = client.post("/score/", content_type='application/json',
                               data=data)
        self.assertEqual(response.status_code, 201)

    def test_post_score2(self):
        client = Client()
        data = {"student_id": "17373010", "semester": "2018秋季",
                "info": [["B1A09104A", "工科数学分析(1)", "6.0", "99"]]}
        response = client.post("/score/", content_type='application/json',
                               data=data)
        self.assertEqual(response.status_code, 401)

    def test_post_score3(self):
        client = Client()
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        data = {"student_id": "17373010",
                "info": [["B1A09104A", "工科数学分析(1)", "6.0", "99"]]}
        response = client.post("/score/", content_type='application/json',
                               data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_score4(self):
        client = Client()
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        data = {"student_id": "17373010",
                "info": [["B1A09104A", "工科数学分析(1)", "6.0", "99"]]}
        response = client.post("/score/", content_type='application/json',
                               data=data)
        self.assertEqual(response.status_code, 400)
